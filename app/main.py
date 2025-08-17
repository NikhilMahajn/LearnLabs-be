from fastapi import FastAPI
from .router.course import course_router
app = FastAPI()

app.include_router(course_router)

@app.get('/')
def home():
    return {'server is live'}

