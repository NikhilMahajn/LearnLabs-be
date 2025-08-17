from fastapi import APIRouter,Response
from db.models import Course
from schemas.course import CourseCreate
from db.course import create_course
course_router = APIRouter(prefix="/course")


@course_router.post('/create')
def create(course: CourseCreate):
    print('request',course)
    resposen = create_course(course)
    return resposen
    
    