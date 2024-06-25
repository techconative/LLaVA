"""
model_name = "llava-v1.5-7b-task-lora"
model_worker_address: get it from fastapi post from controller server
code: 
controller_url = http://localhost:10000
    ret = requests.post(controller_url + "/get_worker_address",
            json={"model": model_name})
    worker_addr = ret.json()["address"]

accept image.png as input and process the image

Construct the payload
pload = {
        "model": model_name,
        "prompt": "",
        "temperature": float(temperature),
        "top_p": float(top_p),
        "max_new_tokens": min(int(max_new_tokens), 1536),
        "stop": state.sep if state.sep_style in [SeparatorStyle.SINGLE, SeparatorStyle.MPT] else state.sep2,
        "images": image,
    }

Get the response
response = requests.post(worker_addr + "/worker_generate_stream",
            headers=headers, json=pload, stream=True, timeout=10)
"""


# import the necessary libraries
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import requests
import base64
from io import BytesIO
from PIL import Image
import hashlib
import json
import time

app = FastAPI()

controller_url = "http://localhost:10000"
model_name = "llava-v1.5-7b-task-lora"

# Function to get the model worker address from controller API
def get_worker_address(model_name: str):
    try:
        response = requests.post(controller_url + "/get_worker_address", json={"model": model_name})
        response.raise_for_status()
        return response.json()["address"]

    except Exception as e:
        raise HTTPException(status_code=500, detail="Unable to fetch model worker address")

# Function to process the image
def process_image(image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

    # return hashlib.md5(image.tobytes()).hexdigest()

# Get the prediction
@app.post("/predict")
async def get_prediction(file: UploadFile = File(...)):
    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Invalid image type")

    try:
        image_data = await file.read()
        image = Image.open(BytesIO(image_data))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image content")

    encoded_image = process_image(image)
    worker_addr = get_worker_address(model_name)

    prompt_template = "A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions. USER: <image> ASSISTANT:"

    payload = {
        "model_name": model_name,
        "prompt": prompt_template,
        "temperature": 0.0,
        "top_p": 0.95,
        "max_new_tokens": 512,
        "stop": "</s>",
        "images": [encoded_image],
    }

    # get the response
    try:
        response = requests.post(
            worker_addr + "/worker_generate_stream",
            headers={"Content-Type": "application/json"},
            json=payload,
            stream=False,
            timeout=5
        )
        # response.raise_for_status()

        assistant_response = ""
        prompt_length = len(prompt_template)

        for chunk in response.iter_lines(decode_unicode=False, delimiter=b"\0"):
            if chunk:
                data = json.loads(chunk.decode())
                if data["error_code"] == 0:
                    output = data["text"][prompt_length:].strip()
                    assistant_response = output + "▌"
                else:
                    output = data["text"] + f" (error_code: {data['error_code']})"
                    assistant_response = output
                    break

        # Finalize the response
        response = assistant_response[:-1]  # Remove the last "▌"

        return JSONResponse(content={"response": response})

        return response.text
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)