from db.database import db


class Maze(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entrance = db.Column(db.String(50))
    grid_size = db.Column(db.String(100))
    walls = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    public_id = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f"Maze({self.id} {self.user_id} {self.entrance} {self.grid_size} {self.walls})"
