class MazeDTO:
    __slots__ = ("entrance", "grid_size", "walls", "user_id")

    def __init__(self, entrance, grid_size, walls, user_id=None):
        self.user_id = user_id
        self.walls = walls
        self.grid_size = grid_size
        self.entrance = entrance
