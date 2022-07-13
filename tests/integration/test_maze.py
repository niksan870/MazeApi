from tests.utils.apis import get_maze_path, get_token, create_maze, get_mazes


def test_create_maze_without_token(client):
    payload = {
        "entrance": "A1",
        "gridSize": "8x8",
        "walls": [
            "C1",
            "G1",
            "A2",
            "C2",
            "E2",
            "G2",
            "C3",
            "E3",
            "B4",
            "C4",
            "E4",
            "F4",
            "G4",
            "B5",
            "E5",
            "B6",
            "D6",
            "E6",
            "G6",
            "H6",
            "B7",
            "D7",
            "G7",
            "B8",
        ],
    }
    maze_response = create_maze(client, payload)
    assert maze_response.status_code == 401
    assert maze_response.json == {"message": "Token is missing"}


def test_create_maze_with_invalid_token(client):
    payload = {
        "entrance": "A1",
        "gridSize": "8x8",
        "walls": [
            "C1",
            "G1",
            "A2",
            "C2",
            "E2",
            "G2",
            "C3",
            "E3",
            "B4",
            "C4",
            "E4",
            "F4",
            "G4",
            "B5",
            "E5",
            "B6",
            "D6",
            "E6",
            "G6",
            "H6",
            "B7",
            "D7",
            "G7",
            "B8",
        ],
    }
    token = get_token(client)
    token += "a"
    maze_response = create_maze(client, payload, token)
    assert maze_response.status_code == 401
    assert maze_response.json == {"message": "Token is invalid"}


def test_get_mazes_without_token(client):
    maze_response = get_mazes(client)
    assert maze_response.status_code == 401
    assert maze_response.json == {"message": "Token is missing"}


def test_get_mazes_with_invalid_token(client):
    token = get_token(client)
    token += "a"
    maze_response = get_mazes(client, token=token)
    assert maze_response.status_code == 401
    assert maze_response.json == {"message": "Token is invalid"}


def test_get_maze_without_token(client):
    maze_response = get_maze_path(client, "1")
    assert maze_response.status_code == 401
    assert maze_response.json == {"message": "Token is missing"}


def test_get_maze_with_invalid_token(client):
    token = get_token(client)
    token += "a"
    maze_response = get_maze_path(client, "1", token=token)
    assert maze_response.status_code == 401
    assert maze_response.json == {"message": "Token is invalid"}


def test_create_maze(client):
    payload = {
        "entrance": "A1",
        "gridSize": "8x8",
        "walls": [
            "C1",
            "G1",
            "A2",
            "C2",
            "E2",
            "G2",
            "C3",
            "E3",
            "B4",
            "C4",
            "E4",
            "F4",
            "G4",
            "B5",
            "E5",
            "B6",
            "D6",
            "E6",
            "G6",
            "H6",
            "B7",
            "D7",
            "G7",
            "B8",
        ],
    }
    token = get_token(client)
    maze_response = create_maze(client, payload, token)
    assert maze_response.status_code == 201
    assert maze_response.json["maze_id"]


def test_create_maze_with_missing_entrance_field(client):
    payload = {
        "gridSize": "8x8",
        "walls": [
            "C1",
            "G1",
            "A2",
            "C2",
            "E2",
            "G2",
            "C3",
            "E3",
            "B4",
            "C4",
            "E4",
            "F4",
            "G4",
            "B5",
            "E5",
            "B6",
            "D6",
            "E6",
            "G6",
            "H6",
            "B7",
            "D7",
            "G7",
            "B8",
        ],
    }
    token = get_token(client)
    maze_response = create_maze(client, payload, token)
    assert maze_response.status_code == 401
    assert maze_response.json == {"message": "Field(s) missing: entrance"}


def test_create_maze_with_missing_walls_field(client):
    payload = {
        "entrance": "A1",
        "gridSize": "8x8",
    }
    token = get_token(client)
    maze_response = create_maze(client, payload, token)
    assert maze_response.status_code == 401
    assert maze_response.json == {"message": "Field(s) missing: walls"}


def test_create_maze_with_missing_grid_size_field(client):
    payload = {
        "entrance": "A1",
        "walls": [
            "C1",
            "G1",
            "A2",
            "C2",
            "E2",
            "G2",
            "C3",
            "E3",
            "B4",
            "C4",
            "E4",
            "F4",
            "G4",
            "B5",
            "E5",
            "B6",
            "D6",
            "E6",
            "G6",
            "H6",
            "B7",
            "D7",
            "G7",
            "B8",
        ],
    }

    token = get_token(client)
    maze_response = create_maze(client, payload, token)
    assert maze_response.status_code == 401
    assert maze_response.json == {"message": "Field(s) missing: grid_size"}


def test_create_maze_with_misspelled_or_different_fields(client):
    payload = {
        "test_additional_field": "A1",
        "entrance": "A1",
        "gridSize": "8x8",
        "walls": [
            "C1",
            "G1",
            "A2",
            "C2",
            "E2",
            "G2",
            "C3",
            "E3",
            "B4",
            "C4",
            "E4",
            "F4",
            "G4",
            "B5",
            "E5",
            "B6",
            "D6",
            "E6",
            "G6",
            "H6",
            "B7",
            "D7",
            "G7",
            "B8",
        ],
    }
    token = get_token(client)
    maze_response = create_maze(client, payload, token)
    assert maze_response.status_code == 401
    assert maze_response.json == {
        "message": "Field(s) redundant: test_additional_field"
    }


