from PyQt6.QtWidgets import QApplication
import sys

from utils.model_manager import ModelManager
from views.prediction_app import PredictionApp



if __name__ == "__main__":
    app = QApplication(sys.argv)
    model_manager = ModelManager()
    if not model_manager.load_resources():
        print("Error al cargar los recursos necesarios")
        sys.exit(1)
    window = PredictionApp(model_manager)
    window.show()
    
    sys.exit(app.exec())