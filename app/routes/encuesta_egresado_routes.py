# Endpoints relacionados con encuestas de egresados
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from ..models.encuesta_egresado import EncuestaEgresado
from ..models.schemas import EncuestaEgresadoSchema, EncuestaEgresadoUpdateSchema
from ..services.encuesta_egresado_service import (
    crear_encuesta, obtener_encuestas, obtener_encuesta,
    actualizar_encuesta, eliminar_encuesta_logica, obtener_estadisticas_encuestas ,restaurar_encuesta_logica
)
from ..services.usuario_service import require_auth
from .. import db

# Crear Blueprint para rutas de encuestas con prefijo /api/crud
encuesta_egresado_bp = Blueprint('encuesta_egresado', __name__, url_prefix='/api/crud')


@encuesta_egresado_bp.route('/encuestas-egresados', methods=['GET'])
def listar_encuestas():
    """Obtener lista de encuestas de egresados con paginación"""

    # Filtros RAW desde querystring
    raw_codigo = request.args.get('codigo_egresado')
    raw_trabaja = request.args.get('trabaja_actualmente')
    raw_negocio = request.args.get('tiene_negocio')
    raw_estado = request.args.get('estado')

    # Paginación
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    # === Helper para booleanos ===
    def parse_bool(v):
        if v is None:
            return None
        v = v.strip().lower()
        if v in ("1", "true", "si", "yes", "y"): return True
        if v in ("0", "false", "no", "n"): return False
        return None

    # === Armar diccionario limpio de filtros ===
    filtros = {}

    if raw_codigo and raw_codigo.strip() != "":
        filtros["codigo_egresado"] = raw_codigo.strip()

    tb = parse_bool(raw_trabaja)
    if tb is not None:
        filtros["trabaja_actualmente"] = tb

    tn = parse_bool(raw_negocio)
    if tn is not None:
        filtros["tiene_negocio"] = tn

    if raw_estado:
        est = raw_estado.strip().upper()
        if est in ("A", "I"):
            filtros["estado"] = est

    # Servicio
    encuestas = obtener_encuestas(filtros, page, per_page)
    return jsonify(encuestas)


@encuesta_egresado_bp.route('/encuestas-egresados', methods=['POST'])
@require_auth
def agregar_encuesta():
    """Agregar nueva encuesta de egresado"""
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No se proporcionaron datos'}), 400

    # Validar datos usando Marshmallow
    schema = EncuestaEgresadoSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify({'message': 'Error de validación', 'errors': err.messages}), 400

    resultado, codigo_respuesta = crear_encuesta(validated_data)
    return jsonify(resultado), codigo_respuesta


@encuesta_egresado_bp.route('/encuestas-egresados/<int:id_encuesta>', methods=['GET'])
def obtener_una_encuesta(id_encuesta):
    """Obtener una encuesta específica"""
    resultado, codigo_respuesta = obtener_encuesta(id_encuesta)
    return jsonify(resultado), codigo_respuesta


@encuesta_egresado_bp.route('/encuestas-egresados/<int:id_encuesta>', methods=['PUT'])
@require_auth
def editar_encuesta(id_encuesta):
    """Editar encuesta existente"""
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No se proporcionaron datos'}), 400

    # Validar datos usando Marshmallow (todos los campos opcionales en actualización)
    schema = EncuestaEgresadoUpdateSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify({'message': 'Error de validación', 'errors': err.messages}), 400

    resultado, codigo_respuesta = actualizar_encuesta(id_encuesta, validated_data)
    return jsonify(resultado), codigo_respuesta


@encuesta_egresado_bp.route('/encuestas-egresados/<int:id_encuesta>', methods=['DELETE'])
@require_auth
def eliminar_encuesta(id_encuesta):
    """Eliminar encuesta lógicamente"""
    resultado, codigo_respuesta = eliminar_encuesta_logica(id_encuesta)
    return jsonify(resultado), codigo_respuesta

@encuesta_egresado_bp.route('/encuestas-egresados/restaurar/<int:id_encuesta>', methods=['PATCH'])
@require_auth
def restaurar_encuesta(id_encuesta):
    """Eliminar encuesta lógicamente"""
    resultado, codigo_respuesta = restaurar_encuesta_logica(id_encuesta)
    return jsonify(resultado), codigo_respuesta


@encuesta_egresado_bp.route('/encuestas-egresados/estadisticas', methods=['GET'])
def estadisticas_encuestas():
    """Obtener estadísticas de encuestas"""
    codigo_egresado = request.args.get('codigo_egresado')
    resultado, codigo_respuesta = obtener_estadisticas_encuestas(
        codigo_egresado)
    return jsonify(resultado), codigo_respuesta
