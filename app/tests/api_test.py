import sys
from requests.cookies import RequestsCookieJar
from starlette.testclient import TestClient

from app.api import app

player_1 = RequestsCookieJar()
player_1.set("player_id", str(1))
player_2 = RequestsCookieJar()
player_2.set("player_id", str(2))

client = TestClient(app)


def test_create_game():
    response = client.post(
        "/api/games",
        json={"player_name": "name"},
        cookies=player_1
    )

    result = response.json()
    assert response.status_code == 200
    assert result == {
        "id": result["id"],
        "state": "- - - - - - - - -",
        "owner": {"id": 1, "sign": 1, "name": "name"},
        "challenger": None,
        "winner": None,
        "status": "pending"
    }


def test_list_games():
    client.post(
        "/api/games",
        json={"player_name": "name"},
        cookies=player_1
    ).json()

    response = client.get("/api/games", cookies=player_1)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json() == {
        'games': [
            {
                'id': 1,
                'state': '- - - - - - - - -',
                'owner': {'id': 1, 'sign': 1, 'name': 'name'},
                'challenger': None,
                'winner': None,
                'status': 'pending'
            },
            {
                'id': 2,
                'state': '- - - - - - - - -',
                'owner': {'id': 1, 'sign': 1, 'name': 'name'},
                'challenger': None,
                'winner': None,
                'status': 'pending'
            }
        ]
    }


def test_get_game_details():
    response = client.get("/api/games", cookies=player_1)
    assert response.status_code == 200

    [game, *_] = response.json()["games"]
    response = client.get(f"/api/games/{game['id']}", cookies=player_1)
    assert response.status_code == 200
    assert game == response.json()


def test_update_game_state():
    response = client.get("/api/games", cookies=player_1)
    assert response.status_code == 200

    [game, *_] = response.json()["games"]
    payload = {
        "state": "1 1 1 - - - - - -"
    }

    response = client.post(f"/api/games/{game['id']}", json=payload, cookies=player_1)
    assert response.status_code == 200

    updated = client.get(f"/api/games/{game['id']}", cookies=player_1)
    assert updated.json() == response.json()


def test_join_game():
    response = client.get("/api/games", cookies=player_2)
    assert response.status_code == 200

    [game, *_] = response.json()["games"]
    payload = {
        "player_name": "bobo"
    }

    response = client.post(f"/api/games/{game['id']}/join", json=payload, cookies=player_2)
    assert response.status_code == 200

    updated = client.get(f"/api/games/{game['id']}", cookies=player_2)
    assert updated.json() == response.json()

