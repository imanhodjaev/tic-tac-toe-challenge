from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

__all__ = [
    "CreateGame",
    "GameList",
    "GameSchema",
    "is_valid_state",
    "InvalidState",
    "JoinGame",
    "Player",
    "State",
    "GameStatus"
]


State = str


class InvalidState(Exception):
    pass


class GameStatus(Enum):
    pending: str = "pending"
    active: str = "active"
    done: str = "done"
    cancelled: str = "cancelled"


class Player(BaseModel):
    id: int     # will use built-in `id`
    sign: int   # 1 or 0
    name: str


class GameSchema(BaseModel):
    """Since game requirements are simple we a going to
    keep it as simple as possible.
    """
    # will also use built-in `id`
    id: int

    # is a string like `1 0 - 0 0 - - - -` to
    # represent the current state of game
    state: str
    owner: Player
    challenger: Optional[Player]
    winner: Optional[int]
    status: GameStatus = GameStatus.pending

    @staticmethod
    def empty_board() -> str:
        return " ".join(["-" for _ in range(9)])

    @staticmethod
    def from_model(model):
        game = GameSchema(
            id=model.id,
            state=model.state,
            owner=Player(**model.owner),
            winner=model.winner,
            status=model.status
        )

        if model.challenger:
            game.challenger = model.challenger

        return game


class GameList(BaseModel):
    games: List[GameSchema]


class CreateGame(BaseModel):
    player_name: str


class JoinGame(BaseModel):
    player_name: str


def is_valid_state(state: str) -> bool:
    return len(state.split(' ')) == 9


win_states = [
    "x x x - - - - - -",
    "- - - x x x - - -",
    "- - - - - - x x x",
    "- x - - x - - x -",
    "x - - x - - x - -",
    "- - x - - x - - x",
    "x - - - x - - - x",
    "- - x - x - x - -"
]


def get_winner(game: GameSchema) -> Optional[Player]:
    """Determine if we have any winner
    :param game: Game
    :return: player
    """
    if not game.challenger:
        return None

    if map_player(game.state, game.owner.sign) in win_states:
        return game.owner

    if map_player(game.state, game.challenger.sign) in win_states:
        return game.challenger

    return None


def map_player(state: str, which: int) -> str:
    """Extract moves for given player and return
    separate mapping and excluding the others
    :param state: str
    :param which: int
    :return: str
    """
    player_map = []
    for v in state:
        if v == str(which):
            player_map.append('x')
        else:
            player_map.append('-')

    return ' '.join(player_map)
