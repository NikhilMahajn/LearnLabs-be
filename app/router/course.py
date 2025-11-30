from fastapi import APIRouter,Response,HTTPException, Depends
import asyncio


from app.schemas.course import CourseCreateRequest,CourseResponse,ChapterResponse
from app.db.course import list_courses,get_course,get_chapters,get_sections,get_course_by_slug
from app.services.course_generation import generate_course_handler
from app.db.auth import require_auth
from app.db.roadmap import get_roadmap_by_slug
from app.utils.slug import reverse_slugify
from app.utils.logger import get_logger

logger = get_logger(__name__)


course_router = APIRouter(prefix="/course")


@course_router.post('/create')
async def create(course: CourseCreateRequest):
    asyncio.create_task(generate_course_handler(course))
    return {"status":200,"details":'Course Generation Started'}

@course_router.get('/')
def get_courses():
    return list_courses()


@course_router.get('/{course_id}')
def get_course_by_id(course_id):
    if course_id is None:
        raise HTTPException(status_code=400, detail="course_id cannot be null")
    try:
        response = get_course(course_id)
        if not response:
            raise HTTPException(status_code=404, detail="No chapters found for this course")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@course_router.get('/chapters/{course_id}')
def get_chapters_by_course(course_id:int):
    if course_id is None:
        raise HTTPException(status_code=400, detail="course_id cannot be null")

    try:
        response = get_chapters(course_id)
        if not response:
            raise HTTPException(status_code=404, detail="No chapters found for this course")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@course_router.get('/chapters/{chapter_id}/sections')
def get_sections_by_chapter(chapter_id:int):
    if chapter_id is None :
        raise HTTPException(status_code=400, detail="chapter_id cannot be null")
    try:
        response = get_sections(chapter_id)
        if not response:
            raise HTTPException(status_code=404, detail="No chapters found for this course")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    
@course_router.get('/get-course-slug/{course_slug}')
async def get_course_by_slug_handler(course_slug: str, roadmap_slug: str = None):
    if not course_slug:
        raise HTTPException(status_code=400, detail="course_slug cannot be null")
    try:
        response = get_course_by_slug(course_slug)
        if not response:
            roadmap = get_roadmap_by_slug(roadmap_slug)
            course = CourseCreateRequest(
                name = reverse_slugify(course_slug),
                difficulty = roadmap.get("difficulty")
            )
            return await create(course)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
