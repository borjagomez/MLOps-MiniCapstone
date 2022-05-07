import sys
sys.path.insert(1, './app')

from fastapi import FastAPI, status, HTTPException

import logging
from logging.config import dictConfig
from log_config import log_config # this is your local file

dictConfig(log_config)
logger = logging.getLogger("minicapstone") # should be this name unless you change it in log_config.py

app = FastAPI()

@app.get('/healthcheck', status_code=status.HTTP_200_OK)
def perform_healthcheck():
    logger.info('Healthcheck ok')
    return {'healthcheck': 'Ok'}

@app.get('/hello', status_code=status.HTTP_200_OK)
def hello_world():
    logger.info('Hello World')
    return {'message': 'Hello World 2!'}
