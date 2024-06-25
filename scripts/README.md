# 🌋 LLaVA: Large Language and Vision Assistant

*Visual instruction tuning towards large language and vision models with GPT-4 level capabilities.*

## Contents
- [Install](#install)
- [CustomData](#customdata)
- [Finetune](#finetune)
- [Serve](#serve)

## Install

If you are not using Linux, do *NOT* proceed, see instructions for [macOS](https://github.com/haotian-liu/LLaVA/blob/main/docs/macOS.md) and [Windows](https://github.com/haotian-liu/LLaVA/blob/main/docs/Windows.md).

1. Clone this repository and navigate to LLaVA folder
```bash
git clone https://github.com/haotian-liu/LLaVA.git
cd LLaVA
```

2. Install Package
```Shell
python -m venv venv
source venv/bin/activate
pip install --upgrade pip  # enable PEP 660 support
pip install -e .
pip install -e ".[train]"
pip install flash-attn --no-build-isolation
```

## CustomData

If you want to prepare the dataset for finetuning the model. Follow the instructions below:
```Shell
python data_prep/data_prep.py data_prep/Sketch2Code_og/data data_prep/Sketch2Code_og
python data_prep/data_split.py data_prep/Sketch2Code_og/ data_prep/split_data
```

## Finetune

To finetune the model with the custom dataset, execute the script below:
```bash
chmod +x scripts/v1_5/finetune_task_lora.sh
scripts/v1_5/finetune_task_lora.sh
```

## Serve

To serve the fine tuned model, execute the scripts below: 
```bash
chmod +x scripts/v1_5/model_serve.sh
scripts/v1_5/model_serve.sh
```
```bash
chmod +x scripts/v1_5/fast_api_host.sh
scripts/v1_5/fast_api_host.sh
```

You should be able to access the model at "http://localhost:8000/docs" using FastAPI-SwaggerUI.
For curl command:
```bash
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@<filepath>;type=image/png'
```



