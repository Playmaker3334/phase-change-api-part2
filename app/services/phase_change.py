import numpy as np
from app.core.logging import logger
from app.core.config import settings

def calculate_specific_volumes(pressure: float) -> dict:
    """
    Calculate specific volumes for liquid and vapor phases at given pressure.
    """
    logger.debug(f"Calculating specific volumes for pressure: {pressure} MPa")
    
    # Extraer constantes de la configuración
    CRITICAL_PRESSURE = settings.CRITICAL_PRESSURE
    CRITICAL_SPECIFIC_VOLUME = settings.CRITICAL_SPECIFIC_VOLUME
    KNOWN_PRESSURE = settings.KNOWN_PRESSURE
    KNOWN_LIQUID_VOLUME = settings.KNOWN_LIQUID_VOLUME
    KNOWN_VAPOR_VOLUME = settings.KNOWN_VAPOR_VOLUME
    
    # Calcular volúmenes específicos
    if pressure >= CRITICAL_PRESSURE:
        # En o por encima de la presión crítica
        logger.debug(f"Pressure {pressure} MPa >= critical pressure {CRITICAL_PRESSURE} MPa")
        specific_volume_liquid = CRITICAL_SPECIFIC_VOLUME
        specific_volume_vapor = CRITICAL_SPECIFIC_VOLUME
    else:
        # Por debajo de la presión crítica - usar interpolación
        logger.debug(f"Pressure {pressure} MPa < critical pressure, using interpolation")
        
        # Cálculo para la fase líquida
        liquid_exponent = np.log(CRITICAL_SPECIFIC_VOLUME / KNOWN_LIQUID_VOLUME) / np.log(CRITICAL_PRESSURE / KNOWN_PRESSURE)
        specific_volume_liquid = KNOWN_LIQUID_VOLUME * (pressure / KNOWN_PRESSURE) ** liquid_exponent
        logger.debug(f"Calculated liquid volume: {specific_volume_liquid} m³/kg")
        
        # Cálculo para la fase vapor
        vapor_exponent = np.log(CRITICAL_SPECIFIC_VOLUME / KNOWN_VAPOR_VOLUME) / np.log(CRITICAL_PRESSURE / KNOWN_PRESSURE)
        specific_volume_vapor = KNOWN_VAPOR_VOLUME * (pressure / KNOWN_PRESSURE) ** vapor_exponent
        logger.debug(f"Calculated vapor volume: {specific_volume_vapor} m³/kg")
    
    return {
        "specific_volume_liquid": specific_volume_liquid,
        "specific_volume_vapor": specific_volume_vapor
    }