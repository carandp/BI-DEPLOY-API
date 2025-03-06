from typing import Optional
from fastapi import FastAPI
import pandas as pd

from DataModel import DataModel
from PredictionModel import Model

app = FastAPI()

@app.post("/predict")
def make_predictions(dataModel: DataModel):
    df = pd.DataFrame(dataModel.dict(), columns=dataModel.dict().keys(), index=[0])
    df.columns = dataModel.columns()
    model = Model()
    result = model.make_predictions(df)
    return result