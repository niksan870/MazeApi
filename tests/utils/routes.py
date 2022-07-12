class AuthRoutes:
    SIGNIN = "/login"
    SIGNUP = "/user"


class MazeRoutes:
    BASE = "/maze"

    def get_maze(self, maze_id, solution_type):
        return (
            f"{self.BASE}/{maze_id}?solution={solution_type}"
            if solution_type
            else f"maze/{maze_id}"
        )
