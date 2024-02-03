from fastapi import FastAPI
from routes.shortener import router as ShortenerRouter

app = FastAPI(title="LinkShortener", description="LinkShortener API", version="0.1.0")
app.include_router(ShortenerRouter)

@app.get("/")
def read_root():
    return {"Hello": "World"}
