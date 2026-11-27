from fastapi import APIRouter

from app.api.v1.routers import activities, admin, audit, auth, projects, reporting

router = APIRouter(prefix="/api")

router.include_router(auth.router)
router.include_router(admin.router)
router.include_router(projects.router)
router.include_router(activities.router)
router.include_router(reporting.router)
router.include_router(audit.router)
