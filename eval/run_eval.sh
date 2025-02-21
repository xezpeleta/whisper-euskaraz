#! /bin/bash

# Run evaluation script with the correct path
python3 evaluate_on_hf_dataset.py \
--is_public_repo True \
--hf_model xezpeleta/whisper-small-eu \
--language eu \
--dataset "asierhv/composite_corpus_eu_v2.1" \
--config "default" \
--split test_cv \
--device 0 \
--batch_size 16 \
--output_dir predictions \
--streaming True \
--is_common_voice False
