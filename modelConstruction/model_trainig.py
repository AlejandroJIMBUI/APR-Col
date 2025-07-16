import numpy as np

#Evaluar metricas
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error

#Modelos para regresion
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split

from character_engineering import df

x=df.drop(["valorobservado","fechaobservacion"],axis=1)
y=df['valorobservado']

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3,random_state=42)


# Modelo de regresion Random Forest

rf_model=RandomForestRegressor(n_estimators=100, #Numero de arboles en el bosque
                               random_state=42, #Semilla para reproducibilidad
                               max_depth=10, #Profundidad maxima de arboles
                               min_samples_split=5 #Minimo numero de muestras para dividir un nodo
                               )

rf_model.fit(x_train,y_train)

y_pred=rf_model.predict(x_test)
y_train_pred=rf_model.predict(x_train)

def train_val(y_train, y_train_pred, y_test, y_pred):
    scores = {
        "_train": {
            "R2": r2_score(y_train, y_train_pred),
            "mae": mean_absolute_error(y_train, y_train_pred),
            "mse": mean_squared_error(y_train, y_train_pred),
            "rmse": np.sqrt(mean_squared_error(y_train, y_train_pred))
        },
        "_test": {
            "R2": r2_score(y_test, y_pred),
            "mae": mean_absolute_error(y_test, y_pred),
            "mse": mean_squared_error(y_test, y_pred),
            "rmse": np.sqrt(mean_squared_error(y_test, y_pred))
        }
    }
    return scores

mlr_score = train_val(y_train, y_train_pred, y_test, y_pred)
print(mlr_score)


# Modelo de regresion Decision Tree

dt_model=DecisionTreeRegressor()    

dt_model.fit(x_train,y_train)

y_pred=dt_model.predict(x_test)
y_train_pred=dt_model.predict(x_train)

mlr_score = train_val(y_train, y_train_pred, y_test, y_pred)
print(mlr_score)


# Modelo de regresion XGBoost

xgb_model = XGBRegressor(
    n_estimators=1000,      # Número de árboles (boosting rounds)
    learning_rate=0.05,     # Tasa de aprendizaje (eta)
    max_depth=6,            # Profundidad máxima de los árboles
    subsample=0.8,          # Porcentaje de muestras usadas en cada árbol
    colsample_bytree=0.8,   # Porcentaje de características usadas en cada árbol
    random_state=42)

xgb_model.fit(x_train,y_train)

y_pred=xgb_model.predict(x_test)
y_train_pred=xgb_model.predict(x_train)

mlr_score = train_val(y_train, y_train_pred, y_test, y_pred)
print(mlr_score)

"""
This code is written by: David Velásquez    
Contact: davisitovelasquez06@gmail.com
"""