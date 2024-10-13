
# Whisper euskaraz

## Zer da Whisper ?

**_Whisper_** ahots errekonozimendurako adimen artifizialeko tresna da. *OpenAI* enpresak 2022 urtean argitaratu zuen *software libre* gisa (MIT lizentzipean).

## Euskarazko audioak transkribatzeko gai da?

*OpenAI*k argitaratutako ereduak emaitza nahiko kaxkarrak eskeintzen dizkigu euskarazko audioetan.

Alabaina, [Mozilla Common Voice](https://commonvoice.mozilla.org) proiektuari esker, jatorrizko ereduak trebatzea posible da, emaitza txukunagoak lortzeko.

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

Deskargatu euskarazko eredua `models` direktoriora:

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
