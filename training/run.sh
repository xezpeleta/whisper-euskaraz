WANDB_PROJECT=whisper-euskaraz \
	python run_speech_recognition_seq2seq_streaming.py \
	--model_name_or_path="openai/whisper-medium" \
	--dataset_name="mozilla-foundation/common_voice_17_0" \
	--dataset_config_name="eu" \
	--language="basque" \
	--train_split_name="train+validation" \
	--eval_split_name="test" \
	--model_index_name="Whisper Small Basque" \
	--max_steps="5000" \
	--output_dir="./" \
	--per_device_train_batch_size="16" \
	--per_device_eval_batch_size="8" \
	--gradient_accumulation_steps="1" \
	--logging_steps="25" \
	--learning_rate="6.25e-6" \
	--warmup_steps="500" \
	--evaluation_strategy="steps" \
	--eval_steps="1000" \
	--save_strategy="steps" \
	--save_steps="1000" \
	--generation_max_length="225" \
	--length_column_name="input_length" \
	--max_duration_in_seconds="30" \
	--text_column_name="sentence" \
	--freeze_feature_encoder="False" \
	--report_to="tensorboard" \
	--metric_for_best_model="wer" \
	--greater_is_better="False" \
	--load_best_model_at_end \
	--gradient_checkpointing \
	--fp16 \
	--overwrite_output_dir \
	--resume_from_checkpoint="checkpoint-9000" \
	--do_train \
	--do_eval \
	--predict_with_generate \
	--do_normalize_eval \
	--streaming \
	--push_to_hub \
	--report_to "wandb" \
	--run_name "whisper-medium-eu"