def test_no_solution_specified(client):
    payload = {"entrance": "A1", "gridSize": "8x8",
               "walls": ["C1", "G1", "A2"]}
    token = get_token(client)
    create_maze(client, payload, token)
    get_maze = get_maze_path(client, token=token)
    assert get_maze.status_code == 400
    assert get_maze.json == {"message": "Solution not in: min, max"}


def test_should_catch_invalid_entrance_field(client):
    payload = {"entrance": "AA", "gridSize": "8x8",
               "walls": ["C1", "G1", "A2"]}
    token = get_token(client)
    create_maze_res = create_maze(client, payload, token)
    assert create_maze_res.status_code == 401
    assert create_maze_res.json == {
        "message": "Entrance format is wrong, letter-int was expected"
    }


def test_should_catch_invalid_grid_size_field(client):
    payload = {"entrance": "A1", "gridSize": "88", "walls": ["C1", "G1", "A2"]}
    token = get_token(client)
    create_maze_res = create_maze(client, payload, token)
    assert create_maze_res.status_code == 401
    assert create_maze_res.json == {
        "message": "Grid size format is wrong, int-x-int was expected"
    }


def test_no_path_found(client):
    payload = {
        "entrance": "A1",
        "gridSize": "8x8",
        "walls": [
            "C1",
            "G1",
            "A2",
            "C2",
            "E2",
            "G2",
            "C3",
            "E3",
            "B4",
            "C4",
            "E4",
            "F4",
            "G4",
            "B5",
            "E5",
            "B6",
            "D6",
            "E6",
            "G6",
            "H6",
            "B7",
            "D7",
            "G7",
            "B8",
        ],
    }
    token = get_token(client)
    create_res = create_maze(client, payload, token)
    get_maze = get_maze_path(client, maze_id=create_res.json["maze_id"],
                             solution_type="min",
                             token=token)
    assert get_maze.status_code == 400
    assert get_maze.json == {"message": "No path found"}


def test_should_handle_non_existing_maze(client):
    token = get_token(client)
    get_maze = get_maze_path(client, maze_id="10", solution_type="min",
                             token=token)
    assert get_maze.status_code == 400
    assert get_maze.json == {'message': 'No maze with such id'}


def test_get_shortest_and_longest_path_of_maze(client):
    payload = {"entrance": "A1", "gridSize": "8x8",
               "walls": ["C1", "G1", "A2"]}
    token = get_token(client)
    create_res = create_maze(client, payload, token)
    shortest_path = get_maze_path(
        client,
        maze_id=create_res.json["maze_id"],
        solution_type="min",
        token=token
    )
    assert shortest_path.json == {
        "path": [
            "A1",
            "B1",
            "B2",
            "B3",
            "B4",
            "B5",
            "B6",
            "B7",
            "B8",
            "C8",
            "D8",
            "E8",
            "F8",
            "G8",
            "H8",
        ]
    }

    longest_path = get_maze_path(
        client,
        maze_id=create_res.json["maze_id"],
        solution_type="max",
        token=token
    )
    assert longest_path.json == {
        "path": [
            "A1",
            "B1",
            "B2",
            "C2",
            "D2",
            "E2",
            "F2",
            "G2",
            "H2",
            "H3",
            "G3",
            "F3",
            "E3",
            "D3",
            "C3",
            "B3",
            "A3",
            "A4",
            "B4",
            "C4",
            "D4",
            "E4",
            "F4",
            "G4",
            "H4",
            "H5",
            "G5",
            "F5",
            "E5",
            "D5",
            "C5",
            "B5",
            "A5",
            "A6",
            "B6",
            "C6",
            "D6",
            "E6",
            "F6",
            "G6",
            "H6",
            "H7",
            "G7",
            "F7",
            "E7",
            "D7",
            "C7",
            "B7",
            "A7",
            "A8",
            "B8",
            "C8",
            "D8",
            "E8",
            "F8",
            "G8",
            "H8",
        ]
    }


def test_get_user_specific_mazes(client):
    payload = {"entrance": "A1", "gridSize": "8x8",
               "walls": ["C1", "G1", "A2"]}

    first_user_token = get_token(client)
    create_maze(client, payload, first_user_token)
    create_maze(client, payload, first_user_token)
    create_maze(client, payload, first_user_token)

    second_user_token = get_token(
        client, creds={"name": "happyUser222", "password": "iTk19!n"}
    )
    create_maze(client, payload, second_user_token)
    create_maze(client, payload, second_user_token)
    create_maze(client, payload, second_user_token)

    first_user_mazes_res = get_mazes(client, first_user_token)
    second_user_mazes_res = get_mazes(client, second_user_token)

    assert len(first_user_mazes_res.json) == 3
    assert len(second_user_mazes_res.json) == 3


def test_get_mazes(client):
    payload = {"entrance": "A1", "gridSize": "8x8",
               "walls": ["C1", "G1", "A2"]}

    first_user_token = get_token(client)
    create_maze(client, payload, first_user_token)
    create_maze(client, payload, first_user_token)
    create_maze(client, payload, first_user_token)

    mazes = get_mazes(client, first_user_token).json
    for maze in mazes:
        assert list(maze.keys()) == ['entrance', 'grid_size',
                                     'public_id', 'user_id', 'walls']

