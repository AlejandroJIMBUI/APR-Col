import pickle

from character_engineering import mapeos_categorias, scaler
from model_trainig import *

# Guardar el LabelEncoder
with open('models/label_encoder_departamento.pkl', 'wb') as f:
    pickle.dump(mapeos_categorias, f)
    
# Guardar el Scaler
with open('models/minmax_scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
    
# Guardar Modelos

# Guardar el modelo de Random Forest
with open('models/modelo_presion_atmosferica_RandomForest.pkl', 'wb') as f:
    pickle.dump(rf_model, f)
    
# Guardar el modelo de Decision Tree
with open('models/modelo_presion_atmosferica_DecisionTree.pkl', 'wb') as f:
    pickle.dump(dt_model, f)
    
# Guardar el modelo de Decision Tree
with open('models/modelo_presion_atmosferica_XGBoost.pkl', 'wb') as f:
    pickle.dump(xgb_model, f)
    
"""
This code is written by: David Velásquez    
Contact: davisitovelasquez06@gmail.com
"""