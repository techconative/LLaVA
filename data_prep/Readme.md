The python file LLaVA_InitialJson.py will make the json data in the customised required format for LLaVA model to work on.
The python file LLaVA_dataSplit.py will perform the data splitting.





Use the following command line prompt to runs the .py files to generate the data splits


python LLaVA_InitialJson.py ~/LLaVA/data_prep/Sketch2Code_og/data ~/LLaVA/data_prep/Sketch2Code_og

python LLaVA_dataSplit.py ~/LLaVA/data_prep/Sketch2Code_og/ ~/splitted_data_verify/


