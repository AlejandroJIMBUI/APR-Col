import pickle
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, 
    QPushButton, QComboBox, QSlider, QTextEdit, QHBoxLayout, 
    QFileDialog, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator, QIntValidator, QPixmap, QFont
import os


class PredictionApp(QMainWindow):
    def __init__(self, model_manager):
        super().__init__()
        self.model_manager = model_manager
        
        self.setWindowTitle("APR - Col")
        self.setGeometry(100, 100, 900, 700)  # Ventana más ancha para el logo grande
        
        # Establecer estilo general mejorado
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel {
                font-weight: bold;
                color: #333;
                font-size: 12px;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                color: black;
                font-size: 12px;
            }
            QComboBox {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                color: black;  /* Texto negro en combobox */
                font-size: 12px;
            }
            QComboBox QAbstractItemView {
                color: black;  /* Texto negro en el dropdown */
                background-color: white;
                selection-background-color: #4CAF50;
                selection-color: white;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                font-family: Arial;
                color: black;
                font-size: 12px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: #ddd;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
                background: #4CAF50;
            }
        """)
        
        self.init_ui()
    
    def init_ui(self):
        # Widget principal y layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Panel izquierdo (formulario) - 45% del ancho
        form_panel = QWidget()
        form_layout = QVBoxLayout()
        form_panel.setLayout(form_layout)
        form_panel.setMaximumWidth(400)
        
        # Panel derecho (logo y salida) - 55% del ancho
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        
        # Sección de selección de modelo
        form_layout.addWidget(QLabel("Selección de Modelo:"))
        
        model_layout = QHBoxLayout()
        self.model_combo = QComboBox()
        self.model_combo.addItems(self.model_manager.models.keys())
        model_layout.addWidget(self.model_combo, 3)  # 3 partes de 4
        
        self.load_model_btn = QPushButton("Cargar Modelo")
        self.load_model_btn.clicked.connect(self.load_custom_model)
        model_layout.addWidget(self.load_model_btn, 1)  # 1 parte de 4
        form_layout.addLayout(model_layout)
        
        # Campos de entrada mejorados
        self.latitud = self.create_float_input("Latitud", form_layout)
        self.longitud = self.create_float_input("Longitud", form_layout)
        self.ano = self.create_int_input("Año", form_layout)
        
        # Slider para el mes con etiqueta de valor actual
        mes_layout = QHBoxLayout()
        mes_layout.addWidget(QLabel("Mes:"))
        self.mes_value_label = QLabel("1")
        self.mes_value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        mes_layout.addWidget(self.mes_value_label)
        form_layout.addLayout(mes_layout)
        
        self.mes = QSlider(Qt.Orientation.Horizontal)
        self.mes.setMinimum(1)
        self.mes.setMaximum(12)
        self.mes.setTickInterval(1)
        self.mes.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.mes.valueChanged.connect(lambda: self.mes_value_label.setText(str(self.mes.value())))
        form_layout.addWidget(self.mes)
        
        # Comboboxes con texto negro
        if self.model_manager.mapeos:
            self.nombre_estacion = self.create_dropdown("Estación", self.model_manager.mapeos['nombreestacion'], form_layout)
            self.departamento = self.create_dropdown("Departamento", self.model_manager.mapeos['departamento'], form_layout)
            self.municipio = self.create_dropdown("Municipio", self.model_manager.mapeos['municipio'], form_layout)
            self.zona = self.create_dropdown("Zona Hidro.", self.model_manager.mapeos['zonahidrografica'], form_layout)
        else:
            form_layout.addWidget(QLabel("Error: No se cargaron los mapeos de categorías"))
        
        # Botón de predicción más grande
        self.boton = QPushButton("PREDECIR PRESIÓN ATMOSFÉRICA")
        self.boton.clicked.connect(self.predict)
        form_layout.addWidget(self.boton)
        
        # Espaciador para empujar todo hacia arriba
        form_layout.addStretch()
        
        # Área del logo (derecha) - más grande y sin bordes
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Cargar logo si existe (ajusta el nombre del archivo)
        logo_path = "logo.png"  # Cambia esto por tu ruta de logo
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            # Escalar manteniendo aspecto (ajusta estos valores según tu logo)
            self.logo_label.setPixmap(pixmap.scaled(450, 450, 
                                                  Qt.AspectRatioMode.KeepAspectRatio,
                                                  Qt.TransformationMode.SmoothTransformation))
        else:
            # Placeholder si no hay logo
            self.logo_label.setText("LOGO APR-COL")
            self.logo_label.setStyleSheet("""
                font-size: 32px; 
                color: #4CAF50; 
                font-weight: bold;
                padding: 20px;
            """)
        
        right_layout.addWidget(self.logo_label, 0, Qt.AlignmentFlag.AlignHCenter)
        
        # Área de salida compacta
        output_layout = QVBoxLayout()
        self.salida = QTextEdit()
        self.salida.setReadOnly(True)
        self.salida.setMaximumHeight(120)
        output_layout.addWidget(self.salida)
        
        right_layout.addLayout(output_layout)
        right_layout.addStretch()
        
        # Añadir ambos paneles al layout principal
        main_layout.addWidget(form_panel)
        main_layout.addWidget(right_panel, 1)  # Expande el panel derecho
    
    def create_float_input(self, label, layout):
        row = QHBoxLayout()
        label_widget = QLabel(label + ":")
        label_widget.setMinimumWidth(100)  # Ancho fijo para alineación
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
        
        # Asegurar texto negro en el combobox
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
        """Permite cargar un modelo personalizado desde un archivo"""
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
            # Actualizar el modelo seleccionado
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