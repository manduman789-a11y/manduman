import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from redis import Redis
from dotenv import load_dotenv

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    load_dotenv()
    app = Flask(__name__, static_folder="static", template_folder="templates")

    # 기본 설정
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

    # DB (ProxySQL 경유 MySQL)
    db_user = os.getenv("DB_USER", "app_admin")
    db_password = os.getenv("DB_PASSWORD", "AppAdmin12#$")
    db_host = os.getenv("DB_HOST", "192.168.11.109")
    db_port = os.getenv("DB_PORT", "6033")
    db_name = os.getenv("DB_NAME", "web_db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 세션 (Redis 공유)
    r_host = os.getenv("REDIS_HOST", "192.168.11.101")
    r_port = int(os.getenv("REDIS_PORT", "6379"))
    r_db = int(os.getenv("REDIS_DB", "1"))
    r_pw = os.getenv("REDIS_PASSWORD", "redis_admin")

    app.config["SESSION_TYPE"] = "redis"
    app.config["SESSION_REDIS"] = Redis(host=r_host, port=r_port, db=r_db, password=r_pw)
    app.config["SESSION_PERMANENT"] = False
    Session(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # 블루프린트
    from .auth import auth_bp
    from .views import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # CLI 유틸
    register_cli(app)

    return app

def register_cli(app):
    from .models import User, Post, Comment
    from werkzeug.security import generate_password_hash

    @app.cli.command("db_init")
    def db_init():
        """최초 테이블 생성"""
        with app.app_context():
            db.create_all()
            print("Tables created.")

    @app.cli.command("create_admin")
    def create_admin():
        """관리자 계정 생성: FLASK_APP=app flask create_admin email password"""
        import click
        @click.argument("email")
        @click.argument("password")
        def run(email, password):
            with app.app_context():
                if User.query.filter_by(email=email).first():
                    print("Already exists.")
                    return
                u = User(email=email, name="Admin", password_hash=generate_password_hash(password))
                db.session.add(u)
                db.session.commit()
                print("Admin created.")
        return run()

    @app.cli.command("create_demo")
    def create_demo():
        from .models import User, Post, Comment
        from werkzeug.security import generate_password_hash
        with app.app_context():
            u = User.query.filter_by(email="demo@example.com").first()
            if not u:
                u = User(email="demo@example.com", name="Demo", password_hash=generate_password_hash("Demo12#$"))
                db.session.add(u); db.session.commit()
            p = Post(title="첫 글", body="flask-board 데모 포스트", author_id=u.id)
            db.session.add(p); db.session.commit()
            c = Comment(body="댓글 테스트", author_id=u.id, post_id=p.id)
            db.session.add(c); db.session.commit()
            print("Demo created.")
