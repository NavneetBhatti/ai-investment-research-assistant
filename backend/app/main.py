from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="AI Investment Research Assistant",
    version="0.1.0"
)

app.include_router(router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Backend is running"
}

