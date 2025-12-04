# Endpoints relacionados con empresas
from flask import Blueprint, request, jsonify
from ..models.empresa import Empresa
from ..services.empresa_service import (
    crear_empresa, obtener_empresas, obtener_empresa,
    actualizar_empresa, eliminar_empresa_logico, restaurar_empresa
)
from ..services.usuario_service import require_auth
from .. import db

# Crear Blueprint para rutas de empresas
empresa_bp = Blueprint('empresa', __name__)

@empresa_bp.route('/empresas', methods=['GET'])
def get_empresas():
    """Obtener lista de empresas con filtros y paginación"""
    filtros = {
        'estado': request.args.get('estado'),
        'nombre': request.args.get('nombre', '').strip(),
        'ruc': request.args.get('ruc', '').strip(),
        'page': request.args.get('page', 1, type=int),
        'per_page': request.args.get('per_page', 10, type=int)
    }
    
    resultado = obtener_empresas(filtros)
    return jsonify(resultado)

@empresa_bp.route('/empresas/<int:id_empresa>', methods=['GET'])
def get_empresa(id_empresa):
    """Obtener una empresa específica"""
    resultado, codigo_respuesta = obtener_empresa(id_empresa)
    return jsonify(resultado), codigo_respuesta

@empresa_bp.route('/empresas', methods=['POST'])
@require_auth
def create_empresa():
    """Crear nueva empresa"""
    data = request.get_json()
    
    if not data.get('nombre') or not data.get('ruc'):
        return jsonify({'message': 'Nombre y RUC son requeridos'}), 400

    resultado, codigo_respuesta = crear_empresa(data)
    return jsonify(resultado), codigo_respuesta

@empresa_bp.route('/empresas/<int:id_empresa>', methods=['PUT'])
@require_auth
def update_empresa(id_empresa):
    """Actualizar empresa existente"""
    data = request.get_json()
    
    resultado, codigo_respuesta = actualizar_empresa(id_empresa, data)
    return jsonify(resultado), codigo_respuesta

@empresa_bp.route('/empresas/<int:id_empresa>', methods=['DELETE'])
@require_auth
def delete_empresa(id_empresa):
    """Eliminar empresa lógicamente"""
    resultado, codigo_respuesta = eliminar_empresa_logico(id_empresa)
    return jsonify(resultado), codigo_respuesta

@empresa_bp.route('/empresas/restaurar/<int:id_empresa>', methods=['PUT'])
@require_auth
def restaurar_empresa_route(id_empresa):
    """Restaurar empresa eliminada lógicamente"""
    from ..services.empresa_service import restaurar_empresa
    resultado, codigo_respuesta = restaurar_empresa(id_empresa)
    return jsonify(resultado), codigo_respuesta

