from pydantic import BaseModel,Field
from typing import List
import json
from langchain.schema import BaseOutputParser

from typing import List, Dict, Any, Optional
        
class SectionType(str, Enum):
    CONTENT = "content"
    INFO = "info"
    CODE = "code"
    TIP = "tip"

class Section(BaseModel):
    """Model for a lesson section"""
    type: SectionType = Field(description="Type of section")
    title: str = Field(description="Section title")
    content: str = Field(description="Main content")
    language: Optional[str] = Field(default=None, description="Programming language for code sections")
    explanation: Optional[str] = Field(default=None, description="Explanation for code sections")

class DetailedChapter(BaseModel):
    """Model for a detailed chapter with rich content"""
    id: int = Field(description="Chapter ID")
    title: str = Field(description="Chapter title")
    duration: str = Field(description="Duration in readable format (e.g., '15 min')")
    type: str = Field(default="lesson", description="Chapter type")
    sections: List[Section] = Field(description="List of chapter sections")


class Chapter(BaseModel):
    """Model for a course chapter"""
    chapter_number: int = Field(description="Chapter number")
    title: str = Field(description="Chapter title")
    description: str = Field(description="Brief description of chapter content")
    learning_objectives: List[str] = Field(description="Key learning objectives")
    estimated_duration: int = Field(description="Estimated time to complete in Minutes")

class CourseOutline(BaseModel):
    """Model for complete course outline"""
    course_title: str = Field(description="Title of the course")
    course_description: str = Field(description="Brief course description")
    level: str = Field(description="Level of course")
    total_chapters: int = Field(description="Total number of chapters")
    duration: int   = Field(description="Time required to complete the course in Minutes")
    chapters: List[Chapter] = Field(description="List of chapters")
    
    
class CourseResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True  # enables conversion from SQLAlchemy model