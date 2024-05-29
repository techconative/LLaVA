# Welcome to the LLaVA DSL Gen Project Wiki

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [FAQ](#faq)

## Introduction
Welcome to the LLaVA DSL Gen Project! This project is designed to demonstrate how to install and navigate through this repository.

## Installation

### Step-by-Step LLaVA Installation Guide from the Github Repository

1. **Clone this repository and navigate to the LLaVA folder:**
    ```shell
    git clone https://github.com/haotian-liu/LLaVA.git
    cd LLaVA
    ```

2. **Install Package:**
    ```shell
    conda create -n llava python=3.10 -y
    conda activate llava
    pip install --upgrade pip  # enable PEP 660 support
    pip install -e .
    ```

3. **Install additional packages for training cases:**
    ```shell
    pip install -e ".[train]"
    pip install flash-attn --no-build-isolation
    ```

_For the purpose of running the current codes use the llava_new venev._

### Finetuning Guide
To start finetuning, run the _LLaVA/scripts/v1_5/finetune_task_lora.sh_ with the desired hyperparameter settings. 

### Data Preperation Guide
In addition to existing steps, the current repository also offers additional feature to split your data into train_eval_test split according to your desired split ratio. Follow the below steps for the same.

1. _LLaVA_InitialJson.py_ will prepare your initial custom data inot the desired LLaVA dataset format and return a .json file useful for the next steps.
   ```shell
   Syntax: python file_name.py --input_folder_with_gui_and_png_files --output_folder_to_store_json_file
   ```

2. _LLaVA_dataSplit.py_ will split your data intp the required train_eval_test split. Default value will be 80_10_10.
   ```shell
   Syntax: python LLaVA_dataSpit.py --path_to_input_folder_containing_data_and_json_file --output_folder_to_save_the_splitted_dataset
   ```
