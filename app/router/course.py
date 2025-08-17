from fastapi import APIRouter,Response
from app.db.models import Course
from app.schemas.course import CourseCreate
from app.db.course import create_course,list_courses
course_router = APIRouter(prefix="/course")


@course_router.post('/create')
def create(course: CourseCreate):
    resposen = create_course(course)
    return resposen
    
@course_router.get('/')
def list():
    return list_courses()