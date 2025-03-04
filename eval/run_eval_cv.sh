#! /usr/bin/env bash

python3 evaluate_on_hf_dataset_cv.py \
--is_public_repo True \
--hf_model xezpeleta/whisper-tiny-eu \
--language eu \
--dataset "mozilla-foundation/common_voice_17_0" \
--config eu \
--split test \
--device 0 \
--batch_size 16 \
--output_dir predictions \
--streaming True \
--is_common_voice True
