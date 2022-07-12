from flask import Flask, jsonify
from werkzeug.utils import import_string

from controllers.auth import auth
from controllers.maze import maze
from db.database import db
from exceptions.exceptions import BaseAppException


def create_app(config_path="config.DevConfig", drop_db=False):
    app = Flask(__name__)
    cfg = import_string(config_path)()
    app.config.from_object(cfg)

    # routes
    app.register_blueprint(auth)
    app.register_blueprint(maze)

    @app.errorhandler(BaseAppException)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    db.init_app(app)
    with app.app_context():
        if drop_db:
            db.session.remove()
            db.drop_all()
        db.create_all()

    return app


app = create_app("config.ProdConfig")

if __name__ == "__main__":
    # setting debug to True enables hot reload
    # and also provides a debugger shell
    # if you hit an error while running the server
    app.run(debug=True)
