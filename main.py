from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Vercel!"}

# This makes FastAPI work in serverless mode

app = FastAPI()

origins = [
    "http://localhost:5173",  # React app
    "http://127.0.0.1:8000",
    "https://learn-labs-be.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
	allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def home():
    return {'message':'hellow'}


handler = Mangum(app)