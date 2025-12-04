# Lógica y operaciones sobre certificaciones
import os
from werkzeug.utils import secure_filename
from ..models.certificacion import Certificacion
from ..models.egresado import Egresado
from .. import db

UPLOAD_FOLDER = 'app/uploads/certificaciones'
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    """Verificar si el archivo tiene una extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def crear_certificacion(data, archivo=None):
    """Crear una nueva certificación"""
    try:
        # Verificar que el egresado existe
        egresado = Egresado.query.get(data['codigo_egresado'])
        if not egresado:
            return {'error': 'Egresado no encontrado'}, 404

        # Procesar archivo si se proporciona
        nombre_archivo = None
        if archivo and archivo.filename and allowed_file(archivo.filename):
            nombre_archivo = secure_filename(archivo.filename)
            # Crear directorio si no existe
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            # Guardar archivo
            ruta_archivo = os.path.join(UPLOAD_FOLDER, nombre_archivo)
            archivo.save(ruta_archivo)

        # Crear nueva certificación
        nueva_certificacion = Certificacion(
            codigo_egresado=data['codigo_egresado'],
            nombre=data['nombre'],
            institucion=data['institucion'],
            fecha_obtencion=data['fecha_obtencion'],
            archivo=nombre_archivo,
            estado=data.get('estado', 'A')
        )

        db.session.add(nueva_certificacion)
        db.session.commit()
        
        return nueva_certificacion.to_dict(), 201
        
    except Exception as e:
        db.session.rollback()
        return {'error': f'Error al crear la certificación: {str(e)}'}, 500

def obtener_certificaciones(filtros):
    """Obtener lista de certificaciones con filtros"""
    query = Certificacion.query.filter_by(estado='A')
    
    if filtros.get('codigo_egresado'):
        query = query.filter_by(codigo_egresado=filtros['codigo_egresado'])
    
    certificaciones = query.order_by(Certificacion.fecha_obtencion.desc()).all()
    
    return [c.to_dict() for c in certificaciones]

def obtener_certificacion(id_certificacion):
    """Obtener una certificación específica"""
    certificacion = Certificacion.query.get(id_certificacion)
    if not certificacion:
        return {'error': 'Certificación no encontrada'}, 404
    return certificacion.to_dict(), 200

def actualizar_certificacion(id_certificacion, data, archivo=None):
    """Actualizar una certificación existente"""
    certificacion = Certificacion.query.get(id_certificacion)
    if not certificacion:
        return {'error': 'Certificación no encontrada'}, 404
    
    try:
        # Procesar nuevo archivo si se proporciona
        if archivo and archivo.filename and allowed_file(archivo.filename):
            # Eliminar archivo anterior si existe
            if certificacion.archivo:
                ruta_anterior = os.path.join(UPLOAD_FOLDER, certificacion.archivo)
                if os.path.exists(ruta_anterior):
                    os.remove(ruta_anterior)
            
            # Guardar nuevo archivo
            nombre_archivo = secure_filename(archivo.filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            ruta_archivo = os.path.join(UPLOAD_FOLDER, nombre_archivo)
            archivo.save(ruta_archivo)
            data['archivo'] = nombre_archivo

        # Actualizar campos
        for key, value in data.items():
            if hasattr(certificacion, key):
                setattr(certificacion, key, value)
        
        db.session.commit()
        return certificacion.to_dict(), 200
        
    except Exception as e:
        db.session.rollback()
        return {'error': f'Error al actualizar la certificación: {str(e)}'}, 500

def eliminar_certificacion_logico(id_certificacion):
    """Eliminar certificación lógicamente"""
    certificacion = Certificacion.query.get(id_certificacion)
    if not certificacion:
        return {'error': 'Certificación no encontrada'}, 404
    
    try:
        certificacion.estado = 'I'
        db.session.commit()
        return {'message': 'Certificación eliminada exitosamente'}, 200
        
    except Exception as e:
        db.session.rollback()
        return {'error': f'Error al eliminar la certificación: {str(e)}'}, 500

def obtener_ruta_archivo(id_certificacion):
    """Obtener la ruta del archivo de certificación"""
    certificacion = Certificacion.query.get(id_certificacion)
    if not certificacion or not certificacion.archivo:
        return {'error': 'Archivo no encontrado'}, 404
    
    ruta_archivo = os.path.join(UPLOAD_FOLDER, certificacion.archivo)
    if not os.path.exists(ruta_archivo):
        return {'error': 'Archivo no existe en el servidor'}, 404
    
    return ruta_archivo, 200

