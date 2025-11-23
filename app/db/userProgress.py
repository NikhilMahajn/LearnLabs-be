from fastapi import HTTPException
from .db import session
from app.schemas.userProgress import UserProgressRequest
from app.db.models import UserProgress
from datetime import datetime
def save_progress(progress: UserProgressRequest):
    try:
        exits = session.query(UserProgress).filter(
            UserProgress.user_id == progress.user_id,
            UserProgress.course_id == progress.course_id,
            UserProgress.chapter_id == progress.chapter_id
            ).first()
        if exits:
            raise HTTPException(status_code = 409,detail="record already exits")
        
        progress_obj = UserProgress(
			user_id = progress.user_id,
			course_id = progress.course_id,
			chapter_id = progress.chapter_id,
			status = progress.status,
			completed_at = datetime.now()
		)
        session.add(progress_obj)
        session.commit()
        session.refresh(progress_obj)
        return progress_obj
    except Exception as e:
        session.rollback()
        raise e

		

