# EuroCon: Benchmarking Parliament Deliberation for Political Consensus Finding

<p align="center">
    <a href="https://huggingface.co/datasets/enrico956/EuroCon">
        <img alt="Build" src="https://img.shields.io/badge/🤗 Dataset-EuroCon-yellow">
    </a>
</p>

This repository is the official implementation of **EuroCon**.

## Requirements

This code has been tested on Ubuntu 20.04 with Python 3.10.

Clone the source code from GitHub:

```bash
git clone https://github.com/enrico956/EuroCon.git
cd EuroCon
```

We recommend using [Miniconda](https://docs.conda.io/en/latest/miniconda.html) and setting up an environment:

```bash
conda create -y --name eurocon python=3.10
conda activate eurocon
export PYTHONPATH=$(pwd)
```

Then install the required packages:

```bash
pip install -r requirements.txt
```

This will automatically setup all dependencies.

## Parameters

We provide a detailed introduction of every argument settings in our `config.py`.

- `--env_name` (str): Environment type (`EuroCon` by default)
- `--task_setting` (str): Task type - `seat_apportionment`/`rawlsianism`/`utilitarianism`
- `--model_name_or_path` (str): LLM path/name (`Qwen/Qwen2.5-32B-Instruct`)
- `--device` (str): GPU device (`cuda:0`)
- `--multi_gpu` (flag): Enable multi-GPU mode
- `--top_p` (float): Generation confidence threshold (0.95)
- `--voting_threshold_setting` (str): Voting system - `simple_majority`/`2_3_majority`/`veto_power`/`none`
- `--party_num` (int): Political groups count (2/4/6)
- `--eval_topic` (str): Evaluation topic (see `task_infos.py`)
- `--max_new_tokens` (int): Max generation length (512)
- `--temperature` (float): Output randomness (0.7)
- `--seed` (int): Random seed (42)

We also have an auto-derived parameter: `model_name` = last path component of `model_name_or_path`


## Datasets

We provide two types of datasets: `task_datas` and `topic_datas` in our benchmark, which are placed in the `datas` folder as the following structure:

```txt
datas
├── building_tasks.py
├── task_datas
│   ├── 2
│   │   ├── agriculture.json
│   │   ├── budget.json
│   │   ├── budgetary control.json
│   │   ├── civil liberties, justice & home affairs.json
│   │   ├── constitutional and inter-institutional affairs.json
│   │   ├── culture & education.json
│   │   ├── development.json
│   │   ├── economic & monetary affairs.json
│   │   ├── employment & social affairs.json
│   │   ├── environment & public health.json
│   │   ├── fisheries.json
│   │   ├── foreign & security policy.json
│   │   ├── gender equality.json
│   │   ├── industry, research & energy.json
│   │   ├── internal market & consumer protection.json
│   │   ├── international trade.json
│   │   ├── legal affairs.json
│   │   ├── regional development.json
│   │   └── transport & tourism.json
│   ├── 4
│   │   ├── agriculture.json
│   │   ├── budget.json
│   │   ├── budgetary control.json
│   │   ├── civil liberties, justice & home affairs.json
│   │   ├── constitutional and inter-institutional affairs.json
│   │   ├── culture & education.json
│   │   ├── development.json
│   │   ├── economic & monetary affairs.json
│   │   ├── employment & social affairs.json
│   │   ├── environment & public health.json
│   │   ├── fisheries.json
│   │   ├── foreign & security policy.json
│   │   ├── gender equality.json
│   │   ├── industry, research & energy.json
│   │   ├── internal market & consumer protection.json
│   │   ├── international trade.json
│   │   ├── legal affairs.json
│   │   ├── regional development.json
│   │   └── transport & tourism.json
│   └── 6
│       ├── agriculture.json
│       ├── budget.json
│       ├── budgetary control.json
│       ├── civil liberties, justice & home affairs.json
│       ├── constitutional and inter-institutional affairs.json
│       ├── culture & education.json
│       ├── development.json
│       ├── economic & monetary affairs.json
│       ├── employment & social affairs.json
│       ├── environment & public health.json
│       ├── fisheries.json
│       ├── foreign & security policy.json
│       ├── gender equality.json
│       ├── industry, research & energy.json
│       ├── internal market & consumer protection.json
│       ├── international trade.json
│       ├── legal affairs.json
│       ├── regional development.json
│       └── transport & tourism.json
├── task_infos.py
└── topic_datas
    ├── agriculture.json
    ├── budget.json
    ├── budgetary control.json
    ├── civil liberties, justice & home affairs.json
    ├── constitutional and inter-institutional affairs.json
    ├── culture & education.json
    ├── development.json
    ├── economic & monetary affairs.json
    ├── employment & social affairs.json
    ├── environment & public health.json
    ├── fisheries.json
    ├── foreign & security policy.json
    ├── foreign and security policy.json
    ├── gender equality.json
    ├── industry, research & energy.json
    ├── internal market & consumer protection.json
    ├── international trade.json
    ├── legal affairs.json
    ├── regional development.json
    └── transport & tourism.json
```

Datas in `task_datas` is the evaluation data version for in the paper, the folder name number is the party num in the parliament setting, whereas those in `topic_datas` is the original datas.

In `task_infos.py`, you can get the detailed infomation of our *EuroCon* benchmark:

```python
topic_list = ['development', 'culture & education', 'agriculture', 'gender equality', 'regional development', 'constitutional and inter-institutional affairs', 'transport & tourism', 'legal affairs', 'employment & social affairs', 'industry, research & energy', 'fisheries', 'internal market & consumer protection', 'international trade', 'budget', 'environment & public health', 'economic & monetary affairs', 'civil liberties, justice & home affairs', 'foreign & security policy', 'budgetary control']

party_num_settings = ['2', '4', '6']

party_lists = {'9th_datas': ['EPP', 'SD', 'ECR', 'RENEW', 'GREEN_EFA', 'GUE_NGL', 'ID'],
               '8th_datas': ['EPP', 'SD', 'ECR', 'EFDD', 'GREEN_EFA', 'GUE_NGL', 'ALDE', 'ENF'],
               '7th_datas': ['EPP', 'EFD', 'SD', 'ALDE', 'ECR', 'GREEN_EFA', 'GUE_NGL']}
```

If you want to build a different task datas, you can run the `building_tasks.py` to regenerate the task datas from topic datas in random parliament settings, including the party number, party seats and which party to have the veto power:

```shell
python datas/building_tasks.py
```

## Start Evaluation

If you want to start the *EuroCon* evals, you should first add your OpenAI API keys in the `openai_keys.py`:

```python
OPENAI_API_KEY = "<your keys>" 
OPENAI_BASE_URL = "<your api url>"
```

And run the following script to start the whole process:

```shell
bash scripts/run_all_tasks.sh 
```

