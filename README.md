# Ollama Command Assistant

![version](https://img.shields.io/badge/version-0.1.0-blue) ![status](https://img.shields.io/badge/status-Beta-orange)

Una interfaz gráfica ligera en `PyQt5` para usar `Ollama` desde el escritorio. Esta app está diseñada para ayudar a crear, ajustar y ejecutar prompts de manera rápida, con soporte para:

- Conexión directa a un servidor Ollama local (`localhost:11434`)
- Selección de modelo Ollama
- Presets de prompt en español
- Aplicar el sistema operativo objetivo al prompt
- Controles de temperatura, top-p, tokens y caracteres
- Tema claro/oscuro
- Muestra respuestas Markdown en un panel legible
- Barra de desplazamiento automática cuando el contenido no cabe en la ventana
- Visualización de especificaciones del sistema (OS, CPU, Python, usuario)

## 📦 Requisitos

- Python 3.8+ (recomendado 3.11)
- Ollama ejecutándose localmente en `http://localhost:11434`
- Dependencias de Python en `requirements.txt`

## 🚀 Instalación

### Instalar Python

Este proyecto requiere Python 3.8 o superior. Si no tienes Python instalado, sigue estos pasos:

1. Ve al sitio oficial de Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Descarga la versión más reciente de Python 3.x (recomendado 3.11).
3. Ejecuta el instalador:
   - **Windows**: Durante la instalación, marca la opción "Add Python to PATH" para facilitar el uso desde la línea de comandos.
   - **macOS**: Usa Homebrew (`brew install python`) o descarga el instalador desde el sitio.
   - **Linux**: Usa el gestor de paquetes de tu distribución (ej. `sudo apt install python3` en Ubuntu).
4. Verifica la instalación abriendo una terminal y ejecutando `python --version` o `python3 --version`.

### Instalar Ollama

Ollama es necesario para ejecutar los modelos de IA localmente.

1. Ve al sitio oficial de Ollama: [https://ollama.com/download](https://ollama.com/download)
2. Descarga e instala la versión correspondiente a tu sistema operativo (Windows, macOS, Linux).
3. Después de la instalación, inicia el servidor de Ollama ejecutando en una terminal:
   ```bash
   ollama serve
   ```
   Esto iniciará Ollama en `http://localhost:11434`.

### Configurar el proyecto

1. Clona o descarga este repositorio:
   - **Clonar con Git**: Si tienes Git instalado, abre una terminal y ejecuta:
     ```bash
     git clone https://github.com/DanHer01/ProyectoAI
     cd ProyectoAI
     ```
   - **Descargar como ZIP**: 
     - Ve a la página del repositorio en GitHub.
     - Haz clic en "Code" > "Download ZIP".
     - Elige una carpeta en tu computadora donde extraer el archivo (por ejemplo, crea una carpeta llamada "ProyectoAI" en tu escritorio o documentos).
     - Extrae el contenido del archivo ZIP en esa carpeta.
2. Abre una terminal en la carpeta del proyecto.
3. Crea un entorno virtual (opcional, pero recomendado):

   ```bash
   python -m venv venv
   source venv/Scripts/activate   # Windows (en cmd o bash)
   # o
   source venv/bin/activate       # macOS / Linux
   ```

   Nota: En Windows con PowerShell, usa `venv\Scripts\Activate.ps1` en lugar de `source`.

4. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Uso

1. Asegúrate de que Ollama esté corriendo:

   ```bash
   ollama serve
   ```

2. Ejecuta la aplicación desde una terminal (cmd, bash o PowerShell) en el directorio del proyecto:

   ```bash
   python main.py
   ```

3. En la app:

- Espera a que se detecte la conexión con Ollama.
- Elige un modelo disponible.
- Escribe o aplica un prompt prediseñado.
- Ajusta la opción de OS si quieres que la respuesta considere un sistema operativo específico.
- Envía el prompt y revisa la respuesta en el panel de resultados.

## 🧩 Estructura del proyecto

- `app.py` - Interfaz principal de `PyQt5`, diseño, controles y presentación.
- `main.py` - Punto de entrada para lanzar la aplicación.
- `ollama_api.py` - Wrapper simple para consultar modelos y generar texto desde Ollama.
- `os_info.py` - Recopila y formatea información del sistema para mostrar en la app.
- `requirements.txt` - Dependencias de Python.
- `dataset.json` - Archivo de datos opcional para uso futuro en prompts o personalización.

## 💡 Notas

- Si la ventana se reduce y no se puede ver todo el contenido, el scroll se activa automáticamente.
- El panel de resultados puede renderizar texto Markdown básico.
- La app está en etapa Beta, por lo que pueden añadirse mejoras y nuevas funciones.

## 🌟 Proxima actualizacion... 

- Añadir soporte para arrastrar y soltar prompts desde archivos.
- Guardar historial de prompts y respuestas.
- Añadir configuración de servidor Ollama desde la interfaz.
- Expandir los presets y agregar plantillas personalizadas.

---

Gracias por usar el Asistente de Comandos Ollama. 
