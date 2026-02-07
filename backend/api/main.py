from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.research import router as research_router


app = FastAPI()

app.include_router(health_router)
app.include_router(research_router)
