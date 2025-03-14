from rest_framework.decorators import api_view
from rest_framework.response import Response
import httpx
import logging
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
# Configurar el logger
logger = logging.getLogger(__name__)

@api_view(['POST'])
def chat(request):
    prompt = request.data.get("prompt", "")
    
    if not prompt:
        return Response({"error": "El prompt es obligatorio"}, status=400)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [{"role": "system", "content": prompt + "responde en español"}]
    }
    
    try:
        with httpx.Client() as client:
            response = client.post(f"{BASE_URL}/chat/completions", json=payload, headers=headers)
        
        if response.status_code == 200:
            content = response.json()
            message = content.get("choices", [{}])[0].get("message", {}).get("content", "No content available")
            return Response({"response": message})
        else:
            logger.error(f"Error en la API: {response.status_code} - {response.text}")
            return Response({"error": "Failed to get response", "details": response.text}, status=400)
    
    except httpx.RequestError as e:
        logger.error(f"Error de conexión con OpenRouter: {e}")
        return Response({"error": "Error de conexión con OpenRouter", "details": str(e)}, status=500)