from fastapi import FastAPI
from .router.course import course_router
from .router.auth import auth_router
from app.core.config import setup_cors
app = FastAPI()

app.include_router(course_router)
app.include_router(auth_router)

#cors setup
setup_cors(app)


@app.get('/')
def home():
    return {'server is live'}

