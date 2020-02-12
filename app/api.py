from uuid import uuid4

from fastapi import FastAPI, HTTPException
from orm import NoMatch
from pydantic import BaseModel, Field
from starlette.requests import Request

from game import (
    GameList,
    GameSchema,
    CreateGame,
    State,
    JoinGame,
    InvalidState
)

from handlers import (
    create_game,
    list_games,
    find_game,
    update_game,
    join_game
)

app = FastAPI(
    docs_url="/api/schema",
    redoc_url="/api/redoc"
)


@app.get("/api/games")
async def games() -> GameList:
    return await list_games()


@app.post("/api/games", response_model=GameSchema)
async def create(request: Request, game_data: CreateGame):
    return await create_game(request, game_data)


@app.get("/api/games/{game_id}", response_model=GameSchema)
async def get_game(game_id: int):
    try:
        return await find_game(game_id)
    except NoMatch:
        raise HTTPException(status_code=404)


class StateUpdate(BaseModel):
    state: State = Field(None, title="New state to set")


@app.post("/api/games/{game_id}", response_model=GameSchema)
async def update(game_id: int, state_update: StateUpdate):
    try:
        return await update_game(game_id, state_update.state)
    except InvalidState:
        raise HTTPException(status_code=400)
    except NoMatch:
        raise HTTPException(status_code=404)


@app.post("/api/games/{game_id}/join", response_model=GameSchema)
async def join(request: Request, game_id: int, join_data: JoinGame):
    try:
        return await join_game(request, game_id, join_data)
    except NoMatch:
        raise HTTPException(status_code=404)


@app.middleware("http")
async def player_session(request: Request, call_next):
    response = await call_next(request)
    if not request.cookies.get("player_id"):
        response.set_cookie("player_id", id(uuid4()))

    return response
