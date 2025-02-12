[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/xezpeleta/whisper-euskaraz) [![Follow me on HF](https://huggingface.co/datasets/huggingface/badges/resolve/main/follow-me-on-HF-md-dark.svg)](https://huggingface.co/xezpeleta)

# Whisper in Basque

In this project, you will find information about Whisper models trained for the Basque language.

You can find more information about the fine-tuning process used to train the models [here](train/README.md).

## What is Whisper?

**_Whisper_** is a tool for speech recognition (ASR, STT or speech-to-text technology). It was [released](https://openai.com/index/whisper/) by *OpenAI* in 2022 as open-source software (under MIT license).

## Can it transcribe Basque audio?

The models released by *OpenAI* provide relatively poor results with Basque audio.

However, thanks to thousands of recordings collected through the [Mozilla Common Voice](https://commonvoice.mozilla.org) project, it is possible to train the original models to achieve better results.

- This training process is called *fine-tuning*. If you want to learn more about this, you can check the [TRAIN](train/README.md) section.
- The differences between the original models and the trained models can be seen in the [EVAL](eval/README.md) section.

Below are the steps to download and use the Basque Whisper models.

### Some examples

Using the Basque *medium* model, the following audios have been transcribed as examples:

[![Amets Arzallus](https://github.com/user-attachments/assets/1b9dbc74-04ce-4716-9705-c2666ba9fc0d)](https://www.youtube.com/watch?v=JQVJawzT6Vo)

[![Xabier Usabiaga](https://github.com/user-attachments/assets/959e13b5-abe5-41c2-b6ef-d8501a8597e2)](https://www.youtube.com/watch?v=mzcxip0FRA0)

## Where can I find the Basque models?

The trained models can be found on [*Hugging Face*](https://huggingface.co/xezpeleta/):

| Model    | Size    | WER   | GGML                                                                                                           |                                                                |
| -------- | ------- | ----- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| *small*  | 488 MB  | 11.83 | [Download](https://huggingface.co/xezpeleta/whisper-small-eu/resolve/main/ggml-small.eu.bin?download=true)     | [![Model on HF](https://huggingface.co/datasets/huggingface/badges/resolve/main/model-on-hf-sm.svg)](https://huggingface.co/xezpeleta/whisper-small-eu)  |
| *medium* | 1.53 GB | 8.80  | [Download](https://huggingface.co/xezpeleta/whisper-medium-eu/resolve/main/ggml-medium.eu.bin?download=true)   | [![Model on HF](https://huggingface.co/datasets/huggingface/badges/resolve/main/model-on-hf-sm.svg)](https://huggingface.co/xezpeleta/whisper-medium-eu) |
| *large*  | 3.1 GB  | 7.21  | [Download](https://huggingface.co/xezpeleta/whisper-large-eu/resolve/main/ggml-large.eu.bin?download=true)     | [![Model on HF](https://huggingface.co/datasets/huggingface/badges/resolve/main/model-on-hf-sm.svg)](https://huggingface.co/xezpeleta/whisper-large-eu)  |

For good results, using the **Medium** model is recommended.

## How to use? (Linux)

There are different ways and implementations to use Whisper. This guide will explain the steps to use it through *Whisper.cpp*.

### Installation

Clone the repository:

```bash
git clone https://github.com/ggerganov/whisper.cpp.git
```

Compile:

```bash
make
```

Download the Basque model (*GGML* file) to the `models` directory (__*medium* model is recommended__)

```bash
curl -L "https://huggingface.co/xezpeleta/whisper-medium-eu/resolve/main/ggml-medium.eu.bin?download=true" -o models/ggml-medium-eu.bin
```

## Usage

### Process Audio

Before using Whisper, we need to process the audio (obtain a *wav* file):

```bash
ffmpeg -i file.mp3 -ar 16000 -ac 1 -c:a pcm_s16le file.wav
```

### Transcription

Then, we can use Whisper.cpp:

```bash
./main -m models/ggml-medium.eu.bin -f samples/file.wav -l eu -pc
```

![image](https://github.com/user-attachments/assets/65abc864-41bf-4bab-ad56-c654d8af4f44)

To create subtitles, you can use this command:

```bash
./main -m models/ggml-medium.eu.bin -f file.wav -l eu -osrt -ml 56 -sow
```

-  `-osrt`: srt file (subtitles)
- `-ml 56`: max length (56 characters)
- `-sow`: word-level segments

If desired, you can modify the video to embed the subtitles in the image:

```bash
ffmpeg -i samples/original_video.mp4 -vf subtitles=samples/subtitles.srt samples/new_video.mp4
```

## How to use? (Windows) -in progress-

On Windows operating system, you can use [SubtitleEdit](https://github.com/SubtitleEdit/subtitleedit).

> [!NOTE]
> This section is still under development.

## What are the main issues detected?

### Dialects and variants

The best results are obtained in standard Basque (euskara batua).

### Hallucinations

The *Whisper* tool sometimes has *hallucinations*, especially in silent periods at the beginning and end of audio.