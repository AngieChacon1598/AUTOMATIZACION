# Endpoints relacionados con reportes y datos auxiliares
from flask import Blueprint, request, jsonify
from ..services.usuario_service import require_auth
from .. import db

# Crear Blueprint para rutas de reportes y auxiliares
reportes_bp = Blueprint('reportes', __name__)

@reportes_bp.route('/api/reportes/egresados-por-carrera')
@require_auth
def egresados_por_carrera():
    """Reporte de egresados agrupados por carrera"""
    try:
        with db.engine.connect() as conn:
            result = conn.execute(db.text('''
                SELECT carrera_id, COUNT(*) as total
                FROM egresado 
                WHERE estado = 'A'
                GROUP BY carrera_id
                ORDER BY total DESC
            '''))
            
            reporte = [{'carrera_id': row[0], 'total': row[1]} for row in result]
            return jsonify({'reporte': reporte}), 200
            
    except Exception as e:
        return jsonify({'error': f'Error al generar reporte: {str(e)}'}), 500

@reportes_bp.route('/api/reportes/egresados-por-estado')
@require_auth
def egresados_por_estado():
    """Reporte de egresados agrupados por estado"""
    try:
        with db.engine.connect() as conn:
            result = conn.execute(db.text('''
                SELECT estado, COUNT(*) as total
                FROM egresado 
                GROUP BY estado
                ORDER BY estado
            '''))
            
            reporte = [{'estado': row[0], 'total': row[1]} for row in result]
            return jsonify({'reporte': reporte}), 200
            
    except Exception as e:
        return jsonify({'error': f'Error al generar reporte: {str(e)}'}), 500

@reportes_bp.route('/api/reportes/egresados-por-anio')
@require_auth
def egresados_por_anio():
    """Reporte de egresados agrupados por año de egreso"""
    try:
        with db.engine.connect() as conn:
            result = conn.execute(db.text('''
                SELECT anio_egreso, COUNT(*) as total
                FROM egresado 
                WHERE estado = 'A' AND anio_egreso IS NOT NULL
                GROUP BY anio_egreso
                ORDER BY anio_egreso DESC
            '''))
            
            reporte = [{'anio_egreso': row[0], 'total': row[1]} for row in result]
            return jsonify({'reporte': reporte}), 200
            
    except Exception as e:
        return jsonify({'error': f'Error al generar reporte: {str(e)}'}), 500

@reportes_bp.route('/carreras', methods=['GET'])
def get_carreras():
    """Obtener todas las carreras profesionales"""
    try:
        with db.engine.connect() as conn:
            result = conn.execute(db.text('''
                SELECT id_carrera, nombre
                FROM carrera_profesional
                ORDER BY nombre
            '''))
            
            carreras = [{'id_carrera': row[0], 'nombre_carrera': row[1]} for row in result]
            return jsonify({'carreras': carreras}), 200
            
    except Exception as e:
        return jsonify({'error': f'Error al obtener carreras: {str(e)}'}), 500

@reportes_bp.route('/estados-civiles', methods=['GET'])
def get_estados_civiles():
    """Obtener todos los estados civiles"""
    try:
        with db.engine.connect() as conn:
            result = conn.execute(db.text('''
                SELECT id_estado, descripcion
                FROM estado_civil
                ORDER BY descripcion
            '''))
            
            estados = [{'id_estado_civil': row[0], 'nombre_estado': row[1]} for row in result]
            return jsonify({'estados_civiles': estados}), 200
            
    except Exception as e:
        return jsonify({'error': f'Error al obtener estados civiles: {str(e)}'}), 500

@reportes_bp.route('/actividades-economicas', methods=['GET'])
def get_actividades_economicas():
    """Obtener todas las actividades económicas"""
    try:
        with db.engine.connect() as conn:
            result = conn.execute(db.text('''
                SELECT id_actividad, nombre
                FROM actividad_economica
                ORDER BY nombre
            '''))
            
            actividades = [{'id_actividad': row[0], 'nombre_actividad': row[1]} for row in result]
            return jsonify({'actividades_economicas': actividades}), 200
            
    except Exception as e:
        return jsonify({'error': f'Error al obtener actividades económicas: {str(e)}'}), 500
