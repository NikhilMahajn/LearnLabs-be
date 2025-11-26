from pydantic import BaseModel, Field
from typing import List, Optional


class RoadmapStep(BaseModel):
    title: str = Field(..., description="Step title")
    description: str = Field(..., description="Short explanation of the step")
    topic_slug: str = Field(..., description="Slug for course generation")
    order_index: int = Field(..., description="Step order in sequence")


class RoadmapOutline(BaseModel):
    name: str = Field(..., description="Roadmap name (e.g., Frontend, Backend)")
    difficulty: str = Field(..., description="Beginner / Intermediate / Advanced")
    slug: str = Field(..., description="Unique identifier for roadmap")
    description: str = Field(..., description="Roadmap description")
    steps: List[RoadmapStep] = Field(..., description="Generated steps")



class RoadmapCreateRequest(BaseModel):
    name: str = Field(..., description="What roadmap should be generated?")
    difficulty: str = Field(..., description="Beginner / Intermediate / Advanced")

