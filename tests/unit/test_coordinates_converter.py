from maze.maze_game import CoordinatesConverter


def test_can_convert_numeric_2_vocal():
    cc = CoordinatesConverter()
    assert cc.numeric_2_vocal(*(0, 0)) == "A1"
    assert cc.numeric_2_vocal(*(1, 0)) == "B1"
    assert cc.numeric_2_vocal(*(2, 0)) == "C1"


def test_can_convert_vocal_2_numeric():
    cc = CoordinatesConverter()
    assert cc.vocal_2_numeric("A1") == (0, 0)
    assert cc.vocal_2_numeric("B1") == (1, 0)
    assert cc.vocal_2_numeric("C1") == (2, 0)
