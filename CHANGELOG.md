
# 2025-02

Whisper models have been fine-tuned on a new dataset ([asierhv/composite_corpus_eu_v2.1](https://huggingface.co/datasets/asierhv/composite_corpus_eu_v2.1)), which is a combination of the following datasets: Mozilla Common Voice 18, OpenSLR 76, Basque Parliament. **Total training data: 675.98 hours**.

## There is room for improvement
Based on paper [HiTZ-AhoLab ASR System for the Albayzin Bilingual Basque-Spanish Speech
to Text Challenge](https://www.isca-archive.org/iberspeech_2024/herranz24_iberspeech.pdf), may be interesting to try to add a second language to the training data, in order to improve the performance of the models.

An alternative to improve the quality of these models could be to take into account the quality and the balance of the data. On the same time, we could try to data augmentation techniques, like Active Learning (picking the most uncertain/unreliable samples) or Synthetization (generating new samples).
