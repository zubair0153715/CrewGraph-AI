import base64
import requests
from typing import Optional, List
from PIL import Image
import io

class VisionAnalyzer:
    """
    Advanced Vision Agent for analyzing images, charts, and documents.
    Uses Ollama's LLaVA model for local vision processing.
    """
    def __init__(self, model_name="llava:latest"):
        self.model_name = model_name
        self.ollama_url = "http://localhost:11434/api/generate"
        
    def encode_image(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
            
    def analyze_image(self, image_path: str, prompt: str = "Describe this image in detail.") -> str:
        try:
            # Check if llava is available, else fallback
            base64_image = self.encode_image(image_path)
            
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "images": [base64_image],
                "stream": False
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=120)
            if response.status_code == 200:
                return response.json().get("response", "No response generated.")
            else:
                return f"Error: {response.text}"
        except Exception as e:
            return f"Vision analysis failed: {str(e)}. Ensure 'ollama pull llava' is run."

    def extract_text_from_image(self, image_path: str) -> str:
        return self.analyze_image(image_path, "Extract all text from this image exactly as written (OCR).")

    def analyze_chart(self, image_path: str) -> dict:
        response = self.analyze_image(image_path, "Analyze this chart/graph. Provide: 1. Title, 2. Key Trends, 3. Data Points in JSON format.")
        return {"analysis": response}
