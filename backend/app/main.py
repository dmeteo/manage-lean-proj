from fastapi import FastAPI

from app.api.v1.api import router

app = FastAPI(title="Lean Project Management", version="0.1.0", redirect_slashes=False)
app.include_router(router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
