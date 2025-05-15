from fastapi import APIRouter, Query, HTTPException
from app.core.logging import logger
from app.services.phase_change import calculate_specific_volumes

router = APIRouter()

@router.get("/phase-change-diagram")
async def phase_change_diagram(
    pressure: float = Query(..., description="Pressure in MPa", gt=0)
):
    """
    Calculate the specific volumes for liquid and vapor phases at the given pressure.
    
    Parameters:
    - pressure: Pressure in MPa (must be positive)
    
    Returns:
    - JSON with specific_volume_liquid and specific_volume_vapor
    """
    try:
        logger.info(f"Received request with pressure: {pressure} MPa")
        result = calculate_specific_volumes(pressure)
        logger.info(f"Calculated volumes: {result}")
        return result
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))