import re


class OllamaCommander:
    def __init__(self, os_info: str = "", dataset: dict = None):
        self.os_info = os_info
        self.dataset = dataset or {}

    def suggest_command(self, user_text: str) -> str:
        normalized = self.normalize_text(user_text)
        command = self.guess_command(normalized)
        explanation = self.make_explanation(normalized)
        os_shortcut = self.get_os_shortcut(normalized)
        if os_shortcut:
            explanation += f"\n\nAtajo del OS: {os_shortcut}"
        return f"{command}\n\n# Explicación:\n{explanation}"

    def normalize_text(self, text: str) -> str:
        text = text.strip().lower()
        text = re.sub(r"\s+", " ", text)
        text = text.replace("shod", "show").replace("mdoel", "model").replace("modle", "model")
        text = text.replace("quant", "quantization").replace("qunat", "quantization")
        text = text.replace("flgas", "flags").replace("flag", "flags")
        text = text.replace("llama2", "llama2")
        return text

    def guess_command(self, text: str) -> str:
        if "run" in text and "local" in text and "model" in text:
            return self.build_local_command(text)
        if "list" in text and "model" in text:
            return "ollama list"
        if "help" in text or "usage" in text:
            return "ollama --help"
        if "chat" in text or "completion" in text:
            return self.build_chat_command(text)
        return self.build_default_command(text)

    def build_local_command(self, text: str) -> str:
        command = "ollama run llama2 --model llama2"
        if "8-bit" in text or "8 bit" in text or "8bit" in text:
            command += " --quantize 8"
        if "file" in text and "prompt" in text:
            command += " --prompt-file prompt.txt"
        if "gpu" in text or "cuda" in text:
            command += " --device gpu"
        elif "cpu" in text:
            command += " --device cpu"
        return command

    def build_chat_command(self, text: str) -> str:
        command = "ollama chat llama2"
        if "system" in text and "prompt" in text:
            command += " --system prompt.txt"
        if "temperature" in text:
            command += " --temperature 0.7"
        return command

    def build_default_command(self, text: str) -> str:
        if "model" in text:
            return "ollama run <model-name> --help"
        return "ollama --help"

    def make_explanation(self, normalized: str) -> str:
        if "run" in normalized and "local" in normalized:
            return (
                "Detectada una solicitud de ejecución de modelo local. El comando sugerido usa `ollama run` con un modelo llama2 por defecto. "
                "Agrega `--quantize 8` para cuantización de 8 bits y `--device gpu` si tu entorno soporta GPU."
            )
        if "list" in normalized and "model" in normalized:
            return "Pediste ver los modelos disponibles, por lo que el asistente retorna `ollama list`."
        if "chat" in normalized:
            return "Se recomienda un comando de estilo chat cuando quieres una sesión interactiva con un modelo."
        if "help" in normalized:
            return "Mostrando el comando de ayuda global porque el usuario parece querer orientación sobre el uso de Ollama."
        return "El asistente no pudo inferir un comando preciso, por lo que sugiere `ollama --help` para las opciones disponibles."

    def get_os_shortcut(self, normalized: str) -> str:
        if not self.dataset:
            return ""
        commands = self.dataset.get("comandos de los sistemas operativos", {}).get("comandos similares en los sistemas operativos", [])
        os_name = self.get_os_name()
        for cmd in commands:
            if cmd["comando"].lower() in normalized:
                shortcut = cmd.get(os_name, "N/A")
                return f"{cmd['comando']}: {shortcut} ({cmd['Descripcion']})"
        return ""

    def get_os_name(self) -> str:
        if "windows" in self.os_info.lower():
            return "windows"
        elif "linux" in self.os_info.lower():
            return "Linux"
        elif "mac" in self.os_info.lower() or "darwin" in self.os_info.lower():
            return "Mac"
        return "windows"  # default
