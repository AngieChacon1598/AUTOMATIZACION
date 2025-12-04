# Lógica y operaciones sobre encuestas de egresados
from ..models.encuesta_egresado import EncuestaEgresado
from ..models.egresado import Egresado
from .. import db


def crear_encuesta(data):
    """Crear una nueva encuesta de egresado"""
    try:
        # Verificar que el egresado existe
        egresado = Egresado.query.get(data.get('codigo_egresado'))
        if not egresado:
            return {'error': 'Egresado no encontrado'}, 404

        # Crear nueva encuesta
        nueva_encuesta = EncuestaEgresado(
            codigo_egresado=data.get('codigo_egresado'),
            fecha_aplicacion=data.get('fecha_aplicacion'),
            trabaja_actualmente=data.get('trabaja_actualmente'),
            tipo_contrato=data.get('tipo_contrato'),
            tipo_empleo=data.get('tipo_empleo'),
            ingreso_mensual=data.get('ingreso_mensual'),
            area_trabajo=data.get('area_trabajo'),
            actividad_economica_id=data.get('actividad_economica_id'),
            relacion_carrera=data.get('relacion_carrera'),
            medios_busqueda=data.get('medios_busqueda'),
            cantidad_empleos_ultimo_ano=data.get(
                'cantidad_empleos_ultimo_ano', 0),
            cantidad_empleos_carrera=data.get('cantidad_empleos_carrera', 0),
            nombre_empresa_actual=data.get('nombre_empresa_actual'),
            nombre_jefe_inmediato=data.get('nombre_jefe_inmediato'),
            telefono_empresa=data.get('telefono_empresa'),
            pagina_web_empresa=data.get('pagina_web_empresa'),
            correo_empresa=data.get('correo_empresa'),
            tiene_negocio=data.get('tiene_negocio', False),
            cantidad_trabajadores=data.get('cantidad_trabajadores'),
            tipo_constitucion=data.get('tipo_constitucion'),
            actividad_economica_negocio_id=data.get(
                'actividad_economica_negocio_id'),
            estado=data.get('estado', 'A')
        )

        db.session.add(nueva_encuesta)
        db.session.commit()

        return nueva_encuesta.to_dict(), 201

    except Exception as e:
        db.session.rollback()
        return {'error': f'Error al crear la encuesta: {str(e)}'}, 500

def obtener_encuestas(filtros, page=1, per_page=10):
    """Obtener lista de encuestas con filtros y paginación"""

    # Base sin filtro de estado
    query = EncuestaEgresado.query

    # === Aplicar filtros dinámicos ===

    # Estado opcional
    if filtros.get("estado"):
        query = query.filter_by(estado=filtros["estado"])

    # Código de egresado
    if filtros.get("codigo_egresado"):
        query = query.filter_by(codigo_egresado=filtros["codigo_egresado"])

    # Trabaja actualmente
    if filtros.get("trabaja_actualmente") is not None:
        query = query.filter_by(trabaja_actualmente=filtros["trabaja_actualmente"])

    # Tiene negocio
    if filtros.get("tiene_negocio") is not None:
        query = query.filter_by(tiene_negocio=filtros["tiene_negocio"])

    # Orden por fecha de aplicación DESC
    query = query.order_by(EncuestaEgresado.fecha_aplicacion.desc())

    # Paginar
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return {
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page,
        "per_page": pagination.per_page,
        "data": [e.to_dict() for e in pagination.items]
    }


def obtener_encuesta(id_encuesta):
    """Obtener una encuesta específica"""
    encuesta = EncuestaEgresado.query.get(id_encuesta)
    if not encuesta:
        return {'error': 'Encuesta no encontrada'}, 404
    return encuesta.to_dict(), 200


def actualizar_encuesta(id_encuesta, data):
    """Actualizar una encuesta existente"""
    encuesta = EncuestaEgresado.query.get(id_encuesta)
    if not encuesta:
        return {'error': 'Encuesta no encontrada'}, 404

    try:
        # Actualizar campos
        for key, value in data.items():
            if hasattr(encuesta, key) and key != 'id_encuesta':
                setattr(encuesta, key, value)

        db.session.commit()
        return encuesta.to_dict(), 200

    except Exception as e:
        db.session.rollback()
        return {'error': f'Error al actualizar la encuesta: {str(e)}'}, 500


def eliminar_encuesta_logica(id_encuesta):
    """Eliminación lógica de una encuesta (cambia estado a 'I')."""

    encuesta = EncuestaEgresado.query.get(id_encuesta)

    if encuesta is None:
        return {'error': 'Encuesta no encontrada'}, 404

    # Ya está eliminada
    if encuesta.estado == 'I':
        return {'message': 'La encuesta ya está inactiva'}, 400

    try:
        encuesta.estado = 'I'
        db.session.commit()
        return {'message': 'Encuesta eliminada lógicamente'}, 200

    except Exception as e:
        db.session.rollback()
        return {'error': f'Ocurrió un error al actualizar: {str(e)}'}, 500

def restaurar_encuesta_logica(id_encuesta):
    """Eliminación lógica de una encuesta (cambia estado a 'A')."""

    encuesta = EncuestaEgresado.query.get(id_encuesta)

    if encuesta is None:
        return {'error': 'Encuesta no encontrada'}, 404

    # Ya está restaurada
    if encuesta.estado == 'A':
        return {'message': 'La encuesta ya está inactiva'}, 400

    try:
        encuesta.estado = 'A'
        db.session.commit()
        return {'message': 'Encuesta restaurada lógicamente'}, 200

    except Exception as e:
        db.session.rollback()
        return {'error': f'Ocurrió un error al actualizar: {str(e)}'}, 500


def obtener_estadisticas_encuestas(codigo_egresado=None):
    """Obtener estadísticas de encuestas"""
    try:
        query = EncuestaEgresado.query.filter_by(estado='A')

        if codigo_egresado:
            query = query.filter_by(codigo_egresado=codigo_egresado)

        total_encuestas = query.count()
        trabaja_actualmente = query.filter_by(trabaja_actualmente=True).count()
        tiene_negocio = query.filter_by(tiene_negocio=True).count()

        return {
            'total_encuestas': total_encuestas,
            'trabaja_actualmente': trabaja_actualmente,
            'tiene_negocio': tiene_negocio,
            'desempleado': total_encuestas - trabaja_actualmente - tiene_negocio
        }, 200

    except Exception as e:
        return {'error': f'Error al obtener estadísticas: {str(e)}'}, 500
