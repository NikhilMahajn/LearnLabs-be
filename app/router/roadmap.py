from fastapi import APIRouter
from app.schemas.roadmap import RoadmapCreateRequest
from app.services.roadmap_generation import generate_roadmap_handler
from app.db.roadmap import get_roadmaps,get_roadmap_by_id,get_roadmap_steps_by_id
roadmap_router = APIRouter(prefix="/roadmap")

@roadmap_router.post("/create")
def create_roadmap_handler(payload:RoadmapCreateRequest):
    roadmap = generate_roadmap_handler(payload)
    return roadmap
    
@roadmap_router.get("/get-roadmaps")
def get_roadmap_handler():
    return get_roadmaps()

@roadmap_router.get("/get-roadmap/{roadmap_id}")
def get_roadmap_handler(roadmap_id: int):
    return get_roadmap_by_id(roadmap_id)

@roadmap_router.get("/get-roadmap-steps/{roadmap_id}")
def get_roadmap_steps_handler(roadmap_id: int):
    return get_roadmap_steps_by_id(roadmap_id)