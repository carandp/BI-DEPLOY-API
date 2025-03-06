import numpy as np
import pandas as pd

from joblib import dump, load

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

class CustomRegressionPipeline(BaseEstimator, RegressorMixin):
    # Inicia el pipeline con los pasos necesarios
    def __init__(self):
        self.pipeline = Pipeline([
            # Selecciona las columnas categóricas y las vectoriza con OneHotEncoder
            ('onehot', ColumnTransformer(
                transformers=[('onehot', OneHotEncoder(), ['class'])],
                remainder='passthrough')),
            # Escala las columnas numéricas con StandardScaler y añade polinomios de grado 2
            ('poly', Pipeline([
                ('scaler', StandardScaler()),
                ('poly', PolynomialFeatures(degree=2, include_bias=False))
            ])),
            # Crea un modelo de regresión lineal
            ('regressor', LinearRegression())
        ])
        
        # Indica si el modelo ha sido entrenado
        self.is_fitted_ = False
    
    # Limpia los datos y los prepara para el entrenamiento
    def _clean_data(self, df):
        df_clean = df.copy()
        
        if 'redshift' not in df_clean.columns:
            print("The 'redshift' column is missing.")
            return None
        
        num_features = ["ra", "dec", "u", "r", "field", "mjd", "rowv", "colv"]
        
        # Elimina los outliers
        for col in num_features:
            q1 = df_clean[col].quantile(0.25)
            q3 = df_clean[col].quantile(0.75)
            riq = q3 - q1
            lower_bound = q1 - 3 * riq
            upper_bound = q3 + 3 * riq
            df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]
        
        # Elimina duplicados
        df_clean = df_clean.drop_duplicates()
        
        # Corrige los valores atípicos en la variable categórica 'class'
        df_clean["class"] = df_clean["class"].replace({"S": "STAR", "G": "GALAXY", "Q": "QSO"})
        df_clean = df_clean[df_clean["class"].isin(["STAR", "GALAXY", "QSO"])]
        
        # Quita los registros que tengan un puntaje menor a 0.5 y que no estén limpios
        df_clean = df_clean[df_clean["score"] >= 0.5]
        df_clean = df_clean[df_clean["clean"] != 0]
        
        return df_clean
    
    # Limpia los datos y los prepara para la predicción
    def _clean_data_predict(self, df):
        df_clean = df.copy()
        
        # Corrige los valores atípicos en la variable categórica 'class'
        df_clean["class"] = df_clean["class"].replace({"S": "STAR", "G": "GALAXY", "Q": "QSO"})
        df_clean = df_clean[df_clean["class"].isin(["STAR", "GALAXY", "QSO"])]
        
        return df_clean

    # Entrena el modelo
    def fit(self, X, y=None):
        df = X.copy()
        
        # Limpia los datos con la función previa
        df_clean = self._clean_data(df)
        
        # Obtiene la variable objetivo y las características
        y_clean = df_clean['redshift']
        feature_cols = ["ra", "dec", "u", "r", "field", "class", "mjd", "rowv", "colv"]
        X_features = df_clean[feature_cols]
        
        # Divide los datos en entrenamiento y prueba de 70% y 30% respectivamente
        X_train, X_test, y_train, y_test = train_test_split(
            X_features, y_clean, test_size=0.3, random_state=1
        )
        
        # Entrena el modelo
        self.pipeline.fit(X_train, y_train)
        
        # Predice los valores de entrenamiento y prueba
        y_train_pred = self.pipeline.predict(X_train)
        y_test_pred  = self.pipeline.predict(X_test)
        
        # Muestra estadísticas de prueba del modelo
        print("====== Model Performance ======")
        print("Train MAE:", mean_absolute_error(y_train, y_train_pred))
        print("Test MAE:", mean_absolute_error(y_test, y_test_pred))
        print("Train RMSE:", np.sqrt(mean_squared_error(y_train, y_train_pred)))
        print("Test RMSE:", np.sqrt(mean_squared_error(y_test, y_test_pred)))
        print("Train R²:", r2_score(y_train, y_train_pred))
        print("Test R²:", r2_score(y_test, y_test_pred))
        print("===============================\n")
        
        # Guarda el modelo entrenado y actualiza el estado de is_fitted_
        self.pipeline.fit(X_features, y_clean)
        self.is_fitted_ = True
        return self

    # Predice los valores de la variable objetivo con el modelo entrenado
    def predict(self, X):
        
        # Verifica si el modelo ha sido entrenado
        if not self.is_fitted_:
            print("You must fit the model before predicting.")
            return None
        
        df = X.copy()
        feature_cols = ["ra", "dec", "u", "r", "field", "class", "mjd", "rowv", "colv"]
        
        # Limpia los datos con la función previa para predicción 
        clean_df = self._clean_data_predict(df)
        
        # Filtra y selecciona las columnas usadas para entrenar el modelo
        X_features = clean_df[feature_cols]
        
        # Predice el valor de la variable objetivo
        return self.pipeline.predict(X_features)