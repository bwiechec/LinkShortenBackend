from fastapi import FastAPI
from routes.shortener import router as ShortenerRouter

app = FastAPI()
app.include_router(ShortenerRouter)

@app.get("/")
def read_root():
    return {"Hello": "World"}
