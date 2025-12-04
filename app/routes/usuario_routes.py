# Endpoints relacionados con usuarios
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from ..models.usuario import Usuario
from ..models.schemas import UsuarioSchema, LoginSchema
from ..services.usuario_service import generate_token, verify_token, get_current_user, require_auth, require_admin
from .. import db

# Crear Blueprint para rutas de usuarios
usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/api/auth/register', methods=['POST'])
def register():
    """Registrar nuevo usuario"""
    try:
        data = request.get_json()
        
        # Validar datos
        schema = UsuarioSchema()
        try:
            validated_data = schema.load(data)
        except ValidationError as err:
            return jsonify({'message': 'Error de validación', 'errors': err.messages}), 400
        
        # Verificar que el username no exista
        if Usuario.query.filter_by(username=validated_data['username']).first():
            return jsonify({'message': 'El nombre de usuario ya existe'}), 400
        
        # Verificar que el email no exista
        if Usuario.query.filter_by(email=validated_data['email']).first():
            return jsonify({'message': 'El email ya está registrado'}), 400
        
        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            nombre=validated_data['nombre'],
            apellidos=validated_data['apellidos'],
            rol=validated_data.get('rol', 'usuario')
        )
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        # Generar token
        token = generate_token(nuevo_usuario)
        
        return jsonify({
            'message': 'Usuario registrado exitosamente',
            'token': token,
            'user': nuevo_usuario.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error interno del servidor: {str(e)}'}), 500

@usuario_bp.route('/api/auth/login', methods=['POST'])
def login():
    """Iniciar sesión"""
    try:
        data = request.get_json()
        
        # Validar datos
        schema = LoginSchema()
        try:
            validated_data = schema.load(data)
        except ValidationError as err:
            return jsonify({'message': 'Error de validación', 'errors': err.messages}), 400
        
        # Buscar usuario
        user = Usuario.query.filter_by(username=validated_data['username']).first()
        
        if not user:
            return jsonify({'message': 'Credenciales inválidas'}), 401
        
        # Verificar si la cuenta está bloqueada
        if user.is_locked():
            return jsonify({'message': 'Cuenta bloqueada por múltiples intentos fallidos'}), 401
        
        # Verificar contraseña
        if not user.check_password(validated_data['password']):
            user.increment_login_attempts()
            return jsonify({'message': 'Credenciales inválidas'}), 401
        
        # Login exitoso
        user.reset_login_attempts()
        
        # Generar token
        token = generate_token(user)
        
        return jsonify({
            'message': 'Login exitoso',
            'token': token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error interno del servidor: {str(e)}'}), 500

@usuario_bp.route('/api/auth/profile', methods=['GET'])
@require_auth
def get_profile():
    """Obtener perfil del usuario actual"""
    user = get_current_user()
    return jsonify({'user': user.to_dict()}), 200

@usuario_bp.route('/api/auth/profile', methods=['PUT'])
@require_auth
def update_profile():
    """Actualizar perfil del usuario actual"""
    try:
        user = get_current_user()
        data = request.get_json()
        
        # Campos que se pueden actualizar
        updatable_fields = ['nombre', 'apellidos', 'email']
        
        for field in updatable_fields:
            if field in data:
                if field == 'email':
                    # Verificar que el email no esté en uso por otro usuario
                    existing_user = Usuario.query.filter(
                        Usuario.email == data[field],
                        Usuario.id_usuario != user.id_usuario
                    ).first()
                    if existing_user:
                        return jsonify({'message': 'El email ya está en uso'}), 400
                setattr(user, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Perfil actualizado exitosamente',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error al actualizar perfil', 'error': str(e)}), 500

@usuario_bp.route('/api/auth/change-password', methods=['POST'])
@require_auth
def change_password():
    """Cambiar contraseña del usuario actual"""
    try:
        user = get_current_user()
        data = request.get_json()
        
        if not data.get('current_password') or not data.get('new_password'):
            return jsonify({'message': 'Contraseña actual y nueva son requeridas'}), 400
        
        # Verificar contraseña actual
        if not user.check_password(data['current_password']):
            return jsonify({'message': 'Contraseña actual incorrecta'}), 400
        
        # Validar nueva contraseña
        if len(data['new_password']) < 6:
            return jsonify({'message': 'La nueva contraseña debe tener al menos 6 caracteres'}), 400
        
        # Cambiar contraseña
        user.set_password(data['new_password'])
        db.session.commit()
        
        return jsonify({'message': 'Contraseña cambiada exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error al cambiar contraseña', 'error': str(e)}), 500

@usuario_bp.route('/api/auth/create-admin', methods=['POST'])
def create_admin():
    """Crear usuario administrador por defecto (solo para desarrollo)"""
    try:
        # Verificar si ya existe un admin
        admin_exists = Usuario.query.filter_by(rol='admin').first()
        if admin_exists:
            return jsonify({'message': 'Ya existe un usuario administrador'}), 400
        
        # Crear admin por defecto
        admin = Usuario(
            username='admin',
            email='admin@admin.com',
            password='admin123',
            nombre='Administrador',
            apellidos='Sistema',
            rol='admin'
        )
        
        db.session.add(admin)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuario administrador creado exitosamente',
            'user': admin.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error al crear administrador', 'error': str(e)}), 500

@usuario_bp.route('/api/auth/verify-token', methods=['POST'])
def verify_token_endpoint():
    """Verificar si un token es válido"""
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({'valid': False, 'message': 'Token no proporcionado'}), 400
        
        payload = verify_token(token)
        if payload:
            user = Usuario.query.get(payload['user_id'])
            if user and user.estado == 'A':
                return jsonify({'valid': True, 'user': user.to_dict()}), 200
        
        return jsonify({'valid': False, 'message': 'Token inválido o expirado'}), 401
        
    except Exception as e:
        return jsonify({'valid': False, 'message': f'Error: {str(e)}'}), 500
