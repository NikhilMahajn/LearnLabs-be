from pydantic import BaseModel,Field
import json
from enum import Enum
from typing import List, Dict, Any, Optional


class UserProgressRequest(BaseModel):
    user_id: int
    course_id: int
    chapter_id: int
    status: bool
class UserProgressResponse(BaseModel):
    id : int
    user_id: int
    course_id: int
    chapter_id: int
    status: bool
    