import os
import sys

from flask import Flask

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.config import config_by_name


def create_app(config_name: str | None = None) -> Flask:
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    config_class = config_by_name.get(config_name, config_by_name["default"])

    app = Flask(
        __name__,
        template_folder=os.path.abspath(
            os.path.join(os.path.dirname(__file__), "templates")
        ),
        static_folder=os.path.abspath(
            os.path.join(os.path.dirname(__file__), "static")
        ),
    )
    app.config.from_object(config_class)

    from src.routes.api_routes import api_bp
    from src.routes.task_routes import tasks_bp

    app.register_blueprint(tasks_bp)
    app.register_blueprint(api_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)

