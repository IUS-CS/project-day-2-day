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