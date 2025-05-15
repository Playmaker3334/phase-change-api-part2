from fastapi import FastAPI
from app.core.logging import logger
from app.api.routes import router

app = FastAPI(
    title="Phase Change API",
    description="API para calcular volúmenes específicos en diagramas de cambio de fase",
    version="1.0.0"
)

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    logger.info("Phase Change API started")