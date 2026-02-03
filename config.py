import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY = "8cb2237d0679ca88db6464eac60da96345513964"
    SQLALCHEMY_DATABASE_URI = "sqlite:///blog.db"
    SQLALCHEMY_TRACK_NOTIFICATIONS = False

class DevelopmentConfig(Config):

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'development.db')}"

    @staticmethod
    def validate():
        Config.validate_config()
        print("Using SQLite for development")

class TestingConfig(Config):

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URI",
        "sqlite:///:memory"
    )

    @staticmethod
    def validate():
        Config.validate_config()
        if not os.getenv("TEST_DATABASE_URI"):
            print("Using SQLite for testing.")

class ProductionConfig(Config):

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI",
       f"postgresql://{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', 'admin93')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'members')}"
    )

    @staticmethod
    def validate():
        Config.validate_config()
        if not os.getenv("DATABASE_URI"):
            raise ValueError("DATABASE_URI not configured. Using PostgreSQL by default")