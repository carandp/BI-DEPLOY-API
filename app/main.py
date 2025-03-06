from typing import Optional
from fastapi import FastAPI
import pandas as pd

from DataModel import DataModel
# from PredictionModel import Model

from joblib import load
from pipeline import CustomRegressionPipeline

app = FastAPI()

@app.post("/predict")
def make_predictions(dataModel: DataModel):
    df = pd.DataFrame(dataModel.dict(), columns=dataModel.dict().keys(), index=[0])
    df.columns = dataModel.columns()
    
    print(df.head())
    
    model = load("model.joblib")
    result = model.predict(df)
    
    # Convert the result to a serializable format
    result_list = result.tolist() if hasattr(result, 'tolist') else result
    
    return {"prediction": result_list}