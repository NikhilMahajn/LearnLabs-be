from .db import session
from .models import Course
from schemas.course import CourseCreate


def create_course(course : CourseCreate):
    new_course = Course(name=course.name,description=course.description)
    session.add(new_course)
    session.commit()
    
    session.refresh(new_course) 
    return new_course