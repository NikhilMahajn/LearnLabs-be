from fastapi import APIRouter,Response
from app.schemas.course import CourseCreateRequest,CourseResponse
from app.db.course import create_course,list_courses
from app.services.course_generation import generate_course_handler


course_router = APIRouter(prefix="/course")


@course_router.post('/create')
def create(course: CourseCreateRequest):
    
    respose = generate_course_handler(course)
    return Response('Course Generation Successfull')

@course_router.get('/')
def list():
    return list_courses()

    