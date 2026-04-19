import requests
import json


class OllamaAPI:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.timeout = 30

    def is_available(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def list_models(self) -> list:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
            return []
        except Exception as e:
            return []

    def generate(
        self,
        model: str,
        prompt: str,
        temperature: float = None,
        max_tokens: int = None,
        top_p: float = None,
        stream: bool = False,
    ) -> str:
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": stream,
            }
            if temperature is not None:
                payload["temperature"] = temperature
            if max_tokens is not None:
                payload["max_tokens"] = max_tokens
            if top_p is not None:
                payload["top_p"] = top_p
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            if response.status_code == 200:
                if stream:
                    result = ""
                    for line in response.iter_lines():
                        if line:
                            chunk = json.loads(line)
                            result += chunk.get("response", "")
                    return result
                else:
                    data = response.json()
                    if isinstance(data, dict):
                        return data.get("response", "") or data.get("text", "") or json.dumps(data)
                    return str(data)
            return f"Error: {response.status_code}"
        except requests.exceptions.Timeout:
            return "Error: Timeout - Ollama tardó demasiado en responder"
        except requests.exceptions.ConnectionError:
            return "Error: No se puede conectar a Ollama. ¿Está ejecutándose en localhost:11434?"
        except Exception as e:
            return f"Error: {str(e)}"

    def pull_model(self, model_name: str) -> str:
        try:
            payload = {"name": model_name}
            response = requests.post(
                f"{self.base_url}/api/pull",
                json=payload,
                timeout=120
            )
            if response.status_code == 200:
                return f"Modelo '{model_name}' descargado exitosamente"
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error al descargar: {str(e)}"
