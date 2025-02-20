import os
import argparse
import evaluate
from tqdm import tqdm
from pathlib import Path
from transformers import pipeline
from datasets import load_dataset, Audio, Value
from transformers.models.whisper.english_normalizer import BasicTextNormalizer

wer_metric = evaluate.load("wer")
cer_metric = evaluate.load("cer")

def is_target_text_in_range(ref):
    if ref.strip() == "ignore time segment in scoring":
        return False
    else:
        return ref.strip() != ""


def get_text(sample):
    if "text" in sample:
        return sample["text"]
    elif "sentence" in sample:
        return sample["sentence"]
    elif "normalized_text" in sample:
        return sample["normalized_text"]
    elif "transcript" in sample:
        return sample["transcript"]
    elif "transcription" in sample:
        return sample["transcription"]
    else:
        raise ValueError(
            f"Expected transcript column of either 'text', 'sentence', 'normalized_text' or 'transcript'. Got sample of "
            ".join{sample.keys()}. Ensure a text column name is present in the dataset."
        )


def get_text_column_names(column_names):
    if "text" in column_names:
        return "text"
    elif "sentence" in column_names:
        return "sentence"
    elif "normalized_text" in column_names:
        return "normalized_text"
    elif "transcript" in column_names:
        return "transcript"
    elif "transcription" in column_names:
        return "transcription"


whisper_norm = BasicTextNormalizer()
def normalise(batch):
    batch["norm_text"] = whisper_norm(get_text(batch))
    return batch


def data(dataset):
    for i, item in enumerate(dataset):
        try:
            if i == 0:
                print("First item structure:", item.keys())
                if "audio" in item:
                    print("Audio structure:", item["audio"].keys() if isinstance(item["audio"], dict) else "direct array")

            if "audio" not in item:
                print(f"Warning: Item {i} has no audio data")
                continue

            # Load audio data
            audio_data = item["audio"]
            if isinstance(audio_data, dict) and "bytes" in audio_data and "path" in audio_data:
                try:
                    # Load audio using soundfile
                    import io
                    import soundfile as sf
                    audio_bytes = io.BytesIO(audio_data["bytes"])
                    raw_audio, sampling_rate = sf.read(audio_bytes)
                except Exception as e:
                    print(f"Warning: Could not load audio from bytes for item {i}: {str(e)}")
                    try:
                        # Fallback to loading from path
                        raw_audio, sampling_rate = sf.read(audio_data["path"])
                    except Exception as e:
                        print(f"Warning: Could not load audio from path for item {i}: {str(e)}")
                        continue
            elif isinstance(audio_data, dict) and "array" in audio_data:
                raw_audio = audio_data["array"]
                sampling_rate = audio_data.get("sampling_rate", 16000)
            else:
                print(f"Warning: Item {i} has invalid audio data format")
                continue

            if raw_audio is None or (hasattr(raw_audio, "size") and raw_audio.size == 0):
                print(f"Warning: Item {i} has empty audio data")
                continue

            reference = get_text(item)
            if not reference:
                print(f"Warning: Item {i} has no reference text")
                continue

            yield {
                "raw": raw_audio,
                "sampling_rate": sampling_rate,
                "reference": reference,
                "norm_reference": item.get("norm_text", reference)
            }
        except Exception as e:
            print(f"Error processing item {i}: {str(e)}")
            continue


