# gpt2_wp_medium

This model is a fine-tuned version of [gpt2-medium](https://huggingface.co/gpt2-medium) on the writingPrompts dataset.
It achieves the following results on the evaluation set:
- Loss: 2.9492

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 5e-05
- train_batch_size: 2
- eval_batch_size: 2
- seed: 42
- distributed_type: multi-GPU
- num_devices: 8
- gradient_accumulation_steps: 4
- total_train_batch_size: 64
- total_eval_batch_size: 16
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: linear
- num_epochs: 3.0

### Framework versions

- Transformers 4.12.5
- Pytorch 1.7.1+cu110
- Datasets 1.12.1
- Tokenizers 0.10.1
