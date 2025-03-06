from joblib import load
import os

class Model:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), "pipeline/model_pipeline.joblib")
        self.model = load(model_path)
    
    def make_predictions(self, data):
        result = self.model.predict(data)
        return result