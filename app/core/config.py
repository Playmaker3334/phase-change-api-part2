import os
from pydantic import BaseModel
from dotenv import load_dotenv

# Cargar variables de entorno si existe un archivo .env
load_dotenv()

class Settings(BaseModel):
    # Valores del punto crítico
    CRITICAL_PRESSURE: float = 10.0  # MPa
    CRITICAL_SPECIFIC_VOLUME: float = 0.0035  # m³/kg
    
    # Punto adicional en la curva de saturación (del diagrama)
    KNOWN_PRESSURE: float = 0.05  # MPa
    KNOWN_LIQUID_VOLUME: float = 0.00105  # m³/kg
    KNOWN_VAPOR_VOLUME: float = 30.0  # m³/kg
    
    # Configuración de la aplicación
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()