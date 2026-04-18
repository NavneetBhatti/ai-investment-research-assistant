from pydantic import BaseModel, Field


class CompareRequest(BaseModel):
    ticker_1: str = Field(..., min_length=1, max_length=10)
    ticker_2: str = Field(..., min_length=1, max_length=10)
    horizon: str = Field(..., description="Investment horizon: short, medium, or long")
    risk_level: str = Field(..., description="Risk level: low, medium, or high")