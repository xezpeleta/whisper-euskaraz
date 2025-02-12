
# 2025-02

Whisper models have been fine-tuned on a new dataset (`asierhv/composite_corpus_eu_v2.1`), which is a combination of the following datasets: Mozilla Common Voice 18, OpenSLR 76, Basque Parliament. **Total training data: 675.98 hours**.

- Updated `whisper-small-eu` model, WER: 10.88 (before: 11.83).
- Pending: `whisper-medium-eu` and `whisper-large-eu` models.

As we can see, the WER improvement in small model is not very significant. However, the new dataset is more diverse and contains more data, which should help to improve the quality of the models. I hope to see more significant improvements in medium and large models, as they tolerate more data.

An alternative to improve the quality of tiny and small models could be to take into account the quality and the balance of the data. On the same time, we could try to data augmentation techniques, like Active Learning (picking the most uncertain/unreliable samples) or Synthetization (generating new samples).