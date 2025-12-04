# Endpoints relacionados con egresados
from flask import Blueprint, request, jsonify, render_template
from marshmallow import ValidationError
from sqlalchemy.exc import OperationalError
import time
from ..models.egresado import Egresado
from ..models.detalle_egresado import DetalleEgresado
from ..models.schemas import EgresadoSchema, DetalleEgresadoSchema, EgresadoUpdateSchema, EgresadoConDetalleSchema, EgresadoConDetalleUpdateSchema
from ..services.egresado_service import (
    crear_egresado, obtener_egresados, actualizar_egresado,
    eliminar_egresado_logico, restaurar_egresado, eliminar_egresado_fisico,
    crear_egresado_con_detalle, actualizar_egresado_con_detalle,
    obtener_egresados_con_detalles
)
from ..services.usuario_service import require_auth
from .. import db

# Crear Blueprint para rutas de egresados
egresado_bp = Blueprint('egresado', __name__)

@egresado_bp.route('/egresados', methods=['GET'])
def get_egresados():
    """Obtener lista de egresados con filtros y paginación"""
    filtros = {
        'estado': request.args.get('estado'),
        'apellidos': request.args.get('apellidos', '').strip(),
        'dni': request.args.get('dni', '').strip(),
        'carrera': request.args.get('carrera', '').strip(),
        'page': request.args.get('page', 1, type=int),
        'per_page': request.args.get('per_page', 10, type=int)
    }

    resultado = obtener_egresados(filtros)
    return jsonify(resultado)

@egresado_bp.route('/egresados/con-detalles', methods=['GET'])
def get_egresados_con_detalles():
    """Obtener lista de egresados con sus detalles incluidos"""
    filtros = {
        'estado': request.args.get('estado'),
        'apellidos': request.args.get('apellidos', '').strip(),
        'dni': request.args.get('dni', '').strip(),
        'carrera': request.args.get('carrera', '').strip(),
        'page': request.args.get('page', 1, type=int),
        'per_page': request.args.get('per_page', 10, type=int)
    }

    resultado = obtener_egresados_con_detalles(filtros)
    return jsonify(resultado)

@egresado_bp.route('/egresados/html', methods=['GET'])
def listar_egresados_html():
    """Mostrar egresados en formato HTML"""
    estado = request.args.get('estado')
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Filtros y paginación
    if estado:
        egresados = Egresado.query.filter_by(estado=estado).paginate(page, per_page, False)
    else:
        egresados = Egresado.query.paginate(page=page, per_page=per_page, error_out=False)

    # Pasar los egresados a la plantilla HTML
    return render_template('egresados.html', egresados=egresados.items, prev_url=egresados.prev_num, next_url=egresados.next_num)

@egresado_bp.route('/egresados', methods=['POST'])
def create_egresado():
    """Crear nuevo egresado"""
    data = request.get_json()

    # Validar datos usando Marshmallow
    schema = EgresadoSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify({'message': 'Error de validación', 'errors': err.messages}), 400

    # Usar el servicio para crear el egresado
    resultado, codigo = crear_egresado(validated_data)
    return jsonify(resultado), codigo

@egresado_bp.route('/egresados/con-detalle', methods=['POST'])
def create_egresado_con_detalle():
    """Crear egresado con detalle en una sola transacción (cabecera y detalles)"""
    data = request.get_json()

    # Validar datos usando Marshmallow
    schema = EgresadoConDetalleSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify({'message': 'Error de validación', 'errors': err.messages}), 400

    # Usar el servicio para crear el egresado con detalle en transacción
    resultado, codigo = crear_egresado_con_detalle(validated_data)
    return jsonify(resultado), codigo

@egresado_bp.route('/egresados/con-detalle/<string:codigo>', methods=['PUT'])
def update_egresado_con_detalle(codigo):
    """Actualizar egresado con detalle en una sola transacción (cabecera y detalles)"""
    data = request.get_json()

    # Validar datos usando Marshmallow
    schema = EgresadoConDetalleUpdateSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify({'message': 'Error de validación', 'errors': err.messages}), 400

    # Usar el servicio para actualizar el egresado con detalle en transacción
    resultado, codigo_respuesta = actualizar_egresado_con_detalle(codigo, validated_data)
    return jsonify(resultado), codigo_respuesta

@egresado_bp.route('/egresados/<string:codigo>', methods=['PUT'])
def update_egresado(codigo):
    """Actualizar egresado existente"""
    data = request.get_json()

    # Validar datos usando Marshmallow (esquema para actualizaciones)
    schema = EgresadoUpdateSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify({'message': 'Error de validación', 'errors': err.messages}), 400

    # Usar el servicio para actualizar el egresado
    resultado, codigo_respuesta = actualizar_egresado(codigo, validated_data)
    return jsonify(resultado), codigo_respuesta

@egresado_bp.route('/egresados/<string:codigo>', methods=['GET'])
def get_egresado(codigo):
    """Obtener un egresado específico"""
    egresado = Egresado.query.get(codigo)
    if not egresado:
        return jsonify({'message': 'Egresado no encontrado'}), 404
    return jsonify(egresado.to_dict())

@egresado_bp.route('/egresados/<string:codigo>', methods=['DELETE'])
def delete_egresado_logico(codigo):
    """Eliminar egresado lógicamente"""
    resultado, codigo_respuesta = eliminar_egresado_logico(codigo)
    return jsonify(resultado), codigo_respuesta

@egresado_bp.route('/egresados/restaurar/<string:codigo>', methods=['PUT'])
@require_auth
def restaurar_egresado_route(codigo):
    """Restaurar egresado eliminado lógicamente"""
    resultado, codigo_respuesta = restaurar_egresado(codigo)
    return jsonify(resultado), codigo_respuesta

