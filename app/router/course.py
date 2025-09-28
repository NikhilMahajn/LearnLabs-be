from fastapi import APIRouter,Response
from app.schemas.course import CourseCreateRequest,CourseResponse,ChapterResponse
from app.db.course import list_courses,get_course,get_chapters
from app.services.course_generation import generate_course_handler


course_router = APIRouter(prefix="/course")


@course_router.post('/create')
def create(course: CourseCreateRequest):
    
    respose = generate_course_handler(course)
    return Response('Course Generation Successfull')

@course_router.get('/')
def get_courses():
    return list_courses()

@course_router.get('/{course_id}')
def get_course_by_id(course_id):
    response = get_course(course_id)
    return response
    
@course_router.get('/chapters/{course_id}')
def get_chapters_by_course(course_id:int):
    response = get_chapters(course_id)
    return response