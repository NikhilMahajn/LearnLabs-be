from fastapi import APIRouter,HTTPException,Response
from app.schemas.userProgress import UserProgressRequest,UserProgressResponse
from app.db.userProgress import save_progress

progress_router = APIRouter(prefix="/progress")

@progress_router.post("/save",response_model = UserProgressResponse)
def progress_handler(progress: UserProgressRequest):
    try:
        return save_progress(progress)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving progress: {str(e)}")

    