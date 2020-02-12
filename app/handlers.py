from typing import Optional

from logzero import logger

from starlette.requests import Request
from db import Game

from game import (
    CreateGame,
    GameList,
    GameSchema,
    GameStatus,
    InvalidState,
    JoinGame,
    Player,
    State,
    is_valid_state
)


async def list_games() -> GameList:
    return GameList(
        games=[
            GameSchema.from_model(game).dict()
            for game in await Game.objects.all()
        ]
    )


async def create_game(request: Request, game_data: CreateGame) -> GameSchema:
    player_id = int(request.cookies.get("player_id"))
    game = await Game.objects.create(
        state=GameSchema.empty_board(),
        owner=Player(
            id=player_id,
            sign=1,
            name=game_data.player_name
        ).dict(),
        challenger=None,
        winner=None,
        status=GameStatus.pending.value
    )

    logger.info(f"Create game for player with id={player_id} and name={game_data.player_name}")

    return GameSchema.from_model(game)


async def find_game(game_id: int) -> Optional[GameSchema]:
    return GameSchema.from_model(await Game.objects.get(id=game_id))


async def update_game(game_id: int, state: State) -> Optional[GameSchema]:
    game = await Game.objects.get(id=game_id)
    if is_valid_state(state):
        await game.update(state=state)
        return GameSchema.from_model(game)
    else:
        logger.info(f"Invalid state={state} update request for game id={game_id}")
        raise InvalidState()


async def join_game(request: Request, game_id: int, join_data: JoinGame) -> Optional[GameSchema]:
    player_id = int(request.cookies.get("player_id"))
    game = await Game.objects.get(id=game_id)

    if can_join(game.owner, game.challenger, player_id) and not game.challenger:
        await game.update(
            challenger=Player(
                id=player_id,
                sign=0,
                name=join_data.player_name
            ).dict(),
            status=GameStatus.active.value
        )

    return GameSchema.from_model(game)


def can_join(owner, challenger, player_id):
    return not (owner["id"] == player_id or (challenger and challenger["id"] == player_id))
