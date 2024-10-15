
# Whisper euskaraz

Proiektu honetan euskarazko *Whisper* ereduei buruzko informazioa aurkituko duzu.

Ereduak trebatzeko jarraitutako *fine-tuning* prozesuaren inguruan informazio gehiago [hemen](training/README.md) aurki dezakezu.


## Zer da Whisper ?

**_Whisper_** ahots errekonozimendurako adimen artifizialeko tresna da. *OpenAI* enpresak 2022 urtean [argitaratu zuen](https://openai.com/index/whisper/) *software libre* gisa (MIT lizentzipean).

## Euskarazko audioak transkribatzeko gai da?

*OpenAI*k argitaratutako ereduek emaitza nahiko kaxkarrak eskeintzen dizkigute euskarazko audioetan.

Alabaina, [Mozilla Common Voice](https://commonvoice.mozilla.org) proiektuan jasotako milaka grabazioei esker, jatorrizko ereduak trebatzea posible da, emaitza txukunagoak lortzeko.

Prozesu honi *fine-tuning* deitzen zaio. Honi buruz gehiago jakin nahi baduzu, [TRAINING](training/README.md) atalera jo dezakezu.

Jatorrizko ereduen eta trebatutako ereduen arteko diferentziak ikus daitezke [EVAL](eval/README.md) atalean.

### Zeinbat adibide

Euskarazko *medium* eredua erabiliz, hurrengo audio hauek transkribatu dira adibide gisa:

[![Amets Arzallus](https://github.com/user-attachments/assets/1b9dbc74-04ce-4716-9705-c2666ba9fc0d)](https://www.youtube.com/watch?v=JQVJawzT6Vo)

[![Xabier Usabiaga](https://github.com/user-attachments/assets/959e13b5-abe5-41c2-b6ef-d8501a8597e2)](https://www.youtube.com/watch?v=mzcxip0FRA0)


## Non aurki daitezke euskarazko ereduak?

Trebatutako ereduak *Hugging Face* webgunean aurki daitezke:

| Eredua   | Tamaina | WER   | GGML                                                                                                           |                                                                |
| -------- | ------- | ----- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| *small*  | 488 MB  | 11.83 | [Deskargatu](https://huggingface.co/xezpeleta/whisper-small-eu/resolve/main/ggml-small.eu.bin?download=true)   | [Webgunea](https://huggingface.co/xezpeleta/whisper-small-eu)  |
| *medium* | 1.53 GB | 8.80  | [Deskargatu](https://huggingface.co/xezpeleta/whisper-medium-eu/resolve/main/ggml-medium.eu.bin?download=true) | [Webgunea](https://huggingface.co/xezpeleta/whisper-medium-eu) |
| *large*  | 3.1 GB  | 7.21  | [Deskargatu](https://huggingface.co/xezpeleta/whisper-large-eu/resolve/main/ggml-large.eu.bin?download=true)   | [Webgunea](https://huggingface.co/xezpeleta/whisper-large-eu)  |

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

Deskargatu euskarazko eredua `models` direktoriora :(*medium* eredua erabiltzea gomendatzen da)

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

## Zeintzuk dira detektatutako arazo nagusiak?

### Euskalkiak eta aldaerak

Emaitza txukunenak euskara batuan lortzen dira.

### Haluzinazioak

*Whisper* tresnak batzuetan *haluzinazioak* ditu, bereziki audio hasiera eta amaierako isiluneetan.
