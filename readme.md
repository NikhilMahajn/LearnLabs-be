uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level info

# Venv Command
source venv/bin/activate

Decorator example 

```
def get_course_by_id(course_id,user = Depends(require_auth)):
    if course_id is None:
        raise HTTPException(status_code=400, detail="course_id cannot be null")
    try:
        response = get_course(course_id)
        if not response:
            raise HTTPException(status_code=404, detail="No chapters found for this course")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
```