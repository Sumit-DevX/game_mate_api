from fastapi import FastAPI

from routers.users import router as user_router
from routers.games import router as game_router
from routers.lfgPosts import router as lfg_router
from routers.auth import router as auth_router

app = FastAPI()

@app.get("/")
def root():
    return {"message" : "Gamemate API is running"}



app.include_router(user_router)
    
app.include_router(game_router)

app.include_router(lfg_router)

app.include_router(auth_router)