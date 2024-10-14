from flask import Flask
import routes
import middlewares
from infrastructure.settings.parsers import load_config
from infrastructure.database.session import create_session_maker


def main() -> Flask:
    config = load_config()
    session_maker = create_session_maker(config.db_config.full_url)

    app = Flask(__name__)
    middlewares.register(app, session_maker)
    routes.register(app)

    return app


def run():
    app = main()
    app.run("0.0.0.0", 9000, debug=True)


if __name__ == "__main__":
    run()