@egresado_bp.route('/egresados/fisico/<string:codigo>', methods=['DELETE'])
@require_auth
def delete_egresado_fisico(codigo):
    """Eliminar egresado físicamente"""
    resultado, codigo_respuesta = eliminar_egresado_fisico(codigo)
    return jsonify(resultado), codigo_respuesta

# Rutas para detalle de egresados


@egresado_bp.route('/detalle-egresados', methods=['GET'])
def get_detalle_egresados():
    """Obtener lista de detalles de egresados"""
    estado = request.args.get('estado')
    codigo_egresado = request.args.get('codigo_egresado')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = DetalleEgresado.query

    if estado:
        query = query.filter_by(estado=estado)

    if codigo_egresado:
        query = query.filter_by(codigo_egresado=codigo_egresado)

    pagination = query.order_by(DetalleEgresado.id_detalle).paginate(page=page, per_page=per_page, error_out=False)
    detalles_list = [d.to_dict() for d in pagination.items]

    return jsonify({
        'detalles': detalles_list,
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'pages': pagination.pages
    })

@egresado_bp.route('/detalle-egresados/<int:id_detalle>', methods=['GET'])
def get_detalle_egresado(id_detalle):
    """Obtener un detalle específico de egresado"""
    detalle = DetalleEgresado.query.get(id_detalle)
    if not detalle:
        return jsonify({'message': 'Detalle de egresado no encontrado'}), 404
    return jsonify(detalle.to_dict())

@egresado_bp.route('/detalle-egresados', methods=['POST'])
def create_detalle_egresado():
    """Crear nuevo detalle de egresado"""
    data = request.get_json()
    
    # Remover el campo estado si viene en el request (no se permite modificar en creación)
    if 'estado' in data:
        del data['estado']

    # Validar datos usando Marshmallow
    schema = DetalleEgresadoSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify({'message': 'Error de validación', 'errors': err.messages}), 400

    # Verificar que el egresado existe
    egresado = Egresado.query.get(validated_data['codigo_egresado'])
    if not egresado:
        return jsonify({'message': 'Egresado no encontrado'}), 404

    # Establecer estado automáticamente como 'A' (activo)
    validated_data['estado'] = 'A'

    # Crear nuevo detalle
    nuevo_detalle = DetalleEgresado(**validated_data)

    try:
        db.session.add(nuevo_detalle)
        db.session.commit()
        return jsonify(nuevo_detalle.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al crear el detalle: {str(e)}'}), 500

@egresado_bp.route('/detalle-egresados/<int:id_detalle>', methods=['PUT'])
def update_detalle_egresado(id_detalle):
    """Actualizar detalle de egresado"""
    data = request.get_json()
    detalle = DetalleEgresado.query.get(id_detalle)
    if not detalle:
        return jsonify({'message': 'Detalle de egresado no encontrado'}), 404

    # Validar datos usando Marshmallow
    schema = DetalleEgresadoSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify({'message': 'Error de validación', 'errors': err.messages}), 400

    try:
        # Actualizar campos
        for key, value in validated_data.items():
            if hasattr(detalle, key):
                setattr(detalle, key, value)

        db.session.commit()
        return jsonify(detalle.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al actualizar el detalle: {str(e)}'}), 500

@egresado_bp.route('/detalle-egresados/<int:id_detalle>', methods=['DELETE'])
def delete_detalle_egresado_logico(id_detalle):
    """Eliminar detalle de egresado lógicamente con retry para manejo de errores de conexión"""
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            detalle = DetalleEgresado.query.get(id_detalle)
            if not detalle:
                return jsonify({'message': 'Detalle de egresado no encontrado'}), 404
            
            detalle.estado = 'I'
            db.session.commit()
            return jsonify({'message': 'Detalle eliminado exitosamente'}), 200
        
        except OperationalError as e:
            if attempt < max_retries - 1:
                db.session.rollback()
                time.sleep(retry_delay)
                continue
            else:
                return jsonify({
                    'message': 'Error de conexión con la base de datos. Por favor, intenta nuevamente.'
                }), 500
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Error al eliminar el detalle: {str(e)}'}), 500

@egresado_bp.route('/detalle-egresados/restaurar/<int:id_detalle>', methods=['PUT'])
def restaurar_detalle_egresado(id_detalle):
    """Restaurar detalle de egresado eliminado lógicamente con retry para manejo de errores de conexión"""
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            detalle = DetalleEgresado.query.get(id_detalle)
            if not detalle:
                return jsonify({'message': 'Detalle de egresado no encontrado'}), 404
            
            detalle.estado = 'A'
            db.session.commit()
            return jsonify({'message': 'Detalle restaurado exitosamente'}), 200
        
        except OperationalError as e:
            if attempt < max_retries - 1:
                db.session.rollback()
                time.sleep(retry_delay)
                continue
            else:
                return jsonify({
                    'message': 'Error de conexión con la base de datos. Por favor, intenta nuevamente.'
                }), 500
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Error al restaurar el detalle: {str(e)}'}), 500

@egresado_bp.route('/detalle-egresados/fisico/<int:id_detalle>', methods=['DELETE'])
def delete_detalle_egresado_fisico(id_detalle):
    """Eliminar detalle de egresado físicamente"""
    detalle = DetalleEgresado.query.get(id_detalle)
    if not detalle:
        return jsonify({'message': 'Detalle de egresado no encontrado'}), 404

    try:
        db.session.delete(detalle)
        db.session.commit()
        return jsonify({'message': 'Detalle eliminado permanentemente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al eliminar el detalle: {str(e)}'}), 500
