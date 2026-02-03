from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import Member, db

def create_app():

    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    login_manager = LoginManager(app)
    migrate = Migrate(app, db)
    csrf = CSRFProtect(app)
    db.init_app(app)

    @login_manager.user_loader
    def load_user(member_id):

        return db.session.get(Member, int(member_id))

    from auth.routes import auth_bp
    from admin.routes import admin_bp
    from main.routes import main_bp
    from user.routes import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)

    return app

if __name__ == '__main__':

    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)