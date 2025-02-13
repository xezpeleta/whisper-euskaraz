
# 2025-02

Whisper models have been fine-tuned on a new dataset (`asierhv/composite_corpus_eu_v2.1`), which is a combination of the following datasets: Mozilla Common Voice 18, OpenSLR 76, Basque Parliament. **Total training data: 675.98 hours**.

- Pening: `whisper-tiny-eu`
- Updated `whisper-small-eu` model, **WER: 8.33** (before: 11.83).
- Updated `whisper-medium-eu` model, **WER: 7.97** (before: 8.80).
- Pending: `whisper-large-v3-eu`

These evaluations have been done using the split `test` of the dataset `Mozilla Common Voice 17.0`, in order to compare the results with the previous evaluations. The evaluations on the mixed dataset are not so good: 10.88 on small, 9.98 on medium.

## There is room for improvement
An alternative to improve the quality of these models could be to take into account the quality and the balance of the data. On the same time, we could try to data augmentation techniques, like Active Learning (picking the most uncertain/unreliable samples) or Synthetization (generating new samples).