# Ebaluazioa

## Emaitzak

Ondorengo taula honetan ikus daitezke Whisper jatorrizko (*pre-trained*) ereduaren eta moldatutako euskarazko ereduaren ebaluazio emaitzak.

*Oharra: normalizatutako WER/CER balioak*

### Whisper *small* eredua

#### Jatorrizko eredua (*pre-trained*)

| Data | Eredua | WER | CER | Dataset |
| ---- | ------ | --- | --- | ------- |
|2024/10 | whisper-small | 159.58 | 57.71 | CV17.0 |


#### Euskarazko ereduak (*fine-tuned*)

| Data | Eredua | WER | CER | Dataset | Bal. orduak |
| ---- | ------ | --- | --- | ------- | ------------ |
|2022/12 | whisper-small-eu | 18.95 | - | CV11.0 | 100 |
|2023/07 | whisper-small-eu | 18.77 | - | CV13.0 | 101 |
|2023/12 | whisper-small-eu | 12.01 | - | CV16.0 | 220 |
|2024/10 | whisper-small-eu | **11.84** | 2.31 | CV17.0 | 274 |

### Whisper *medium* eredua

#### Jatorrizko eredua (*pre-trained*)

| Data | Eredua | WER | CER | Dataset |
| ---- | ------ | --- | --- | ------- |
| 2024/10 | whisper-medium  | 128.34  |  57.2 | CV17.0 |

#### Euskarazko ereduak (*fine-tuned*)

| Data | Eredua | WER | CER | Dataset | Bal. orduak |
| ---- | ------ | --- | --- | ------- | ------------ |
| 2023/07 | whisper-medium-eu | 12.88 | - | CV13.0 | 101 |
| 2023/12 | whisper-medium-eu | 9.18 | - | CV16.0 | 220 |
| 2024/10 | whisper-medium-eu | **8.80** | - | CV17.0 | 274 |


## Nola burutu ebaluazioa?

### *Fine-tuning* egiteko prozesuan bertan

*Fine-tuning*-a egiteko erabili den Python scriptak berak ebaluazioa burutzeko aukera ematen du. 

Horretarako, *fine-tuning* prozesuan erabiliko den *dataset* berdina erabiliko da. Hurrengo parametroak zehaztu behar dira:

```bash
--eval_split_name="test" \
--per_device_eval_batch_size=8 \
--evaluation_strategy="steps" \
--eval_steps=1000 \
--do_eval \
--do_normalize_eval \
```

### Ebaluazioa soilik

Ebaluazioa soilik burutzeko, direktorio honetako scriptak erabili daitezke.

```bash
bash run_eval.sh
```

Ebaluazioko parametroak zehaztu behar dira. Horretarako, editatu `run_eval.sh` fitxategia:

```bash
#! /usr/bin/env bash

python3 evaluate_on_hf_dataset.py \
--is_public_repo True \
--hf_model xezpeleta/whisper-medium-eu \
--language eu \
--dataset "mozilla-foundation/common_voice_17_0" \
--config eu \
--split test \
--device 0 \
--batch_size 16 \
--output_dir predictions
```

Adibide honetan, `whisper-medium-eu` eredua erabiliko da, `eu` hizkuntza eta `mozilla-foundation/common_voice_17_0` *dataset* erabiliko da.

Emaitzak `predictions` direktorioan gordeko dira.
