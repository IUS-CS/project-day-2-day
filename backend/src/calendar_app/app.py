# app.py
# This does the initialization and execution of the application
# Uses Flask for it all.
# Important note: Serves as the primary backend service for the application
# Delivers frontend pages as well.

from flask import Flask
from backend.src.calendar_app.routes.main_routes import main_bp
from backend.src.calendar_app.routes.notes_routes import notes_bp


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(notes_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)