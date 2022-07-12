import json

from flask import Blueprint

from constants import SOLUTIONS
from db.database import db
from dtos.mappers import MazeMapper
from flask import request, jsonify, make_response

from exceptions.exceptions import BaseAppException
from maze.maze_game import MazeGame
from models.maze import Maze
from utils.funcs import token_required

maze = Blueprint("maze", __name__)


@maze.route("/maze", methods=["POST"])
@token_required
def create_maze(current_user):
    mapped_maze = MazeMapper.map_2_dto(request.json)
    new_maze = Maze(
        grid_size=mapped_maze.grid_size,
        walls=mapped_maze.walls,
        entrance=mapped_maze.entrance,
        user_id=current_user.id,
    )
    db.session.add(new_maze)
    db.session.commit()

    return make_response({"maze_id": new_maze.id}, 201)


@maze.route("/maze/<maze_id>", methods=["GET"])
@token_required
def get_maze(_, maze_id):
    solution = request.args.get("solution")
    if solution not in SOLUTIONS:
        raise BaseAppException(f"Solution not in: {', '.join(SOLUTIONS)}")

    m = Maze.query.filter_by(id=maze_id).first()
    mg = MazeGame(
        entrance=m.entrance, grid_size=m.grid_size, walls=json.loads(m.walls)
    )
    path = mg.shortest_path(True if solution == "min" else False)
    return make_response(jsonify(path), 200)


@maze.route("/maze", methods=["GET"])
@token_required
def get_mazes(current_user):
    mazes = Maze.query.filter_by(user_id=current_user.id).all()
    return make_response(
        jsonify([MazeMapper.db_2_payload(m) for m in mazes]), 200
    )
