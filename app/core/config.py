from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",  # React app
    "http://127.0.0.1:8000",
    "https://learn-labs-fe.vercel.app"
]
def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)

