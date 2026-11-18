from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.models import Marca, Carro, Opcional
    from app.controllers.main import main_bp
    from app.controllers.marcas import marcas_bp
    from app.controllers.carros import carros_bp
    from app.controllers.opcionais import opcionais_bp
    from app.controllers.relatorios import relatorios_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(marcas_bp, url_prefix="/marcas")
    app.register_blueprint(carros_bp, url_prefix="/carros")
    app.register_blueprint(opcionais_bp, url_prefix="/opcionais")
    app.register_blueprint(relatorios_bp, url_prefix="/relatorios")

    return app
