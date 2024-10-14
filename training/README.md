# Whisper euskarazko ereduak sortzeko prozesua

## Beharrezko hardwarea

*Fine-tuning* prozesua burutzeko, beharrezkoa da GPU duen ordenagailua. Proba honetan, *Small* eta *Medium* ereduak trebatzeko, NVIDIA RTX 3090 txartelak erabili dira Ubuntu Linux 24.04 sisteman.

Noski, Nvidia driver egokia instalatuta izan behar da, baita CUDA eta cuDNN liburutegiak ere.

## Ingurunea prestatu

Instalatu ondorengo paketeak:

```bash
sudo apt install git git-lfs python-venv ffmpeg
```

Aktibatu *git-lfs*:

```bash
git lfs install
```

Deskargatu errepositorio hau:

```bash
git clone https://github.com/xezpeleta/whisper-euskaraz.git
```

Sortu ingurune birtuala eta aktibatu:

```bash
cd whisper-euskaraz
python3 -m venv .venv
source .venv/bin/activate
```

## Instalatu beharrezko liburutegiak

```bash
pip install -r requirements.txt
```

## (Aukerazkoa) Autentikatu Hugging Face-en

Eredua trebatu ostean, argitaratu eta elkarbanatu ahal izateko, Hugging Faceko zerbitzuan erabiltzailea sortue ta ondoren ordenagailutik autentikatzea beharrezkoa izango da.

Datasetak deskargatzeko ere posible da autentikatua egon behar izatea.

Horretarako, jarraitu hurrengo pausoak:

```bash
git config --global credential.helper store
huggingface-cli login
```

## (Aukerazkoa) Konfiguratu Wandb

*Fine-tuning* prozesua nola doan ikusteko, *wandb* zerbitzua erabiltzen da. Horretarako, beharrezkoa da *wandb* kontua sortzea eta API gako bat lortzea.

## Fine-tuning prozesua

### Ezarri parametroak

Erabili `run.sh` script-a fine-tuning prozesua hasteko. Aurrez ezarritako parametroak aldatu daitezke script honetan. Besteak beste:

- `--model_name_or_path`: Trebatzeko jatorrizko eredua
- `--dataset_name`: Erabiliko den dataset-a (Mozilla Common Voice gure kasuan)
- `--learning_rate`: *Learning rate* balioa ezarri (ereduaren tamainaaren arabera)
- `--per_device_train_batch_size`: *Batch size" balioa (Ezarri zure GPUaren ezaugarrien arabera)

*Learning rate* hiperparametroa ezartzeko, [taula hau](https://github.com/vasistalodagala/whisper-finetune?tab=readme-ov-file#hyperparameter-tuning) erabili erreferentzi gisa.
