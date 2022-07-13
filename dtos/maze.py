class MazeDTO:
    __slots__ = ("entrance", "grid_size", "walls", "user_id", "public_id")

    def __init__(self, entrance, grid_size, walls, public_id=None,
                 user_id=None):
        self.public_id = public_id
        self.user_id = user_id
        self.walls = walls
        self.grid_size = grid_size
        self.entrance = entrance
