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
            f"{','.join(sample.keys())}. Ensure a text column name is present in the dataset."
        )

def get_text_column_names(column_names):
    # If we're dealing with a streaming dataset, column_names might be None
    if column_names is None:
        return None
        
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
    return None

whisper_norm = BasicTextNormalizer()
def normalise(batch):
    batch["norm_text"] = whisper_norm(get_text(batch))
    return batch

def data(dataset, is_common_voice=False):
    for i, item in enumerate(dataset):
        try:
            if is_common_voice:
                # Common Voice style - simpler audio handling
                yield {**item["audio"], "reference": get_text(item), "norm_reference": item["norm_text"]}
            else:
                # Custom dataset style with more robust audio handling
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
                        import io
                        import soundfile as sf
                        audio_bytes = io.BytesIO(audio_data["bytes"])
                        raw_audio, sampling_rate = sf.read(audio_bytes)
                    except Exception as e:
                        print(f"Warning: Could not load audio from bytes for item {i}: {str(e)}")
                        try:
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
    
    # Initialize the ASR pipeline
    whisper_asr = pipeline(
        "automatic-speech-recognition",
        model=model_id,
        device=args.device,
        chunk_length_s=30,
        stride_length_s=5
    )

    print("Setting forced decoder ids for language:", args.language)
    whisper_asr.model.config.forced_decoder_ids = (
        whisper_asr.tokenizer.get_decoder_prompt_ids(
            language=args.language, task="transcribe"
        )
    )
    
    print("\nLoading dataset...")
    if args.is_common_voice:
        # Common Voice style loading
        dataset = load_dataset(
            args.dataset,
            args.config,
            split=args.split,
            token=True,
        )
        dataset = dataset.cast_column("audio", Audio(sampling_rate=16000))
    else:
        # For other datasets, use more flexible loading with feature detection
        features = {
            'audio': Audio(sampling_rate=16000),
        }
        
        text_keys = ['sentence', 'text', 'transcript', 'transcription', 'normalized_text']
        for key in text_keys:
            features[key] = Value('string')
            
        try:
            dataset = load_dataset(
                args.dataset,
                args.config,
                split=args.split,
                streaming=args.streaming,
                features=features
            )
        except Exception as e:
            print(f"Error loading dataset with detected features: {str(e)}")
            print("Falling back to default dataset features...")
            dataset = load_dataset(
                args.dataset,
                args.config,
                split=args.split,
                streaming=args.streaming
            )
    
    print("Dataset loaded. Processing...")
    
    # Handle streaming datasets differently
    if args.streaming:
        # For streaming datasets, we'll check the first item to determine the structure
        first_item = next(iter(dataset))
        available_columns = first_item.keys() if first_item else []
        text_column_name = get_text_column_names(available_columns)
        dataset = dataset.map(normalise)
        if text_column_name:
            dataset = dataset.filter(lambda x: is_target_text_in_range(get_text(x)))
    else:
        dataset = dataset.map(normalise, num_proc=2)
        text_column_name = get_text_column_names(dataset.column_names)
        if text_column_name:
            dataset = dataset.filter(
                is_target_text_in_range, 
                input_columns=[text_column_name],
                num_proc=2
            )

    # Instead of erroring out, we'll continue even without a specific text column
    # since we have the get_text function that can handle multiple column names
    if not text_column_name:
        print("Warning: Could not explicitly identify text column, will try to infer from each item")

    predictions = []
    references = []
    norm_predictions = []
    norm_references = []
    
    # Process the dataset
    pbar = tqdm(desc='Decode Progress')
    
    if args.streaming or not args.is_common_voice:
        # Process one by one for streaming or custom datasets
        for item in data(dataset, args.is_common_voice):
            try:
                out = whisper_asr(item)
                predictions.append(out["text"])
                references.append(item["reference"])
                norm_predictions.append(whisper_norm(out["text"]))
                norm_references.append(item["norm_reference"])
                pbar.update(1)
            except Exception as e:
                print(f"\nError processing audio: {str(e)}")
                continue
    else:
        # Batch processing for Common Voice dataset
        for out in whisper_asr(data(dataset, True), batch_size=args.batch_size):
            predictions.append(out["text"])
            references.append(out["reference"][0])
            norm_predictions.append(whisper_norm(out["text"]))
            norm_references.append(out["norm_reference"][0])
            pbar.update(1)
    
    pbar.close()
    
    if not predictions:
        print("\nNo valid predictions were generated. Please check the dataset structure and audio files.")
        return

    # Calculate metrics
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

    # Save results
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
        "--is_common_voice",
        required=False,
        default=False,
        type=lambda x: (str(x).lower() == 'true'),
        help="Whether the dataset is Common Voice format.",
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
