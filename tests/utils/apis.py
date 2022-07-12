import json

from tests.utils.funcs import construct_headers
from tests.utils.routes import AuthRoutes, MazeRoutes

user_creds = {"name": "happyUser", "password": "iTk19!n"}


def do_post(client, route, payload, token=None):
    return client.post(
        route, data=json.dumps(payload), headers=construct_headers(token)
    )


def do_get(client, route, token):
    return client.get(route, headers=construct_headers(token))


def signin_route(client, creds):
    return do_post(client, AuthRoutes.SIGNIN, payload=creds)


def signup_route(client, creds):
    return do_post(client, AuthRoutes.SIGNUP, payload=creds)


def create_maze(client, payload, token=None):
    return do_post(client, MazeRoutes.BASE, payload=payload, token=token)


def get_maze_path(client, maze_id="1", token=None, solution_type=None):
    return do_get(client, MazeRoutes().get_maze(maze_id, solution_type), token=token)


def get_mazes(client, token=None):
    return do_get(client, MazeRoutes.BASE, token=token)


def get_token(client, creds=None):
    if creds is None:
        creds = user_creds
    signup_route(client, creds=creds)
    signin_response = signin_route(client, creds)
    return signin_response.json["token"]
