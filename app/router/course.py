from fastapi import APIRouter,Response
from app.db.models import Course
from app.schemas.course import CourseOutline
from app.db.course import create_course,list_courses
from app.services.course_generation import generate_course_handler
course_router = APIRouter(prefix="/course")


@course_router.post('/create')
def create(name,target_audiunce,difficulty,duration):
    body = {
        "name":name,
        "target_audiunce":target_audiunce,
        "difficulty":difficulty,
        "duration":duration
    }
    respose = generate_course_handler(body)
    return respose

@course_router.get('/')
def list():
    return list_courses()

    