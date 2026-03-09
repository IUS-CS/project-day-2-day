# app.py
# This does the initialization and execution of the application
# Uses Flask for it all.
# Important note: Serves as the primary backend service for the application
# Delivers frontend pages as well.

from flask import Flask, render_template

# Corrected imports — use calendar_app.* because THAT is your package
from calendar_app.routes.main_routes import main_bp
from calendar_app.routes.notes_routes import notes_bp

# Import blueprint factories
from calendar_app.api.admin_api import create_admin_api
from calendar_app.api.profile_api import create_profile_api

# Import DB + repositories
from calendar_app.data.db import init_db
from calendar_app.data.user_repo import UserRepo
from calendar_app.data.profile_repo import ProfileRepo

# Import services
from calendar_app.logic.admin_service import AdminService
from calendar_app.logic.profile_service import ProfileService


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Initialize database
    SessionFactory = init_db()

    # Instantiate repositories (DB-backed)
    user_repo = UserRepo(SessionFactory)
    profile_repo = ProfileRepo(SessionFactory)

    # Instantiate services
    admin_service = AdminService(user_repo, profile_repo)
    profile_service = ProfileService(profile_repo)

    # Register API blueprints with injected services
    app.register_blueprint(create_admin_api(admin_service))
    app.register_blueprint(create_profile_api(profile_service))

    # Register blueprints (these contain the REAL index route)
    app.register_blueprint(main_bp)
    app.register_blueprint(notes_bp)

    # Calendar grid route
    @app.route("/calendar/grid")
    def calendar_grid_view():
        return render_template("calendar_grid.html")

    return app


# IMPORTANT:
# When running as a module (`python -m calendar_app.app`),
# __name__ will NOT be "__main__".
# So we must still allow the app to run.
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)