# On Decoding Strategies for Neural Text Generators

## Metrics
The following table contains metrics and the corresponding framework used in our work.

| Metric        | Framework                           |
| ------------- | ----------------------------------- |
| BLEU          | https://github.com/mjpost/sacrebleu |
| METEOR        | https://github.com/cmu-mtlab/meteor |
| COMET         | https://github.com/Unbabel/COMET    |
| ROUGE         | https://github.com/google-research/google-research/tree/master/rouge  |
| BLEURT        | https://github.com/google-research/bleurt  |

The code for the `Ent-n`, `Dist-n`, and `n-gram diversity` can be found in `src/ngram_div.py`. A script to calculate repetition can be found in `src/repetition.py`. The latter is slightly modified version of the one provided by https://github.com/ari-holtzman/degen.

## Human Evaluation
The human ratings can be found in `data/human_eval`
## Models & Datasets
We use the [Hugging Face](https://huggingface.co/) framework to train models and to generate prompts from the model instances.

### Abstractive Summarization
The large version of the BART can be loaded like this:
```python
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
```
The [CNN/Daylimail](https://github.com/abisee/cnn-dailymail) dataset can also be accessed via the Hugging Face API:
```python
from datasets import load_dataset
dataset = load_dataset("cnn_dailymail", '3.0.0')
```
### Machine Translation
For each language pair the corresponding models can be loaded with the following commands:
```python
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/wmt19-en-de")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/wmt19-de-en")
```

For each language pair there is a directory in `data/datasets/wmt` containing source sentences and reference translations. The data is part of the test set of the [Newstest19 Dataset](http://www.statmt.org/wmt19/metrics-task.html).

### Dialogue
The DialoGPT model can be accesed in huggingface using the following line of code:
```python
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
```
The dataset on which we performed our experiments can be found in the `data/datasets/dialogue` folder. The file `dialogue.src` contains dialogue turns and `dialogue.ref` contains reference responses. This is a processed version of the `small` version of the dataset that can be downloaded using scripts from the [DialoGPT repository](https://github.com/microsoft/DialoGPT).

### Story Generation
#### Preprocessing
The preprocessing script can be found in `src/preproc_wp.py`. Download the [writingPrompts dataset](https://dl.fbaipublicfiles.com/fairseq/data/writingPrompts.tar.gz) and unzip the .tar into  the `data/datasets` folder. Then run `preproc_wp.py`.

The script creates for each of the train/test/valid splits a `<split>.comb.txt` file that contains one prompt-story pair per line.


#### Fine-Tuning
The finetuning script is located at `src/run_clm.py`. One can specify the model instance to be finetuned via the `--model_name_or_path` argument. We fine-tune an instance of `"gpt2"` and `"gpt2-medium"` each. The training and validation files can be passed in via the `--train_file` and `--validation_file` arguments. For a full overview of all available training args see the [Hugging Face Documentation](https://huggingface.co/docs/transformers/main_classes/trainer#transformers.TrainingArguments).

The trained model instance can then be loaded into Hugging Face by passing the path to the saved model instance to the `from_pretrained` method.

The hyperparamters used for fine-tuning can be found in `hyperparamets.md`. Note that the same hyperparamaters are used for both Story Generation and Unconditional Language Generation tasks. 

### Unconditional Language Generation
#### Preprocessing
The preprocessing script can be found in `src/preproc_wiki.py`. Download the raw version of [WikiText 103](https://blog.einstein.ai/the-wikitext-long-term-dependency-language-modeling-dataset/#download) Dataset and unzip into  the `data/datasets` folder. Then run `preproc_wiki.py`.

The script creates for each of the train/test/valid splits a `wiki.<split>.processed.txt` file that contains one trainings example per line.


#### Fine-Tuning
Fine-tuning is done as for the Story Generation task.

## Generation
All texts in our work are generated using Hugging Face's `generate` method called on a model instance initialized via the `from_pretrained` method. All generation settings such as `num_beams`, `max_length`, `top_k`, `top_p` etc can be passed as parameters to the `generate` method. Note that most models come with default generation parameters. By passing no parameters, `generate` will fall back to the default parameters. Be sure to overwrite all parameters related to decoding to ensure comparability across models. For more details see the [Hugging Face Documentation](https://huggingface.co/docs/transformers/v4.14.1/en/main_classes/model#transformers.generation_utils.GenerationMixin.generate).

#### MBR decoding
The MBR decoding framework requires to obtain multiple ancestral samples from the model. This can be achieved using the `generate` method and setting the `num_return_sequences` argument to the desired number. One can also include outputs of other decoding methods into the set of candidates. To then perform the actual minimum risk decoding we use the following framework: https://github.com/Roxot/mbr-nmt
