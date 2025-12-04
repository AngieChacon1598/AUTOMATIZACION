# Inicialización de la aplicación Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.pool import QueuePool
from .settings import SQLALCHEMY_DATABASE_URI

# Inicialización de la app Flask
app = Flask(__name__)

# Configuración CORS - Permitir todos los orígenes
CORS(app)

# Configuración de la base de datos con pool de conexiones y reconexión
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'poolclass': QueuePool,
    'pool_size': 5,
    'max_overflow': 10,
    'pool_pre_ping': True,  # ⭐ IMPORTANTE: Verifica conexiones antes de usarlas
    'pool_recycle': 3600,   # Recicla conexiones cada hora
    'connect_args': {
        'sslmode': 'require',
        'connect_timeout': 10
    }
}
db = SQLAlchemy(app)

# Importar modelos después de inicializar db
from . import models

# Función para registrar blueprints después de que db esté disponible
def register_blueprints():
    """Registrar todos los blueprints después de que db esté disponible"""
    from .routes.usuario_routes import usuario_bp
    from .routes.egresado_routes import egresado_bp
    from .routes.empresa_routes import empresa_bp
    from .routes.certificacion_routes import certificacion_bp
    from .routes.encuesta_egresado_routes import encuesta_egresado_bp
    from .routes.reportes_routes import reportes_bp

    app.register_blueprint(usuario_bp)
    app.register_blueprint(egresado_bp)
    app.register_blueprint(empresa_bp)
    app.register_blueprint(certificacion_bp)
    app.register_blueprint(encuesta_egresado_bp)
    app.register_blueprint(reportes_bp)

# Registrar blueprints
register_blueprints()
