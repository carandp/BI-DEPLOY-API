from typing import Optional
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import pandas as pd

from DataModel import DataModel
# from PredictionModel import Model

from joblib import load
from pipeline import CustomRegressionPipeline

app = FastAPI()

@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.post("/predict")
def make_predictions(dataModel: DataModel):
    df = pd.DataFrame(dataModel.dict(), columns=dataModel.dict().keys(), index=[0])
    df.columns = dataModel.columns()
    
    model = load("model.joblib")
    result = model.predict(df)
    
    return {"redshift": result.tolist()[0]}