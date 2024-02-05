from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.shortener import router as ShortenerRouter

app = FastAPI(title="LinkShortener", description="LinkShortener API", version="0.1.0")
app.include_router(ShortenerRouter)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}
