from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=10, description="Stock ticker symbol")
    horizon: str = Field(..., description="Investment horizon: short, medium, or long")
    risk_level: str = Field(..., description="Risk level: low, medium, or high")