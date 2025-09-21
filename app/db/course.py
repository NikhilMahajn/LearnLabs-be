from .db import session
from app.schemas.course import CourseOutline,Chapter as ChapterSchema
from .models import Course,Chapter


def create_course(course:CourseOutline):
    new_course = Course(
        title=course.course_title,
        description=CourseOutline.course_description,
        level=CourseOutline.level,
        duration=CourseOutline.duration
    )
    session.add(new_course)
    session.commit()
    
    session.refresh(new_course) 
    return new_course

def list_courses():
    courses = session.query(Course).all()
    return courses
    
def create_chapter(Course_id,ChapterSchema):
    
    new_chapter = Chapter(
        chapter_number=ChapterSchema.chapter_number,
        title=ChapterSchema.title,
        description = ChapterSchema.description,
        estimated_duration= ChapterSchema.estimated_duration,
        course_id = Course_id
        )

    session.add(new_chapter)
    session.commit()
    
    session.refresh(new_chapter) 
    return new_chapter

    