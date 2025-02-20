#! /bin/bash

# Activate virtual environment
source /home/tknika/xezpeleta/whisper/.venv/bin/activate

# Change to the eval directory
cd "$(dirname "$0")"

# Ensure the output directory exists
mkdir -p predictions

# Run evaluation script with the correct path
python3 evaluate_on_hf_dataset.py \
--is_public_repo True \
--hf_model xezpeleta/whisper-base-eu \
--language eu \
--dataset "asierhv/composite_corpus_eu_v2.1" \
--config "default" \
--split test_cv \
--device 0 \
--batch_size 1 \
--output_dir predictions
