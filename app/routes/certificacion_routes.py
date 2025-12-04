# Endpoints relacionados con certificaciones
from flask import Blueprint, request, jsonify, send_file
from ..models.certificacion import Certificacion
from ..services.certificacion_service import (
    crear_certificacion, obtener_certificaciones, obtener_certificacion,
    actualizar_certificacion, eliminar_certificacion_logico, obtener_ruta_archivo
)
from ..services.usuario_service import require_auth
from .. import db

# Crear Blueprint para rutas de certificaciones
certificacion_bp = Blueprint('certificacion', __name__)

@certificacion_bp.route('/certificaciones', methods=['GET'])
def listar_certificaciones():
    """Obtener lista de certificaciones"""
    filtros = {
        'codigo_egresado': request.args.get('codigo_egresado')
    }
    
    certificaciones = obtener_certificaciones(filtros)
    return jsonify({'certificaciones': certificaciones})

@certificacion_bp.route('/certificaciones', methods=['POST'])
@require_auth
def agregar_certificacion():
    """Agregar nueva certificación"""
    data = request.form
    archivo = request.files.get('archivo')
    
    # Validar datos requeridos
    if not data.get('codigo_egresado') or not data.get('nombre') or not data.get('institucion') or not data.get('fecha_obtencion'):
        return jsonify({'message': 'Todos los campos son requeridos'}), 400

    resultado, codigo_respuesta = crear_certificacion(data, archivo)
    return jsonify(resultado), codigo_respuesta

@certificacion_bp.route('/certificaciones/<int:id_certificacion>', methods=['PUT'])
@require_auth
def editar_certificacion(id_certificacion):
    """Editar certificación existente"""
    data = request.form
    archivo = request.files.get('archivo')
    
    resultado, codigo_respuesta = actualizar_certificacion(id_certificacion, data, archivo)
    return jsonify(resultado), codigo_respuesta

@certificacion_bp.route('/certificaciones/<int:id_certificacion>', methods=['DELETE'])
@require_auth
def eliminar_certificacion(id_certificacion):
    """Eliminar certificación lógicamente"""
    resultado, codigo_respuesta = eliminar_certificacion_logico(id_certificacion)
    return jsonify(resultado), codigo_respuesta

@certificacion_bp.route('/certificaciones/<int:id_certificacion>/archivo', methods=['GET'])
def descargar_archivo_certificacion(id_certificacion):
    """Descargar archivo de certificación"""
    resultado, codigo_respuesta = obtener_ruta_archivo(id_certificacion)
    
    if codigo_respuesta != 200:
        return jsonify(resultado), codigo_respuesta
    
    certificacion = Certificacion.query.get(id_certificacion)
    return send_file(resultado, as_attachment=True, download_name=certificacion.archivo)

