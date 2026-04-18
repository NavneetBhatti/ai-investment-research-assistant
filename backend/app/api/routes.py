from fastapi import APIRouter
from app.schemas.request import AnalyzeRequest
from app.schemas.response import AnalyzeResponse
from app.schemas.compare_request import CompareRequest
from app.schemas.compare_response import CompareResponse
from app.services.analysis_service import analyze_stock
from app.services.compare_service import compare_stocks

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": "Welcome to AI Investment Research Assistant API"
    }


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest):
    return analyze_stock(
        ticker=payload.ticker,
        risk_level=payload.risk_level
    )


@router.post("/compare", response_model=CompareResponse)
def compare(payload: CompareRequest):
    return compare_stocks(
        ticker_1=payload.ticker_1,
        ticker_2=payload.ticker_2,
        risk_level=payload.risk_level,
        horizon=payload.horizon
    )