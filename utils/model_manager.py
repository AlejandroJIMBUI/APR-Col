import os
import pickle

class ModelManager:
    """Clase para manejar la carga y gestión de modelos"""
    def __init__(self):
        self.models = {}
        self.current_model = None
        self.scaler = None
        self.mapeos = None
        
    def load_resources(self, models_dir='models'):
        """Carga todos los recursos necesarios desde el directorio especificado"""
        try:
            # Cargar mapeos de categorías
            with open(os.path.join(models_dir, 'label_encoder_departamento.pkl'), 'rb') as f:
                self.mapeos = pickle.load(f)
            
            # Cargar scaler
            with open(os.path.join(models_dir, 'minmax_scaler.pkl'), 'rb') as f:
                self.scaler = pickle.load(f)
            
            # Cargar todos los modelos disponibles
            model_files = [
                'modelo_presion_atmosferica_DecisionTree.pkl',
                'modelo_presion_atmosferica_RandomForest.pkl',
                'modelo_presion_atmosferica_XGBoost.pkl'
            ]
            
            for model_file in model_files:
                model_path = os.path.join(models_dir, model_file)
                if os.path.exists(model_path):
                    with open(model_path, 'rb') as f:
                        model_name = os.path.splitext(model_file)[0]
                        self.models[model_name] = pickle.load(f)
            
            # Establecer el primer modelo como predeterminado
            if self.models:
                self.current_model = next(iter(self.models.values()))
                
            return True
        except Exception as e:
            print(f"Error al cargar recursos: {str(e)}")
            return False
    
    def predict(self, latitud, longitud, ano, mes, nombreestacion, departamento, municipio, zonahidrografica):
        """Realiza una predicción usando el modelo actual"""
        if not self.current_model or not self.scaler:
            raise ValueError("Modelo o scaler no cargado")
            
        # Solo escalamos las variables numéricas que se escalaron originalmente
        datos_numericos = [[latitud, longitud]]
        datos_escalados = self.scaler.transform(datos_numericos)[0]

        # Añadimos año y mes sin escalar + variables categóricas codificadas
        entrada = list(datos_escalados) + [ano, mes, nombreestacion, departamento, municipio, zonahidrografica]

        return self.current_model.predict([entrada])[0]