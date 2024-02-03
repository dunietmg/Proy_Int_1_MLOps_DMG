
from typing import Union, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
from dateutil import parser
import pyarrow.parquet as pq
import os
import string
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


# Creacion de una aplicacion FastApi

app = FastAPI()

# App de prueba (ejemplo)
@app.get("/")
def read_root():
    return {"Hola": "Mundo!"}
