
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/xezpeleta/whisper-euskaraz) [![Follow me on HF](https://huggingface.co/datasets/huggingface/badges/resolve/main/follow-me-on-HF-md-dark.svg)](https://huggingface.co/xezpeleta)

# Whisper euskaraz

Proiektu honetan euskarazko *Whisper* ereduei buruzko informazioa aurkituko duzu.

Ereduak trebatzeko jarraitutako *fine-tuning* prozesuaren inguruan informazio gehiago [hemen](train/README.md) aurki dezakezu.


## Zer da Whisper ?

**_Whisper_** ahots errekonozimendurako adimen artifizialeko tresna da. *OpenAI* enpresak 2022 urtean [argitaratu zuen](https://openai.com/index/whisper/) *software libre* gisa (MIT lizentzipean).

## Euskarazko audioak transkribatzeko gai da?

*OpenAI*k argitaratutako ereduek emaitza nahiko kaxkarrak eskeintzen dizkigute euskarazko audioetan.

Alabaina, [Mozilla Common Voice](https://commonvoice.mozilla.org) proiektuan jasotako milaka grabazioei esker, jatorrizko ereduak trebatzea posible da, emaitza txukunagoak lortzeko.

- Trebatze prozesu honi *fine-tuning* deitzen zaio. Honi buruz gehiago jakin nahi baduzu, [TRAIN](train/README.md) atalera jo dezakezu.
- Jatorrizko ereduen eta trebatutako ereduen arteko diferentziak ikus daitezke [EVAL](eval/README.md) atalean.

Jarraian euskarazko *Whisper* ereduak deskargatu eta erabiltzeko urratsak azalduko dira.

### Zeinbat adibide

Euskarazko *medium* eredua erabiliz, hurrengo audio hauek transkribatu dira adibide gisa:

[![Amets Arzallus](https://github.com/user-attachments/assets/1b9dbc74-04ce-4716-9705-c2666ba9fc0d)](https://www.youtube.com/watch?v=JQVJawzT6Vo)

[![Xabier Usabiaga](https://github.com/user-attachments/assets/959e13b5-abe5-41c2-b6ef-d8501a8597e2)](https://www.youtube.com/watch?v=mzcxip0FRA0)


## Non aurki daitezke euskarazko ereduak?

Trebatutako ereduak [*Hugging Face*](https://huggingface.co/xezpeleta/) webgunean aurki daitezke:

| Eredua   | Tamaina | WER   | GGML | CTranslate2 | |
| -------- | ------- | ----- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- | ---- |
| *tiny*   | 37.8M   | 13.56 | [Deskargatu](https://huggingface.co/xezpeleta/whisper-tiny-eu/resolve/main/ggml-tiny.eu.bin?download=true)     | [whisper-tiny-eu-ct2](https://huggingface.co/xezpeleta/whisper-tiny-eu-ct2), [whisper-tiny-eu-ct2-int8](https://huggingface.co/xezpeleta/whisper-tiny-eu-ct2-int8) | [![Model on HF](https://huggingface.co/datasets/huggingface/badges/resolve/main/model-on-hf-sm.svg)](https://huggingface.co/xezpeleta/whisper-tiny-eu)   |
| *base* | 72.6M | 10.78 | [Deskargatu](https://huggingface.co/xezpeleta/whisper-base-eu/resolve/main/ggml-base.eu.bin?download=true) | [whisper-base-eu-ct2](https://huggingface.co/xezpeleta/whisper-base-eu-ct2), [whisper-base-eu-ct2-int8](https://huggingface.co/xezpeleta/whisper-base-eu-ct2-int8) | [![Model on HF](https://huggingface.co/datasets/huggingface/badges/resolve/main/model-on-hf-sm.svg)](https://huggingface.co/xezpeleta/whisper-base-eu) |
| *small*  | 242M (488MB)  | 7.63 | [Deskargatu](https://huggingface.co/xezpeleta/whisper-small-eu/resolve/main/ggml-small.eu.bin?download=true)   | [whisper-small-eu-ct2](https://huggingface.co/xezpeleta/whisper-small-eu-ct2), [whisper-small-eu-ct2-int8](https://huggingface.co/xezpeleta/whisper-small-eu-ct2-int8) | [![Model on HF](https://huggingface.co/datasets/huggingface/badges/resolve/main/model-on-hf-sm.svg)](https://huggingface.co/xezpeleta/whisper-small-eu)  |
| *medium* | 764M (1.53GB) | 7.14  | [Deskargatu](https://huggingface.co/xezpeleta/whisper-medium-eu/resolve/main/ggml-medium.eu.bin?download=true) | [whisper-medium-eu-ct2](https://huggingface.co/xezpeleta/whisper-medium-eu-ct2) | [![Model on HF](https://huggingface.co/datasets/huggingface/badges/resolve/main/model-on-hf-sm.svg)](https://huggingface.co/xezpeleta/whisper-medium-eu) |
| *large*  | 1.54B (3.1GB)  | 4.84  | [Deskargatu](https://huggingface.co/xezpeleta/whisper-large-eu/resolve/main/ggml-large.eu.bin?download=true)   | [whisper-large-v3-eu-ct2](https://huggingface.co/xezpeleta/whisper-large-v3-eu-ct2) | [![Model on HF](https://huggingface.co/datasets/huggingface/badges/resolve/main/model-on-hf-sm.svg)](https://huggingface.co/xezpeleta/whisper-large-eu)  |

*OHARRA*: ebaluazio datuak *Mozilla Common Voice 18.0* datuetan oinarrituta daude, `test` zatian eta normalizatutako *WER* balioak erabiliz. Informazio gehiagorako, [EVAL](eval/README.md) atalera jo dezakezu.


Emaitza onak lortzeko, **Medium** eredua erabiltzea gomendatzen da.

## Nola erabili? (Linux)

Whisper erabiltzeko modu edota inplementazio ezberdinak daude. Gida honetan *Whisper.cpp* bidez erabiltzeko urratsak azalduko dira.

### Instalazioa

Errepositorioa klonatu:

```bash
git clone https://github.com/ggerganov/whisper.cpp.git
```

Konpilatu:

```bash
make
```

Deskargatu euskarazko eredua (*GGML* fitxategia) `models` direktoriora (__*medium* eredua erabiltzea gomendatzen da__)

```bash
curl -L "https://huggingface.co/xezpeleta/whisper-medium-eu/resolve/main/ggml-medium.eu.bin?download=true" -o models/ggml-medium-eu.bin
```

## Erabilera

### Audioak prozesatu

Whisper erabili aurretik, audioa prozesatu behar dugu (*wav* fitxategia lortu behar dugu):

```bash
ffmpeg -i fixategia.mp3 -ar 16000 -ac 1 -c:a pcm_s16le fitxategia.wav
```

### Transkripzioa

Ondoren, Whisper.cpp erabili dezakegu:

```bash
./main -m models/ggml-medium.eu.bin -f samples/fitxategia.wav -l eu -pc
```

![irudia](https://github.com/user-attachments/assets/65abc864-41bf-4bab-ad56-c654d8af4f44)



Azpitituluak sortzeko, honako agindu hau erabil daitezke:

```bash
./main -m models/ggml-medium.eu.bin -f 
fitxategia.wav -l eu -osrt -ml 56 -sow
```

-  `-osrt`: srt fitxategia (azpitituluak)
- `-ml 56`: max length edo gehienezko luzeera (56 karaktere)
- `-sow`: hitzen baitako segmentuak

Nahi izanez gero, bideoa moldatu dezakegu, azpitituluak irudian bertan txertatzeko:

```bash
ffmpeg -i samples/jatorrizko_bideoa.mp4 -vf subtitles=samples/azpitituluak.srt samples/bideo_berria.mp4
```


## Nola erabili? (Windows) -osatzeke-

Windows sistema eragilean, [SubtitleEdit](https://github.com/SubtitleEdit/subtitleedit) erabili daiteke.

> [!OHARRA]
> Atal hau oraindik osatzen ari gara.

## Zeintzuk dira detektatutako arazo nagusiak?

### Euskalkiak eta aldaerak

Emaitza txukunenak euskara batuan lortzen dira.

### Haluzinazioak

*Whisper* tresnak batzuetan *haluzinazioak* ditu, bereziki audio hasiera eta amaierako isiluneetan.
