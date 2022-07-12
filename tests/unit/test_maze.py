from exceptions.exceptions import MazeException
from maze.maze_game import MazeGame


def test_find_shortest_and_longest_path():
    """
    'M', 'W', 'M', 'M', 'M', 'M', 'M', 'M'
    'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M'
    'W', 'W', 'M', 'M', 'M', 'M', 'M', 'M'
    'M', 'W', 'M', 'M', 'M', 'M', 'M', 'M'
    'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M'
    'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M'
    'W', 'M', 'M', 'M', 'M', 'M', 'M', 'M'
    'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M'
    """
    walls = ["C1", "G1", "A2", "C2", "D2"]
    m = MazeGame(entrance="A1", grid_size="8x8", walls=walls)

    assert m.shortest_path() == {
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
    assert m.shortest_path(False) == {
        "path": [
            "A1",
            "B1",
            "B2",
            "B3",
            "C3",
            "D3",
            "E3",
            "F3",
            "G3",
            "H3",
            "H4",
            "G4",
            "F4",
            "E4",
            "D4",
            "C4",
            "B4",
            "A4",
            "A5",
            "B5",
            "C5",
            "D5",
            "E5",
            "F5",
            "G5",
            "H5",
            "H6",
            "G6",
            "F6",
            "E6",
            "D6",
            "C6",
            "B6",
            "A6",
            "A7",
            "B7",
            "C7",
            "D7",
            "E7",
            "F7",
            "G7",
            "H7",
            "H8",
        ]
    }


def test_find_shortest_and_longest_path_without_walls():
    m = MazeGame(entrance="A1", grid_size="8x8", walls=[])

    assert m.shortest_path() == {
        "path": [
            "A1",
            "A2",
            "A3",
            "A4",
            "A5",
            "A6",
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
    assert m.shortest_path(False) == {
        "path": [
            "A1",
            "B1",
            "C1",
            "D1",
            "E1",
            "F1",
            "G1",
            "H1",
            "H2",
            "G2",
            "F2",
            "E2",
            "D2",
            "C2",
            "B2",
            "A2",
            "A3",
            "B3",
            "C3",
            "D3",
            "E3",
            "F3",
            "G3",
            "H3",
            "H4",
            "G4",
            "F4",
            "E4",
            "D4",
            "C4",
            "B4",
            "A4",
            "A5",
            "B5",
            "C5",
            "D5",
            "E5",
            "F5",
            "G5",
            "H5",
            "H6",
            "G6",
            "F6",
            "E6",
            "D6",
            "C6",
            "B6",
            "A6",
            "A7",
            "B7",
            "C7",
            "D7",
            "E7",
            "F7",
            "G7",
            "H7",
            "H8",
        ]
    }


def test_return_no_path_found_when_no_possible_path():
    try:
        walls = ["A2", "B1"]
        m = MazeGame(entrance="A1", grid_size="8x8", walls=walls)
        m.shortest_path()
        assert False
    except MazeException as e:
        assert e.message == "No path found"


def test_target_over_grid_limits():
    try:
        walls = ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8"]
        MazeGame(entrance="A1", grid_size="8x8", walls=walls)
        assert False
    except MazeException as e:
        assert e.message == "Target over grid limit"
