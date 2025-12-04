# Modelo de datos para usuarios
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from ..settings import MAX_LOGIN_ATTEMPTS, LOCKOUT_DURATION_MINUTES
import bcrypt

# Importar db desde el módulo principal
from .. import db

class Usuario(db.Model):
    """Modelo de Usuario para autenticación"""
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='usuario')
    estado = db.Column(db.String(1), nullable=False, default='A')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_ultimo_login = db.Column(db.DateTime)
    intentos_login = db.Column(db.Integer, default=0)
    bloqueado_hasta = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        # Extraer password antes de pasar kwargs a super()
        password = kwargs.pop('password', None)
        super(Usuario, self).__init__(**kwargs)
        if password:
            self.set_password(password)

    def set_password(self, password):
        """Hashea y establece la contraseña"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        """Verifica si la contraseña es correcta"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def is_locked(self):
        """Verifica si la cuenta está bloqueada"""
        if self.bloqueado_hasta and self.bloqueado_hasta > datetime.utcnow():
            return True
        return False

    def increment_login_attempts(self):
        """Incrementa los intentos de login fallidos"""
        self.intentos_login += 1
        if self.intentos_login >= MAX_LOGIN_ATTEMPTS:
            self.bloqueado_hasta = datetime.utcnow() + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
        db.session.commit()

    def reset_login_attempts(self):
        """Resetea los intentos de login y desbloquea la cuenta"""
        self.intentos_login = 0
        self.bloqueado_hasta = None
        self.fecha_ultimo_login = datetime.utcnow()
        db.session.commit()

    def to_dict(self):
        """Convierte el usuario a diccionario (sin contraseña)"""
        return {
            'id_usuario': self.id_usuario,
            'username': self.username,
            'email': self.email,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'rol': self.rol,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_ultimo_login': self.fecha_ultimo_login.isoformat() if self.fecha_ultimo_login else None
        }
