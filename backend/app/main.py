from fastapi import FastAPI

from app.api.v1.api import router
from app.api.v1.pending import PendingEndpoint, pending_handler

app = FastAPI(
    title="Lean Project Management",
    version="0.1.0",
    redirect_slashes=False,
)
app.add_exception_handler(PendingEndpoint, pending_handler)
app.include_router(router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
