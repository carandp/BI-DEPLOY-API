import os
from joblib import dump
import pandas as pd
from pipeline import CustomRegressionPipeline

def dump_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_location = os.path.join(base_dir,'data', 'Regresion_train_data.csv')
    
    # Carga el dataset de estrellas
    stars_df = pd.read_csv(db_location, sep=',', encoding="ISO-8859-1")

    # Crea un objeto de la clase CustomRegressionPipeline y entrena el modelo
    model_pipeline = CustomRegressionPipeline()
    model_pipeline.fit(stars_df)
    
    # Exporta el modelo entrenado en un archivo .joblib
    dump(model_pipeline, "app/model.joblib")
    print("Modelo exportado como model.joblib a la carpeta de app\n")

dump_model()