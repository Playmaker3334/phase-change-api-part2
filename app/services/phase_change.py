import numpy as np
from app.core.logging import logger
from app.core.config import settings

def calculate_specific_volumes(pressure: float) -> dict:
    """
    Calculate specific volumes for liquid and vapor phases at given pressure.
    Uses linear interpolation of v with respect to log(P).
    """
    logger.debug(f"Calculating specific volumes for pressure: {pressure} MPa using v vs log(P) linear interpolation.")
    
    CRITICAL_PRESSURE = settings.CRITICAL_PRESSURE
    CRITICAL_SPECIFIC_VOLUME = settings.CRITICAL_SPECIFIC_VOLUME
    KNOWN_PRESSURE = settings.KNOWN_PRESSURE
    KNOWN_LIQUID_VOLUME = settings.KNOWN_LIQUID_VOLUME
    KNOWN_VAPOR_VOLUME = settings.KNOWN_VAPOR_VOLUME
    
    # Logaritmos de las presiones conocidas (usaremos logaritmo natural - np.log)
    LOG_KNOWN_PRESSURE = np.log(KNOWN_PRESSURE)
    LOG_CRITICAL_PRESSURE = np.log(CRITICAL_PRESSURE)
    
    if pressure >= CRITICAL_PRESSURE:
        logger.debug(f"Pressure {pressure} MPa >= critical pressure {CRITICAL_PRESSURE} MPa")
        specific_volume_liquid = CRITICAL_SPECIFIC_VOLUME
        specific_volume_vapor = CRITICAL_SPECIFIC_VOLUME
    elif pressure <= KNOWN_PRESSURE: # Manejar el caso si P es igual o menor al punto conocido
        logger.debug(f"Pressure {pressure} MPa <= known pressure {KNOWN_PRESSURE} MPa")
        # Aunque el robot solo consulta P > 0.05 MPa, es bueno tener este caso.
        # Si P < KNOWN_PRESSURE, esta interpolación estaría extrapolando, lo cual podría no ser preciso.
        # Pero si P == KNOWN_PRESSURE, debería dar los valores conocidos.
        # Para P < KNOWN_PRESSURE, decidimos si extrapolamos o devolvemos error/valor conocido.
        # Por ahora, la fórmula de interpolación lineal manejará la extrapolación.
        # Si P == KNOWN_PRESSURE, la fórmula debería dar los valores conocidos.
        
        # Si es exactamente el punto conocido, devolver valores conocidos para evitar problemas de log(0) si pressure fuera 0
        if pressure == KNOWN_PRESSURE:
            specific_volume_liquid = KNOWN_LIQUID_VOLUME
            specific_volume_vapor = KNOWN_VAPOR_VOLUME
        else: # Extrapolación o P entre 0 y KNOWN_PRESSURE (que no debería ocurrir por la pista del robot)
              # Recalculamos usando la fórmula para consistencia, pero con advertencia.
            logger.warning(f"Pressure {pressure} is outside the primary interpolation range (KNOWN_PRESSURE to CRITICAL_PRESSURE). Results are extrapolated.")
            # Pendiente (m) para la línea de líquido v vs log(P)
            m_liquid = (CRITICAL_SPECIFIC_VOLUME - KNOWN_LIQUID_VOLUME) / (LOG_CRITICAL_PRESSURE - LOG_KNOWN_PRESSURE)
            # Intercepto (c) para la línea de líquido: v = m*log(P) + c => c = v - m*log(P)
            # Usamos el punto conocido: c_liquid = KNOWN_LIQUID_VOLUME - m_liquid * LOG_KNOWN_PRESSURE
            # Entonces: specific_volume_liquid = m_liquid * np.log(pressure) + c_liquid
            specific_volume_liquid = KNOWN_LIQUID_VOLUME + m_liquid * (np.log(pressure) - LOG_KNOWN_PRESSURE)
            
            # Pendiente (m) para la línea de vapor v vs log(P)
            m_vapor = (CRITICAL_SPECIFIC_VOLUME - KNOWN_VAPOR_VOLUME) / (LOG_CRITICAL_PRESSURE - LOG_KNOWN_PRESSURE)
            # Intercepto (c) para la línea de vapor: c_vapor = KNOWN_VAPOR_VOLUME - m_vapor * LOG_KNOWN_PRESSURE
            # Entonces: specific_volume_vapor = m_vapor * np.log(pressure) + c_vapor
            specific_volume_vapor = KNOWN_VAPOR_VOLUME + m_vapor * (np.log(pressure) - LOG_KNOWN_PRESSURE)
    else:
        # Interpolar para 0.05 < pressure < 10
        logger.debug(f"Pressure {pressure} MPa is between KNOWN_PRESSURE and CRITICAL_PRESSURE, interpolating v vs log(P).")
        
        log_current_pressure = np.log(pressure)
        
        # Interpolación lineal para líquido: v_liq = v1 + (v2-v1) * (logP - logP1) / (logP2 - logP1)
        # Punto 1: (LOG_KNOWN_PRESSURE, KNOWN_LIQUID_VOLUME)
        # Punto 2: (LOG_CRITICAL_PRESSURE, CRITICAL_SPECIFIC_VOLUME)
        # Punto actual: log_current_pressure
        
        specific_volume_liquid = KNOWN_LIQUID_VOLUME + \
                               (CRITICAL_SPECIFIC_VOLUME - KNOWN_LIQUID_VOLUME) * \
                               (log_current_pressure - LOG_KNOWN_PRESSURE) / \
                               (LOG_CRITICAL_PRESSURE - LOG_KNOWN_PRESSURE)
        logger.debug(f"Calculated liquid volume: {specific_volume_liquid} m³/kg")
        
        # Interpolación lineal para vapor: v_vap = v1 + (v2-v1) * (logP - logP1) / (logP2 - logP1)
        # Punto 1: (LOG_KNOWN_PRESSURE, KNOWN_VAPOR_VOLUME)
        # Punto 2: (LOG_CRITICAL_PRESSURE, CRITICAL_SPECIFIC_VOLUME)

        specific_volume_vapor = KNOWN_VAPOR_VOLUME + \
                                (CRITICAL_SPECIFIC_VOLUME - KNOWN_VAPOR_VOLUME) * \
                                (log_current_pressure - LOG_KNOWN_PRESSURE) / \
                                (LOG_CRITICAL_PRESSURE - LOG_KNOWN_PRESSURE)
        logger.debug(f"Calculated vapor volume: {specific_volume_vapor} m³/kg")
        
    return {
        "specific_volume_liquid": specific_volume_liquid,
        "specific_volume_vapor": specific_volume_vapor
    }
