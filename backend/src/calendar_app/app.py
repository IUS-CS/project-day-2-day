#app.py
# This does the initiliazation and execution of the application
# Uses Flask for it all.
# Important note: Serves as the primary backend service for the the application
# Delivers frontend pages as well.

from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    # Home route
    @app.route("/")
    def index():
        return render_template("index.html")

    # Calendar route
    @app.route("/calendar")
    def calendar_view():
        return render_template("calendar.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)