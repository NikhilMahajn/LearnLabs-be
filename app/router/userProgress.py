from fastapi import APIRouter,HTTPException,Response
from app.schemas.userProgress import UserProgressRequest,UserProgressResponse
from app.db.userProgress import save_progress,get_completed_chapters

progress_router = APIRouter(prefix="/progress")

@progress_router.post("/save",response_model = UserProgressResponse)
def progress_handler(progress: UserProgressRequest):
    try:
        return save_progress(progress)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving progress: {str(e)}")

@progress_router.get("/get-progress")
def completed_chapter_handler(user_id:int,course_id:int):
    try:
        chapters = get_completed_chapters(user_id,course_id)
        return chapters
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error fetching progress: {str(e)}")