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

1. Clona o descarga este repositorio.
2. Abre una terminal en la carpeta del proyecto.
3. Crea un entorno virtual (opcional, pero recomendado):

   ```bash
   python -m venv venv
   source venv/Scripts/activate   # Windows
   # o
   source venv/bin/activate       # macOS / Linux
   ```

4. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Uso

1. Asegúrate de que Ollama esté corriendo:

   ```bash
   ollama serve
   ```

2. Ejecuta la aplicación:

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

## 🌟 Sugerencias para avanzar

- Añadir soporte para arrastrar y soltar prompts desde archivos.
- Guardar historial de prompts y respuestas.
- Añadir configuración de servidor Ollama desde la interfaz.
- Expandir los presets y agregar plantillas personalizadas.

---

Gracias por usar el Asistente de Comandos Ollama. ¡Disfruta creando prompts más rápido y con mejor contexto! 😊
