from fastapi import FastAPI
from app.routers.scores import router as game_router

app = FastAPI()

# Include the game router
app.include_router(game_router, prefix="/scores", tags=["Scores"])


@app.get("/")
def root():
    return {"message": "Welcome to the Dart API!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
