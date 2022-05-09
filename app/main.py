import sys
sys.path.insert(1, './app')

import os

from fastapi import FastAPI, status, UploadFile, File
from fastapi.responses import HTMLResponse
from keras.preprocessing import image
from keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import tensorflow as tf
import numpy as np

import logging
from logging.config import dictConfig
from log_config import log_config # this is your local file

from classes import _FINE_LABEL_NAMES

dictConfig(log_config)
logger = logging.getLogger("minicapstone") # should be this name unless you change it in log_config.py

tf.random.set_seed(42)

app = FastAPI()

model = load_model('./app/model/cifar100')

@app.get('/healthcheck', status_code=status.HTTP_200_OK)
def perform_healthcheck():
    logger.info('Healthcheck ok')
    return {'healthcheck': 'Ok'}

@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    filename = file.filename
    save_path = './app/images'
    completeName = os.path.join(save_path, filename)
    file1 = open(completeName, "w+b")
    file1.write(contents)
    file1.close()

    img = image.load_img(completeName, target_size=(32, 32))
    imageArray = image.img_to_array(img)
    imageArray = np.expand_dims(imageArray, axis=0)
    imageArray = preprocess_input(imageArray)
    imageArray = imageArray * 1.0 / 255

    predictions = model.predict(imageArray)
    result = _FINE_LABEL_NAMES[np.argmax(predictions, axis=1)[0]]

    return {"prediction": result}


@app.get("/")
async def main():
    content = """
<body>
<p>Upload your image</p>
<form action="/upload/" enctype="multipart/form-data" method="post">
<input name="file" type="file">
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
