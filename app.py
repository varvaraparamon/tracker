from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from models import db, User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Blueprints
    from routes.auth import auth_bp
    from routes.team_eval import team_eval_bp
    from routes.indiv_eval import indiv_eval_bp
    from routes.transcribe import transcribe_bp
    from routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(team_eval_bp, url_prefix="/team")
    app.register_blueprint(indiv_eval_bp, url_prefix="/individual")
    app.register_blueprint(transcribe_bp, url_prefix="/transcribator")
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
