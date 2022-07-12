from exceptions.exceptions import MazeException, GridGeneratorException
from maze.maze_game import GridGenerator


def test_generate_grid():
    gg = GridGenerator(grid_size="3x3", walls=["A2", "B2"])
    assert gg.generate_new_grid() == [["M", "W", "M"], ["M", "W", "M"], ["M", "M", "M"]]


def test_unique_grid_generation():
    gg = GridGenerator(grid_size="3x3", walls=["A2", "B2"])
    first_grid = gg.generate_new_grid()
    first_grid[0][2] = "W"
    assert first_grid != gg.generate_new_grid()


def test_shouldnt_generate_maze_beyond_limits():
    try:
        GridGenerator(grid_size="30x30", walls=["A2", "B2"])
        assert False
    except GridGeneratorException as e:
        assert e.message == "Maze should be no bigger than 26"
