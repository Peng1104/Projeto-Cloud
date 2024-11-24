"""
Main module of the app
"""

import os
from fastapi import FastAPI
from web_app.db_manager import lifespan
from web_app.app_routes import ROUTER

# Instância do FastAPI no escopo global
APP = FastAPI(lifespan=lifespan)
APP.include_router(ROUTER)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("web_app.__main__:APP", host="0.0.0.0", port=int(
        os.getenv("APP_PORT", "8000")), log_level="info")
