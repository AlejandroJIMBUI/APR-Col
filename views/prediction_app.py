import pickle
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, 
    QPushButton, QComboBox, QSlider, QTextEdit, QHBoxLayout, 
    QFileDialog, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator, QIntValidator, QPixmap, QIcon
import os


class PredictionApp(QMainWindow):
    def __init__(self, model_manager):
        super().__init__()
        self.model_manager = model_manager
        
        self.setWindowTitle("APR - Col")
        self.setGeometry(100, 100, 500, 300)  # Tamaño ajustado
        
        # Establecer icono de la ventana
        self.setWindowIcon(QIcon("resources/logo.ico"))  # Asegúrate de tener este archivo
        
        # Establecer estilo general mejorado
        self.setStyleSheet("""
            QMainWindow {
                background-color: #36454f;
            }
            QLabel {
                font-weight: bold;
                color: #93abc2;
                font-size: 12px;
            }
            QLineEdit {
                background-color: #708090;
                border: 1px solid #000000;
                border-radius: 4px;
                padding: 5px;
                color: black;
                font-size: 12px;
            }
            QComboBox {
                background-color: #708090;
                border: 1px solid #000000;
                border-radius: 4px;
                padding: 5px;
                color: black;
                font-size: 12px;
            }
            QComboBox QAbstractItemView {
                color: black;
                background-color: #708090;
                selection-background-color: #4CAF50;
                selection-color: #708090;
            }
            QTextEdit {
                background-color: #708090;
                border: 1px solid #000000;
                border-radius: 4px;
                padding: 8px;
                font-family: Arial;
                color: black;
                font-size: 12px;
            }
            QPushButton {
                background-color: #536878;
                color: #000000;
                border: 1px solid #000000;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #708090;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: #708090;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
                background: #93abc2;
            }
        """)
        
        self.init_ui()
    
    def init_ui(self):
        # Widget principal y layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Sección de selección de modelo
        main_layout.addWidget(QLabel("Modelo:"))
        
        model_layout = QHBoxLayout()
        self.model_combo = QComboBox()
        self.model_combo.addItems(self.model_manager.models.keys())
        model_layout.addWidget(self.model_combo, 3)
        
        self.load_model_btn = QPushButton("Cargar Modelo Externo")
        self.load_model_btn.clicked.connect(self.load_custom_model)
        model_layout.addWidget(self.load_model_btn, 1)
        main_layout.addLayout(model_layout)
        
        # Campos de entrada
        self.latitud = self.create_float_input("Latitud", main_layout)
        self.longitud = self.create_float_input("Longitud", main_layout)
        self.ano = self.create_int_input("Año", main_layout)
        
        # Slider para el mes con etiqueta de valor actual
        mes_layout = QHBoxLayout()
        mes_layout.addWidget(QLabel("Mes:"))
        self.mes_value_label = QLabel("1")
        self.mes_value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        mes_layout.addWidget(self.mes_value_label)
        main_layout.addLayout(mes_layout)
        
        self.mes = QSlider(Qt.Orientation.Horizontal)
        self.mes.setMinimum(1)
        self.mes.setMaximum(12)
        self.mes.setTickInterval(1)
        self.mes.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.mes.valueChanged.connect(lambda: self.mes_value_label.setText(str(self.mes.value())))
        main_layout.addWidget(self.mes)
        
        # Comboboxes
        if self.model_manager.mapeos:
            self.nombre_estacion = self.create_dropdown("Estación", self.model_manager.mapeos['nombreestacion'], main_layout)
            self.departamento = self.create_dropdown("Departamento", self.model_manager.mapeos['departamento'], main_layout)
            self.municipio = self.create_dropdown("Municipio", self.model_manager.mapeos['municipio'], main_layout)
            self.zona = self.create_dropdown("Zona Hidro.", self.model_manager.mapeos['zonahidrografica'], main_layout)
        else:
            main_layout.addWidget(QLabel("Error: No se cargaron los mapeos de categorías"))
        
        # Botón de predicción
        self.boton = QPushButton("HACER PREDICCIÓN")
        self.boton.clicked.connect(self.predict)
        main_layout.addWidget(self.boton)
        
        # Área de salida debajo del botón
        self.salida = QTextEdit()
        self.salida.setReadOnly(True)
        self.salida.setMinimumHeight(100)
        main_layout.addWidget(self.salida)
        
        # Espaciador para mantener todo arriba
        main_layout.addStretch()
    
    def create_float_input(self, label, layout):
        row = QHBoxLayout()
        label_widget = QLabel(label + ":")
        label_widget.setMinimumWidth(100)
        row.addWidget(label_widget)
        input_field = QLineEdit()
        validator = QDoubleValidator()
        input_field.setValidator(validator)
        row.addWidget(input_field)
        layout.addLayout(row)
        return input_field
    
    def create_int_input(self, label, layout):
        row = QHBoxLayout()
        label_widget = QLabel(label + ":")
        label_widget.setMinimumWidth(100)
        row.addWidget(label_widget)
        input_field = QLineEdit()
        validator = QIntValidator()
        input_field.setValidator(validator)
        row.addWidget(input_field)
        layout.addLayout(row)
        return input_field
    
    def create_dropdown(self, label, opciones, layout):
        row = QHBoxLayout()
        label_widget = QLabel(label + ":")
        label_widget.setMinimumWidth(100)
        row.addWidget(label_widget)
        combo = QComboBox()
        combo.addItems(opciones.keys())
        combo.setStyleSheet("""
            QComboBox {
                color: black;
            }
            QComboBox QAbstractItemView {
                color: black;
            }
        """)
        row.addWidget(combo)
        layout.addLayout(row)
        return combo
    
    def load_custom_model(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo de modelo", 
            "", "Pickle files (*.pkl);;All files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    model = pickle.load(f)
                    model_name = os.path.splitext(os.path.basename(file_path))[0]
                    self.model_manager.models[model_name] = model
                    self.model_combo.addItem(model_name)
                    self.model_combo.setCurrentText(model_name)
                    self.model_manager.current_model = model
                    self.salida.append(f"✓ Modelo {model_name} cargado exitosamente")
            except Exception as e:
                self.salida.append(f"✗ Error al cargar modelo: {str(e)}")
    
    def predict(self):
        try:
            selected_model = self.model_combo.currentText()
            self.model_manager.current_model = self.model_manager.models.get(selected_model)
            
            if not self.model_manager.current_model:
                raise ValueError("No se ha seleccionado un modelo válido")
            
            pred = self.model_manager.predict(
                float(self.latitud.text()),
                float(self.longitud.text()),
                int(self.ano.text()),
                self.mes.value(),
                self.model_manager.mapeos['nombreestacion'][self.nombre_estacion.currentText()],
                self.model_manager.mapeos['departamento'][self.departamento.currentText()],
                self.model_manager.mapeos['municipio'][self.municipio.currentText()],
                self.model_manager.mapeos['zonahidrografica'][self.zona.currentText()]
            )
            self.salida.setText(f"MODELO: {selected_model}\nPREDICCIÓN: {pred:.2f} hPa")
        except ValueError as e:
            self.salida.setText(f"✗ Error: Valores numéricos inválidos\n{str(e)}")
        except Exception as e:
            self.salida.setText(f"✗ Error inesperado:\n{str(e)}")