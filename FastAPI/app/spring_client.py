import httpx
import os
from typing import Optional, Dict, Any

class SpringAPIClient:
    def __init__(self):
        self.base_url = os.getenv("SPRING_API_URL", "http://localhost:8080")
        self.timeout = 10.0

    async def crear_persona(self, persona_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Crear persona en Spring Boot"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/personas",
                    json=persona_data
                )
                if response.status_code in [200, 201]:
                    return response.json()
                return None
        except Exception as e:
            print(f"Error al crear persona en Spring: {e}")
            return None

    async def actualizar_persona(self, persona_id: int, persona_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualizar persona en Spring Boot"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.put(
                    f"{self.base_url}/api/personas/{persona_id}",
                    json=persona_data
                )
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            print(f"Error al actualizar persona en Spring: {e}")
            return None

    async def eliminar_persona(self, persona_id: int) -> bool:
        """Eliminar persona en Spring Boot"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.delete(
                    f"{self.base_url}/api/personas/{persona_id}"
                )
                return response.status_code == 204
        except Exception as e:
            print(f"Error al eliminar persona en Spring: {e}")
            return False
