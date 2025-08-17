from pydantic import BaseModel

class CourseCreate(BaseModel):
    name: str
    description: str

class CourseResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True  # enables conversion from SQLAlchemy model
