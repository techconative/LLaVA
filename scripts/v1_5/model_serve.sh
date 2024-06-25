# start the controller server
python -m llava.serve.controller --host 0.0.0.0 --port 10000 &
sleep 10

# start the gradio ui server
# python -m llava.serve.gradio_web_server --host 0.0.0.0 --controller http://localhost:10000 --model-list-mode reload &
# sleep 10

# model worker to host the base model
# python -m llava.serve.model_worker --host 0.0.0.0 --controller http://localhost:10000 --port 40000 --worker http://localhost:40000 --model-path liuhaotian/llava-v1.5-7b 

# model worker to host the fine tuned model
python -m llava.serve.model_worker --host 0.0.0.0 --controller http://localhost:10000 --port 40000 --worker http://localhost:40000 --model-path ${PWD}/LLaVA/checkpoints/llava-v1.5-7b-task-lora --model-base liuhaotian/llava-v1.5-7b  
