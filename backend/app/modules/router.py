from fastapi import APIRouter

from app.modules.evaluations.router import router as evaluations_router
from app.modules.health.router import router as health_router
from app.modules.prompt_blocks.router import router as prompt_blocks_router
from app.modules.tickets.router import router as tickets_router
from app.modules.topics.router import router as topics_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health_router)
api_router.include_router(topics_router)
api_router.include_router(tickets_router)
api_router.include_router(prompt_blocks_router)
api_router.include_router(evaluations_router)
