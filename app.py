import json
import platform
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal

from ollama_helper import OllamaCommander
from os_info import get_os_info, format_os_info
from ollama_api import OllamaAPI


class OllamaAssistant(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Asistente de Comandos Ollama")
        self.setMinimumSize(460, 900)
        self.resize(460, 900)
        self.setWindowIcon(QtGui.QIcon())
        self.dataset = self.load_dataset()
        self.api = OllamaAPI()
        self.available_models = []
        self.dark_mode = False
        self.init_ui()
        self.load_system_specs()
        self.check_ollama_connection()

    def load_dataset(self):
        try:
            with open("dataset.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def init_ui(self):
        scroll_area = QtWidgets.QScrollArea()
        self.setCentralWidget(scroll_area)
        central_widget = QtWidgets.QWidget()
        scroll_area.setWidget(central_widget)
        scroll_area.setWidgetResizable(True)
        layout = QtWidgets.QVBoxLayout(central_widget)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        header = QtWidgets.QLabel("Asistente de Comandos Ollama")
        header.setObjectName("header")
        header.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(header)

        connection_layout = QtWidgets.QHBoxLayout()
        self.status_label = QtWidgets.QLabel("Estado: Conectando...")
        self.status_label.setObjectName("status")
        connection_layout.addWidget(self.status_label)
        connection_layout.addStretch(1)
        self.dark_mode_button = QtWidgets.QPushButton("🌙 Modo Oscuro")
        self.dark_mode_button.setMaximumWidth(120)
        self.dark_mode_button.clicked.connect(self.toggle_dark_mode)
        connection_layout.addWidget(self.dark_mode_button)
        self.reconnect_button = QtWidgets.QPushButton("Reconectar")
        self.reconnect_button.setMaximumWidth(100)
        self.reconnect_button.clicked.connect(self.check_ollama_connection)
        connection_layout.addWidget(self.reconnect_button)
        layout.addLayout(connection_layout)

        description = QtWidgets.QLabel(
            "Conecta con Ollama, selecciona un modelo y escribe tu prompt. "
            "La app ejecutará el comando directamente contra tu servidor Ollama local."
        )
        description.setWordWrap(True)
        layout.addWidget(description)

        self.spec_group = QtWidgets.QGroupBox("Especificaciones del OS / Entorno")
        spec_layout = QtWidgets.QVBoxLayout(self.spec_group)
        self.spec_text = QtWidgets.QPlainTextEdit()
        self.spec_text.setReadOnly(True)
        self.spec_text.setMinimumHeight(120)
        self.spec_text.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        spec_layout.addWidget(self.spec_text)

        self.refresh_button = QtWidgets.QPushButton("Actualizar desde PC")
        self.refresh_button.clicked.connect(self.load_system_specs)
        spec_layout.addWidget(self.refresh_button, alignment=QtCore.Qt.AlignRight)
        layout.addWidget(self.spec_group)

        self.preset_group = QtWidgets.QGroupBox("Prompts prediseñados")
        preset_layout = QtWidgets.QHBoxLayout(self.preset_group)
        self.preset_combo = QtWidgets.QComboBox()
        self.preset_combo.addItems([
            "Selecciona un preset...",
            "Explicar un concepto",
            "Generar un comando",
            "Traducir texto",
            "Resumir texto",
            "Corregir gramática"
        ])
        preset_layout.addWidget(self.preset_combo, 1)
        self.apply_preset_button = QtWidgets.QPushButton("Aplicar preset")
        self.apply_preset_button.setMaximumWidth(120)
        self.apply_preset_button.clicked.connect(self.apply_preset)
        preset_layout.addWidget(self.apply_preset_button)
        layout.addWidget(self.preset_group)

        self.os_group = QtWidgets.QGroupBox("Sistema Operativo")
        os_layout = QtWidgets.QHBoxLayout(self.os_group)
        os_layout.addWidget(QtWidgets.QLabel("OS:"))
        self.os_combo = QtWidgets.QComboBox()
        self.os_combo.addItems(["Automático", "Windows", "Linux", "macOS"])
        os_layout.addWidget(self.os_combo, 1)
        self.apply_os_button = QtWidgets.QPushButton("Aplicar OS al prompt")
        self.apply_os_button.setMaximumWidth(140)
        self.apply_os_button.clicked.connect(self.apply_os)
        os_layout.addWidget(self.apply_os_button)
        layout.addWidget(self.os_group)

        self.model_group = QtWidgets.QGroupBox("Modelo Ollama")
        model_layout = QtWidgets.QHBoxLayout(self.model_group)
        model_layout.addWidget(QtWidgets.QLabel("Modelo:"))
        self.model_combo = QtWidgets.QComboBox()
        self.model_combo.addItem("Cargando modelos...")
        model_layout.addWidget(self.model_combo, 1)
        self.refresh_models_button = QtWidgets.QPushButton("Refrescar")
        self.refresh_models_button.setMaximumWidth(80)
        self.refresh_models_button.clicked.connect(self.load_models)
        model_layout.addWidget(self.refresh_models_button)
        layout.addWidget(self.model_group)

        self.input_group = QtWidgets.QGroupBox("Tu Prompt")
        input_layout = QtWidgets.QVBoxLayout(self.input_group)
        self.prompt_input = QtWidgets.QPlainTextEdit()
        self.prompt_input.setPlaceholderText("Ejemplo: Explícame cómo archivar múltiples archivos en un solo comando usando zip en Windows.")
        self.prompt_input.setMinimumHeight(100)
        self.prompt_input.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        input_layout.addWidget(self.prompt_input)

        self.options_group = QtWidgets.QGroupBox("Opciones de respuesta")
        options_layout = QtWidgets.QGridLayout(self.options_group)
        options_layout.setSpacing(10)
        options_layout.addWidget(QtWidgets.QLabel("Temperatura:"), 0, 0)
        self.temperature_spin = QtWidgets.QDoubleSpinBox()
        self.temperature_spin.setRange(0.0, 1.0)
        self.temperature_spin.setSingleStep(0.05)
        self.temperature_spin.setValue(0.7)
        options_layout.addWidget(self.temperature_spin, 0, 1)

        options_layout.addWidget(QtWidgets.QLabel("Top-p:"), 0, 2)
        self.top_p_spin = QtWidgets.QDoubleSpinBox()
        self.top_p_spin.setRange(0.0, 1.0)
        self.top_p_spin.setSingleStep(0.05)
        self.top_p_spin.setValue(1.0)
        options_layout.addWidget(self.top_p_spin, 0, 3)

        options_layout.addWidget(QtWidgets.QLabel("Máx. tokens:"), 1, 0)
        self.max_tokens_spin = QtWidgets.QSpinBox()
        self.max_tokens_spin.setRange(1, 2048)
        self.max_tokens_spin.setValue(256)
        options_layout.addWidget(self.max_tokens_spin, 1, 1)

        options_layout.addWidget(QtWidgets.QLabel("Máx. caracteres:"), 1, 2)
        self.max_chars_spin = QtWidgets.QSpinBox()
        self.max_chars_spin.setRange(0, 5000)
        self.max_chars_spin.setValue(0)
        options_layout.addWidget(self.max_chars_spin, 1, 3)

        options_layout.addWidget(QtWidgets.QLabel("Idioma de respuesta:"), 2, 0)
        self.language_combo = QtWidgets.QComboBox()
        self.language_combo.addItems(["Automático", "Español", "Inglés", "Francés", "Portugués"])
        options_layout.addWidget(self.language_combo, 2, 1, 1, 3)
        input_layout.addWidget(self.options_group)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch(1)
        self.execute_button = QtWidgets.QPushButton("Ejecutar")
        self.execute_button.clicked.connect(self.execute_prompt)
        self.execute_button.setEnabled(False)
        button_layout.addWidget(self.execute_button)
        input_layout.addLayout(button_layout)
        layout.addWidget(self.input_group)

        self.result_group = QtWidgets.QGroupBox("Respuesta de Ollama")
        result_layout = QtWidgets.QVBoxLayout(self.result_group)
        self.result_text = QtWidgets.QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumHeight(200)
        self.result_text.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        result_layout.addWidget(self.result_text)
        layout.addWidget(self.result_group)

        layout.addStretch(1)
        self.apply_stylesheet()

    def load_system_specs(self):
        info = get_os_info()
        self.spec_text.setPlainText(format_os_info(info))

    def check_ollama_connection(self):
        if self.api.is_available():
            self.status_label.setText("Estado: ✓ Ollama Conectado")
            self.status_label.setStyleSheet("color: #10b981; font-weight: bold;")
            self.execute_button.setEnabled(True)
            self.load_models()
        else:
            self.status_label.setText("Estado: ✗ Ollama No Disponible (localhost:11434)")
            self.status_label.setStyleSheet("color: #ef4444; font-weight: bold;")
            self.execute_button.setEnabled(False)
            self.model_combo.clear()
            self.model_combo.addItem("No disponible")

    def load_models(self):
        models = self.api.list_models()
        self.available_models = models
        self.model_combo.clear()
        if models:
            self.model_combo.addItems(models)
        else:
            self.model_combo.addItem("No hay modelos disponibles")

    def execute_prompt(self):
        user_text = self.prompt_input.toPlainText().strip()
        if not user_text:
            self.result_text.setPlainText("Por favor escribe un prompt para ejecutar.")
            return

        model = self.model_combo.currentText()
        if model in ["No hay modelos disponibles", "No disponible", "Cargando modelos..."]:
            self.result_text.setPlainText("No hay modelos disponibles. Descarga un modelo primero con: ollama pull <nombre_modelo>")
            return

        temperature = self.temperature_spin.value()
        top_p = self.top_p_spin.value()
        max_tokens = self.max_tokens_spin.value()
        max_chars = self.max_chars_spin.value()
        language = self.language_combo.currentText()

        prompt = user_text
        if language != "Automático":
            prompt = f"Por favor responde en {language}.\n{prompt}"
        if max_chars > 0:
            prompt = f"Responde en un máximo de {max_chars} caracteres.\n{prompt}"

        self.result_text.setPlainText(f"Ejecutando con modelo '{model}'...\n\n---\n")
        QtWidgets.QApplication.processEvents()

        result = self.api.generate(
            model=model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=False
        )
        self.result_text.setMarkdown(f"**Modelo:** {model}\n\n{result}")

    def apply_preset(self):
        selected = self.preset_combo.currentText()
        if selected == "Explicar un concepto":
            self.prompt_input.setPlainText("Explica de forma sencilla el siguiente concepto:\n")
        elif selected == "Generar un comando":
            self.prompt_input.setPlainText("Genera un comando de terminal para realizar la tarea descrita:\n")
        elif selected == "Traducir texto":
            self.prompt_input.setPlainText("Traduce el siguiente texto manteniendo el significado:")
        elif selected == "Resumir texto":
            self.prompt_input.setPlainText("Resume el siguiente texto en pocas oraciones:")
        elif selected == "Corregir gramática":
            self.prompt_input.setPlainText("Corrige la gramática y el estilo del siguiente texto:")
        else:
            self.prompt_input.clear()

    def apply_os(self):
        selected_os = self.os_combo.currentText()
        current_text = self.prompt_input.toPlainText().strip()
        if selected_os != "Automático":
            if current_text:
                self.prompt_input.setPlainText(f"Para {selected_os}: {current_text}")
            else:
                self.prompt_input.setPlainText(f"Para {selected_os}: ")
        else:
            # Remove any "Para OS: " prefix
            if current_text.startswith("Para "):
                colon_index = current_text.find(": ")
                if colon_index != -1:
                    self.prompt_input.setPlainText(current_text[colon_index + 2:])
            else:
                self.prompt_input.setPlainText(current_text)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.apply_stylesheet()
        if self.dark_mode:
            self.dark_mode_button.setText("☀️ Modo Claro")
        else:
            self.dark_mode_button.setText("🌙 Modo Oscuro")

    def apply_stylesheet(self):
        self.setStyleSheet(self.get_stylesheet())

    def get_stylesheet(self):
        if self.dark_mode:
            return self.dark_stylesheet()
        else:
            return self.light_stylesheet()

    @staticmethod
    def light_stylesheet():
        return """
        QWidget {
            background: #f5f7fb;
            color: #222;
            font-family: Segoe UI, Arial, sans-serif;
            font-size: 11pt;
        }
        QGroupBox {
            border: 1px solid #c8d0df;
            border-radius: 8px;
            margin-top: 10px;
            padding: 12px;
            background: #ffffff;
        }
        QGroupBox:title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 14px;
            padding: 0 8px 0 8px;
            color: #33475b;
            font-weight: bold;
        }
        QLabel {
            color: #33475b;
        }
        QPlainTextEdit, QTextEdit {
            border: 1px solid #d1d9e6;
            border-radius: 6px;
            background: #f9fbff;
            padding: 8px;
            color: #222;
        }
        QPushButton {
            background: #3f76ff;
            color: white;
            border-radius: 6px;
            padding: 8px 14px;
            min-width: 120px;
            border: none;
        }
        QPushButton:hover {
            background: #2f5be3;
        }
        QPushButton:pressed {
            background: #264ccd;
        }
        QLabel#header {
            font-size: 18pt;
            font-weight: 700;
            color: #1f3d7a;
        }
        QLabel#status {
            font-size: 10pt;
        }
        QComboBox {
            border: 1px solid #d1d9e6;
            border-radius: 6px;
            padding: 6px;
            background: #f9fbff;
            color: #222;
        }
        """

    @staticmethod
    def dark_stylesheet():
        return """
        QWidget {
            background: #1e1e2e;
            color: #e0e0e0;
            font-family: Segoe UI, Arial, sans-serif;
            font-size: 11pt;
        }
        QGroupBox {
            border: 1px solid #444;
            border-radius: 8px;
            margin-top: 10px;
            padding: 12px;
            background: #2d2d3d;
        }
        QGroupBox:title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 14px;
            padding: 0 8px 0 8px;
            color: #a0a0d8;
            font-weight: bold;
        }
        QLabel {
            color: #e0e0e0;
        }
        QPlainTextEdit, QTextEdit {
            border: 1px solid #444;
            border-radius: 6px;
            background: #252535;
            padding: 8px;
            color: #e0e0e0;
        }
        QPushButton {
            background: #5a6acf;
            color: white;
            border-radius: 6px;
            padding: 8px 14px;
            min-width: 120px;
            border: none;
        }
        QPushButton:hover {
            background: #7b8dd8;
        }
        QPushButton:pressed {
            background: #4a5aaf;
        }
        QLabel#header {
            font-size: 18pt;
            font-weight: 700;
            color: #a0a0d8;
        }
        QLabel#status {
            font-size: 10pt;
        }
        QComboBox {
            border: 1px solid #444;
            border-radius: 6px;
            padding: 6px;
            background: #252535;
            color: #e0e0e0;
        }
        """
