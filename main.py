from fastapi import FastAPI
from src.routes.auth import user_routes
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
@app.get("/")
def root():
    return {
        "message": "Backend is running successfully "
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://frontendpdf.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_routes)