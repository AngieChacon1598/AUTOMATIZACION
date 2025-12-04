# Lógica y operaciones sobre encuestas de egresados
from ..models.encuesta_egresado import EncuestaEgresado
from ..models.egresado import Egresado
from .. import db


def crear_encuesta(data):
    """Crear una nueva encuesta de egresado"""
    try:
        # Normalizar alias: ingresos_mensuales -> ingreso_mensual
        if 'ingresos_mensuales' in data and 'ingreso_mensual' not in data:
            data['ingreso_mensual'] = data.pop('ingresos_mensuales')
        
        # Normalizar booleanos (aceptar string, int, bool)
        def normalize_bool(value):
            if value is None:
                return None
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                return value.lower() in ('true', '1', 'si', 'yes', 'y')
            if isinstance(value, int):
                return bool(value)
            return None
        
        # Normalizar campos booleanos
        if 'trabaja_actualmente' in data:
            data['trabaja_actualmente'] = normalize_bool(data['trabaja_actualmente'])
        if 'tiene_negocio' in data:
            data['tiene_negocio'] = normalize_bool(data['tiene_negocio'])
        
        # Validar campos requeridos
        if not data.get('codigo_egresado'):
            return {'message': 'codigo_egresado es requerido'}, 400
        if not data.get('fecha_aplicacion'):
            return {'message': 'fecha_aplicacion es requerido'}, 400
        
        # Verificar que el egresado existe
        egresado = Egresado.query.get(data.get('codigo_egresado'))
        if not egresado:
            return {'message': 'Egresado no encontrado'}, 404

        # Crear nueva encuesta (solo con campos que existen en la BD)
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
            cantidad_empleos_ultimo_ano=data.get('cantidad_empleos_ultimo_ano', 0),
            cantidad_empleos_carrera=data.get('cantidad_empleos_carrera', 0),
            nombre_empresa_actual=data.get('nombre_empresa_actual'),
            nombre_jefe_inmediato=data.get('nombre_jefe_inmediato'),
            telefono_empresa=data.get('telefono_empresa'),
            pagina_web_empresa=data.get('pagina_web_empresa'),
            correo_empresa=data.get('correo_empresa'),
            tiene_negocio=data.get('tiene_negocio', False),
            cantidad_trabajadores=data.get('cantidad_trabajadores'),
            tipo_constitucion=data.get('tipo_constitucion'),
            actividad_economica_negocio_id=data.get('actividad_economica_negocio_id'),
            estado=data.get('estado', 'A')
        )

        db.session.add(nueva_encuesta)
        db.session.commit()

        return nueva_encuesta.to_dict(), 201

    except Exception as e:
        db.session.rollback()
        return {'message': f'Error al crear la encuesta: {str(e)}'}, 500

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

    # Retornar estructura según manual (encuestas en lugar de data)
    return {
        "encuestas": [e.to_dict() for e in pagination.items],
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages
    }


def obtener_encuesta(id_encuesta):
    """Obtener una encuesta específica"""
    encuesta = EncuestaEgresado.query.get(id_encuesta)
    if not encuesta:
        return {'message': 'Encuesta no encontrada'}, 404
    return encuesta.to_dict(), 200


def actualizar_encuesta(id_encuesta, data):
    """Actualizar una encuesta existente"""
    encuesta = EncuestaEgresado.query.get(id_encuesta)
    if not encuesta:
        return {'message': 'Encuesta no encontrada'}, 404

    try:
        # Normalizar alias: ingresos_mensuales -> ingreso_mensual
        if 'ingresos_mensuales' in data and 'ingreso_mensual' not in data:
            data['ingreso_mensual'] = data.pop('ingresos_mensuales')
        
        # Normalizar booleanos
        def normalize_bool(value):
            if value is None:
                return None
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                return value.lower() in ('true', '1', 'si', 'yes', 'y')
            if isinstance(value, int):
                return bool(value)
            return None
        
        if 'trabaja_actualmente' in data:
            data['trabaja_actualmente'] = normalize_bool(data['trabaja_actualmente'])
        if 'tiene_negocio' in data:
            data['tiene_negocio'] = normalize_bool(data['tiene_negocio'])
        
        # Actualizar campos (solo los que existen en la BD)
        campos_permitidos = [
            'codigo_egresado', 'fecha_aplicacion', 'trabaja_actualmente',
            'tipo_contrato', 'tipo_empleo', 'ingreso_mensual', 'area_trabajo',
            'actividad_economica_id', 'relacion_carrera', 'medios_busqueda',
            'cantidad_empleos_ultimo_ano', 'cantidad_empleos_carrera',
            'nombre_empresa_actual', 'nombre_jefe_inmediato', 'telefono_empresa',
            'pagina_web_empresa', 'correo_empresa', 'tiene_negocio',
            'cantidad_trabajadores', 'tipo_constitucion',
            'actividad_economica_negocio_id', 'estado'
        ]
        
        for key, value in data.items():
            if key in campos_permitidos and key != 'id_encuesta' and key != 'ingresos_mensuales':
                setattr(encuesta, key, value)

        db.session.commit()
        return encuesta.to_dict(), 200

    except Exception as e:
        db.session.rollback()
        return {'message': f'Error al actualizar la encuesta: {str(e)}'}, 500


def eliminar_encuesta_logica(id_encuesta):
    """Eliminación lógica de una encuesta (cambia estado a 'I')."""

    encuesta = EncuestaEgresado.query.get(id_encuesta)

    if encuesta is None:
        return {'message': 'Encuesta no encontrada'}, 404

    try:
        encuesta.estado = 'I'
        db.session.commit()
        return {'message': 'Encuesta eliminada exitosamente', 'id_encuesta': id_encuesta}, 200

    except Exception as e:
        db.session.rollback()
        return {'message': f'Error al eliminar la encuesta: {str(e)}'}, 500

def restaurar_encuesta_logica(id_encuesta):
    """Restaurar encuesta eliminada lógicamente (cambia estado a 'A')."""

    encuesta = EncuestaEgresado.query.get(id_encuesta)

    if encuesta is None:
        return {'message': 'Encuesta no encontrada'}, 404

    try:
        encuesta.estado = 'A'
        db.session.commit()
        return {'message': 'Encuesta restaurada exitosamente', 'id_encuesta': id_encuesta, 'estado': 'A'}, 200

    except Exception as e:
        db.session.rollback()
        return {'message': f'Error al restaurar la encuesta: {str(e)}'}, 500


def obtener_estadisticas_encuestas(codigo_egresado=None):
    """Obtener estadísticas de encuestas"""
    try:
        query = EncuestaEgresado.query.filter_by(estado='A')

        if codigo_egresado:
            query = query.filter_by(codigo_egresado=codigo_egresado)

        total_encuestas = query.count()
        encuestas_activas = query.filter_by(estado='A').count()
        encuestas_inactivas = EncuestaEgresado.query.filter_by(estado='I').count()
        if codigo_egresado:
            encuestas_inactivas = EncuestaEgresado.query.filter_by(estado='I', codigo_egresado=codigo_egresado).count()
        
        trabaja_actualmente = query.filter_by(trabaja_actualmente=True).count()
        tiene_negocio = query.filter_by(tiene_negocio=True).count()

        return {
            'total_encuestas': total_encuestas,
            'encuestas_activas': encuestas_activas,
            'encuestas_inactivas': encuestas_inactivas,
            'trabajan_actualmente': trabaja_actualmente,
            'tienen_negocio': tiene_negocio
        }, 200

    except Exception as e:
        return {'message': f'Error al obtener estadísticas: {str(e)}'}, 500