def main(args):
    if args.is_public_repo == False:
        os.system(f"mkdir -p {args.temp_ckpt_folder}")
        ckpt_dir_parent = str(Path(args.ckpt_dir).parent)
        os.system(f"cp {ckpt_dir_parent}/added_tokens.json {ckpt_dir_parent}/normalizer.json \
        {ckpt_dir_parent}/preprocessor_config.json {ckpt_dir_parent}/special_tokens_map.json \
        {ckpt_dir_parent}/tokenizer_config.json {ckpt_dir_parent}/merges.txt \
        {ckpt_dir_parent}/vocab.json {args.ckpt_dir}/config.json {args.ckpt_dir}/pytorch_model.bin \
        {args.ckpt_dir}/training_args.bin {args.temp_ckpt_folder}")
        model_id = args.temp_ckpt_folder
    else:
        model_id = args.hf_model

    print(f"Loading model: {model_id}")
    
    # First, load the dataset in streaming mode to inspect its structure
    print("\nInspecting dataset structure...")
    inspection_dataset = load_dataset(
        args.dataset,
        args.config,
        split=args.split,
        streaming=True  # Force streaming for inspection
    )
    
    # Get the first item to inspect the structure
    first_item = next(iter(inspection_dataset))
    print(f"Dataset features structure:")
    for key, value in first_item.items():
        if isinstance(value, dict):
            print(f"{key}: {value.keys()}")
        else:
            print(f"{key}: {type(value)}")
    
    # Get features from inspection to dynamically build the feature dict
    features = {}
    
    # Flexible feature mapping based on inspection
    if 'audio' in first_item:
        features['audio'] = Audio(sampling_rate=16000)
    
    text_keys = ['sentence', 'text', 'transcript', 'transcription', 'normalized_text']
    for key in text_keys:
        if key in first_item:
            features[key] = Value('string')
            break
    
    if 'duration' in first_item:
        features['duration'] = Value('float32')
    
    print("\nDetected features:", features)
    
    # Load dataset with detected features
    try:
        dataset = load_dataset(
            args.dataset,
            args.config,
            split=args.split,
            streaming=True,  # Always use streaming for large datasets
            features=features
        )
    except Exception as e:
        print(f"Error loading dataset with detected features: {str(e)}")
        print("Falling back to default dataset features...")
        dataset = load_dataset(
            args.dataset,
            args.config,
            split=args.split,
            streaming=True  # Always use streaming for large datasets
        )
    
    print(f"\nDataset info:")
    print(f"Column names: {dataset.column_names}")
    
    text_column_name = get_text_column_names(dataset.column_names)
    if not text_column_name:
        print("Error: Could not find a valid text column in the dataset")
        return
        
    print(f"Using text column: {text_column_name}")
    
    # Initialize the ASR pipeline with parameters based on dataset inspection
    print("\nInitializing ASR pipeline...")
    whisper_asr = pipeline(
        "automatic-speech-recognition",
        model=model_id,
        device=args.device,
        chunk_length_s=30,
        stride_length_s=5,
        batch_size=1  # For streaming, process one at a time
    )

    print("Setting forced decoder ids for language:", args.language)
    whisper_asr.model.config.forced_decoder_ids = (
        whisper_asr.tokenizer.get_decoder_prompt_ids(
            language=args.language, task="transcribe"
        )
    )
    
    print("Starting dataset preprocessing")
    
    # Always use streaming mode, so remove the streaming check
    dataset = dataset.map(normalise)
    dataset = dataset.filter(lambda x: is_target_text_in_range(get_text(x)))
    print("Dataset preprocessing complete")

    predictions = []
    references = []
    norm_predictions = []
    norm_references = []
    
    # Initialize progress bar with unknown total for streaming dataset
    pbar = tqdm(desc='Decode Progress')
    
    # Process the dataset with better error handling
    for item in data(dataset):
        try:
            out = whisper_asr({
                "raw": item["raw"],
                "sampling_rate": item["sampling_rate"]
            })
            predictions.append(out["text"])
            references.append(item["reference"])
            norm_predictions.append(whisper_norm(out["text"]))
            norm_references.append(item["norm_reference"])
            pbar.update(1)
        except Exception as e:
            print(f"\nError processing audio: {str(e)}")
            continue
    
    pbar.close()
    
    if not predictions:
        print("\nNo valid predictions were generated. Please check the dataset structure and audio files.")
        return

    wer = wer_metric.compute(references=references, predictions=predictions)
    cer = cer_metric.compute(references=references, predictions=predictions)
    norm_wer = wer_metric.compute(references=norm_references, predictions=norm_predictions)
    norm_cer = cer_metric.compute(references=norm_references, predictions=norm_predictions)

    wer = round(100 * wer, 2)
    cer = round(100 * cer, 2)
    norm_wer = round(100 * norm_wer, 2)
    norm_cer = round(100 * norm_cer, 2)

    print("\nWER : ", wer)
    print("CER : ", cer)
    print("\nNORMALIZED WER : ", norm_wer)
    print("NORMALIZED CER : ", norm_cer)

    os.system(f"mkdir -p {args.output_dir}")
    dset = args.dataset.replace('/', '_') + '_' + args.config + '_' + args.split
    op_file = args.output_dir + '/' + dset
    if args.is_public_repo:
            op_file = op_file + '_' + args.hf_model.replace('/', '_')
    else:
        op_file = op_file + '_' + args.ckpt_dir.split('/')[-1].replace('/', '_')
    result_file = open(op_file, 'w')
    result_file.write('\nWER: ' + str(wer) + '\n')
    result_file.write('CER: ' + str(cer) + '\n')
    result_file.write('\nNORMALIZED WER: ' + str(norm_wer) + '\n')
    result_file.write('NORMALIZED CER: ' + str(norm_cer) + '\n\n\n')

    for ref, hyp in zip(references, predictions):
        result_file.write('REF: ' + ref + '\n')
        result_file.write('HYP: ' + hyp + '\n')
        result_file.write("------------------------------------------------------" + '\n')
    result_file.close()

    if args.is_public_repo == False:
        os.system(f"rm -r {args.temp_ckpt_folder}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--is_public_repo",
        required=False,
        default=True, 
        type=lambda x: (str(x).lower() == 'true'),
        help="If the model is available for download on huggingface.",
    )
    parser.add_argument(
        "--hf_model",
        type=str,
        required=False,
        default="openai/whisper-tiny",
        help="Huggingface model name. Example: openai/whisper-tiny",
    )
    parser.add_argument(
        "--ckpt_dir",
        type=str,
        required=False,
        default=".",
        help="Folder with the pytorch_model.bin file",
    )
    parser.add_argument(
        "--temp_ckpt_folder",
        type=str,
        required=False,
        default="temp_dir",
        help="Path to create a temporary folder containing the model and related files needed for inference",
    )
    parser.add_argument(
        "--language",
        type=str,
        required=False,
        default="hi",
        help="Two letter language code for the transcription language, e.g. use 'hi' for Hindi. This helps initialize the tokenizer.",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        required=False,
        default="mozilla-foundation/common_voice_11_0",
        help="Dataset from huggingface to evaluate the model on. Example: mozilla-foundation/common_voice_11_0",
    )
    parser.add_argument(
        "--config",
        type=str,
        required=False,
        default="hi",
        help="Config of the dataset. Eg. 'hi' for the Hindi split of Common Voice",
    )
    parser.add_argument(
        "--split",
        type=str,
        required=False,
        default="test",
        help="Split of the dataset. Eg. 'test'",
    )
    parser.add_argument(
        "--device",
        type=int,
        required=False,
        default=0,
        help="The device to run the pipeline on. -1 for CPU, 0 for the first GPU (default) and so on.",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        required=False,
        default=16,
        help="Number of samples to go through each streamed batch.",
    )
    parser.add_argument(
        "--streaming",
        type=lambda x: (str(x).lower() == 'true'),
        required=False,
        default=False,
        help="Whether to stream the dataset instead of downloading it completely. Useful for large datasets.",
    )
    parser.add_argument(
        "--output_dir", 
        type=str, 
        required=False, 
        default="predictions_dir", 
        help="Output directory for the predictions and hypotheses generated.",
    )

    args = parser.parse_args()
    main(args)
