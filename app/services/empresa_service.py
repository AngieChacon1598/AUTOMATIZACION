# Lógica y operaciones sobre empresas
from ..models.empresa import Empresa
from .. import db

def crear_empresa(data):
    """Crear una nueva empresa"""
    try:
        # Validar datos requeridos
        if not data.get('nombre') or not data.get('ruc'):
            return {'error': 'Nombre y RUC son requeridos'}, 400

        # Verificar que el nombre no exista
        if Empresa.query.filter_by(nombre=data['nombre']).first():
            return {'error': 'El nombre de la empresa ya existe'}, 400

        # Verificar que el RUC no exista
        if Empresa.query.filter_by(ruc=data['ruc']).first():
            return {'error': 'El RUC ya está registrado'}, 400

        # Crear nueva empresa
        nueva_empresa = Empresa(
            nombre=data['nombre'],
            ruc=data['ruc'],
            direccion=data.get('direccion', ''),
            telefono=data.get('telefono', ''),
            correo=data.get('correo', ''),
            estado=data.get('estado', 'A')
        )

        db.session.add(nueva_empresa)
        db.session.commit()
        
        return nueva_empresa.to_dict(), 201
        
    except Exception as e:
        db.session.rollback()
        return {'error': f'Error al crear la empresa: {str(e)}'}, 500

def obtener_empresas(filtros):
    """Obtener lista de empresas con filtros y paginación"""
    query = Empresa.query
    
    # Aplicar filtros
    if filtros.get('estado'):
        query = query.filter_by(estado=filtros['estado'])
    
    if filtros.get('nombre'):
        query = query.filter(Empresa.nombre.ilike(f"%{filtros['nombre']}%"))
    
    if filtros.get('ruc'):
        query = query.filter(Empresa.ruc.ilike(f"%{filtros['ruc']}%"))
    
    pagination = query.order_by(Empresa.nombre).paginate(
        page=filtros.get('page', 1), 
        per_page=filtros.get('per_page', 10), 
        error_out=False
    )
    
    return {
        'empresas': [e.to_dict() for e in pagination.items],
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'pages': pagination.pages
    }

def obtener_empresa(id_empresa):
    """Obtener una empresa específica"""
    empresa = Empresa.query.get(id_empresa)
    if not empresa:
        return {'error': 'Empresa no encontrada'}, 404
    return empresa.to_dict(), 200

def actualizar_empresa(id_empresa, data):
    """Actualizar una empresa existente"""
    empresa = Empresa.query.get(id_empresa)
    if not empresa:
        return {'error': 'Empresa no encontrada'}, 404
    
    try:
        # Verificar nombre único si se está cambiando
        if 'nombre' in data and data['nombre'] != empresa.nombre:
            if Empresa.query.filter_by(nombre=data['nombre']).first():
                return {'error': 'El nombre de la empresa ya existe'}, 400

        # Verificar RUC único si se está cambiando
        if 'ruc' in data and data['ruc'] != empresa.ruc:
            if Empresa.query.filter_by(ruc=data['ruc']).first():
                return {'error': 'El RUC ya está registrado'}, 400

        # Actualizar campos
        for key, value in data.items():
            if hasattr(empresa, key):
                setattr(empresa, key, value)
        
        db.session.commit()
        return empresa.to_dict(), 200
        
    except Exception as e:
        db.session.rollback()
        return {'error': f'Error al actualizar la empresa: {str(e)}'}, 500

def eliminar_empresa_logico(id_empresa):
    """Eliminar empresa lógicamente"""
    empresa = Empresa.query.get(id_empresa)
    if not empresa:
        return {'error': 'Empresa no encontrada'}, 404
    
    try:
        empresa.estado = 'I'
        db.session.commit()
        return {'message': 'Empresa eliminada exitosamente'}, 200
        
    except Exception as e:
        db.session.rollback()
        return {'error': f'Error al eliminar la empresa: {str(e)}'}, 500

def restaurar_empresa(id_empresa):
    """Restaurar empresa eliminada lógicamente"""
    empresa = Empresa.query.get(id_empresa)
    if not empresa:
        return {'error': 'Empresa no encontrada'}, 404
    
    try:
        empresa.estado = 'A'
        db.session.commit()
        return {'message': 'Empresa restaurada exitosamente'}, 200
        
    except Exception as e:
        db.session.rollback()
        return {'error': f'Error al restaurar la empresa: {str(e)}'}, 500

