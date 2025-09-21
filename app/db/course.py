from .db import session
from app.schemas.course import CourseOutline,Chapter,DetailedChapter
from .models import Course,Chapter,Section


def create_course(course:CourseOutline):
    new_course = Course(
        title=course.course_title,
        description=course.course_description,
        level=course.level,
        duration=course.duration,
        total_chapters = course.total_chapters
    )
    session.add(new_course)
    session.commit()
    
    session.refresh(new_course) 
    return new_course

def list_courses():
    courses = session.query(Course).all()
    return courses
    
def create_chapter(Course_id,chapter,chapter_content:DetailedChapter):
    
    new_chapter = Chapter(
        chapter_number=chapter.chapter_number,
        title=chapter.title,
        description = chapter.description,
        estimated_duration= chapter.estimated_duration,
        course_id = Course_id
    )
    
    for section in chapter_content.sections:
        
        new_section = Section(
                type=section.type,
                title=section.title,
                content=section.content,
                language=section.language,
                explanation=section.explanation,
                chapter_id=new_chapter.id
        )
        session.add(new_section)
        session.commit()
        
    session.add(new_chapter)
    session.commit()
    
    session.refresh(new_chapter) 
    return new_chapter

    