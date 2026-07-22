from fastapi import FastAPI
from src.api.routers.financials import router as financials_router
from src.api.routers.portfolio import router as portfolio_router
from src.api.routers.valuation import router as valuation_router
from src.api.routers.screener import router as screener_router
from src.api.routers.sectors import router as sectors_router
from src.api.routers.recommendation import router as recommendation_router
from src.api.routers.risk import router as risk_router

from src.api.routers.peer import router as peer_router
from src.api.routers.health import router as health_router
from src.api.routers.companies import router as companies_router


app = FastAPI(
    title="N100 Financial Intelligence API",
    version="1.0"
)

@app.get("/")
def root():
    return {
        "message": "N100 Financial Intelligence API Running"
    }

app.include_router(health_router)
app.include_router(companies_router)
app.include_router(financials_router)
app.include_router(portfolio_router)
app.include_router(valuation_router)
app.include_router(screener_router)
app.include_router(sectors_router)
app.include_router(recommendation_router)
app.include_router(risk_router)
app.include_router(peer_router)