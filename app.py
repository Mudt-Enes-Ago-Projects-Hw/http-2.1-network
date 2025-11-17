from flask import Flask
from src.config.settings import Config
from src.models.db import db, create_tables
from src.controllers.auth_controller import auth_bp
from src.controllers.blog_controller import blog_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        create_tables()
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(port=app.config['PORT'], debug=True)