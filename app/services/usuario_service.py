# Lógica y operaciones sobre usuarios
from datetime import datetime, timedelta
from flask import request
import jwt
from ..models.usuario import Usuario
from ..settings import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_HOURS

def generate_token(user):
    """Genera un token JWT para el usuario"""
    payload = {
        'user_id': user.id_usuario,
        'username': user.username,
        'rol': user.rol,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def verify_token(token):
    """Verifica y decodifica un token JWT"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_current_user():
    """Obtiene el usuario actual desde el token JWT"""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    
    try:
        token = auth_header.split(' ')[1]  # Formato: "Bearer <token>"
        payload = verify_token(token)
        if payload:
            user = Usuario.query.get(payload['user_id'])
            if user and user.estado == 'A':
                return user
    except:
        pass
    return None

def require_auth(f):
    """Decorador para requerir autenticación"""
    from functools import wraps
    
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user:
            return {'error': 'Token requerido'}, 401
        return f(*args, **kwargs)
    return decorated

def require_admin(f):
    """Decorador para requerir rol de administrador"""
    from functools import wraps
    
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user:
            return {'error': 'Token requerido'}, 401
        if user.rol != 'admin':
            return {'error': 'Acceso denegado. Se requiere rol de administrador'}, 403
        return f(*args, **kwargs)
    return decorated

