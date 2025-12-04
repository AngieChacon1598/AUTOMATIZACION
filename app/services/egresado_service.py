# Lógica y operaciones sobre egresados
import re
from datetime import datetime
from ..models.egresado import Egresado
from ..models.detalle_egresado import DetalleEgresado
from .. import db

def validar_correo(correo):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, correo) is not None

def validar_telefono(telefono):
    return telefono.isdigit() and len(telefono) == 9

def validar_dni(dni):
    return Egresado.query.filter_by(dni=dni).first() is None

def validar_nombre_apellido(nombre):
    return bool(re.match("^[A-Za-zÑñÁáÉéÍíÓóÚúÜü\\s]+$", nombre))

def validar_codigo(codigo):
    return Egresado.query.filter_by(codigo=codigo).first() is None

def validar_codigo_egresado(codigo):
    return Egresado.query.filter_by(codigo=codigo).first() is not None

def validar_sueldo(sueldo):
    return sueldo is None or sueldo >= 0

def validar_fecha(fecha_str):
    if not fecha_str:
        return True
    try:
        datetime.strptime(fecha_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def crear_egresado(data):
    """Crear un nuevo egresado"""
    try:
        # Validar DNI único
        if not validar_dni(data['dni']):
            return {'error': 'El DNI ya está registrado.'}, 400

        # Validar Código único
        if not validar_codigo(data['codigo']):
            return {'error': 'El código ya está registrado.'}, 400

        # Validar correo electrónico
        if not validar_correo(data['correo']):
            return {'error': 'Correo electrónico inválido.'}, 400

        # Validar teléfono
        if data.get('telefono') and not validar_telefono(data['telefono']):
            return {'error': 'Número de teléfono inválido. Debe contener solo números y tener 9 dígitos.'}, 400

        # Validar nombre y apellidos
        if not validar_nombre_apellido(data['nombre']):
            return {'error': 'El nombre contiene caracteres no válidos.'}, 400
        if not validar_nombre_apellido(data['apellidos']):
            return {'error': 'Los apellidos contienen caracteres no válidos.'}, 400

        # Crear nuevo egresado
        nuevo_egresado = Egresado(
            codigo=data['codigo'],
            nombre=data['nombre'],
            apellidos=data['apellidos'],
            dni=data['dni'],
            fecha_nacimiento=data.get('fecha_nacimiento'),
            sexo=data.get('sexo'),
            direccion=data.get('direccion'),
            telefono=data.get('telefono', ''),
            telefono_referencia=data.get('telefono_referencia'),
            correo=data['correo'],
            es_conviviente=data.get('es_conviviente', False),
            estado_civil_id=data.get('estado_civil_id'),
            cantidad_hijos=data.get('cantidad_hijos', 0),
            tiene_discapacidad=data.get('tiene_discapacidad', False),
            carrera_id=data['carrera_id'],
            anio_ingreso=data.get('anio_ingreso'),
            anio_egreso=data.get('anio_egreso'),
            es_titulado=data.get('es_titulado', False),
            anio_titulacion=data.get('anio_titulacion'),
            estado=data.get('estado', 'A')
        )

        db.session.add(nuevo_egresado)
        db.session.commit()
        
        return nuevo_egresado.to_dict(), 201
        
    except Exception as e:
        db.session.rollback()
        return {'error': f'Error al registrar el egresado: {str(e)}'}, 500

def obtener_egresados(filtros):
    """Obtener lista de egresados con filtros"""
    query = Egresado.query
    
    # Aplicar filtros
    if filtros.get('estado'):
        query = query.filter_by(estado=filtros['estado'])
    
    if filtros.get('apellidos'):
        query = query.filter(Egresado.apellidos.ilike(f"%{filtros['apellidos']}%"))
    
    if filtros.get('dni'):
        query = query.filter(Egresado.dni.ilike(f"%{filtros['dni']}%"))
    
    if filtros.get('carrera'):
        query = query.filter(Egresado.carrera_id == filtros['carrera'])
    
    pagination = query.order_by(Egresado.codigo).paginate(
        page=filtros.get('page', 1), 
        per_page=filtros.get('per_page', 10), 
        error_out=False
    )
    
    return {
        'egresados': [e.to_dict() for e in pagination.items],
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'pages': pagination.pages
    }

def obtener_egresados_con_detalles(filtros):
    """Obtener lista de egresados con sus detalles incluidos"""
    query = Egresado.query
    
    # Aplicar filtros
    if filtros.get('estado'):
        query = query.filter_by(estado=filtros['estado'])
    
    if filtros.get('apellidos'):
        query = query.filter(Egresado.apellidos.ilike(f"%{filtros['apellidos']}%"))
    
    if filtros.get('dni'):
        query = query.filter(Egresado.dni.ilike(f"%{filtros['dni']}%"))
    
    if filtros.get('carrera'):
        query = query.filter(Egresado.carrera_id == filtros['carrera'])
    
    pagination = query.order_by(Egresado.codigo).paginate(
        page=filtros.get('page', 1), 
        per_page=filtros.get('per_page', 10), 
        error_out=False
    )
    
    # Construir respuesta con detalles incluidos
    egresados_con_detalles = []
    for egresado in pagination.items:
        egresado_dict = egresado.to_dict()
        
        # Obtener detalles del egresado
        detalles = DetalleEgresado.query.filter_by(
            codigo_egresado=egresado.codigo,
            estado='A'  # Solo detalles activos
        ).all()
        
        # Convertir detalles a diccionarios
        detalles_list = [detalle.to_dict() for detalle in detalles]
        
        # Agregar detalles al egresado
        egresado_dict['detalles'] = detalles_list
        egresados_con_detalles.append(egresado_dict)
    
    return {
        'egresados': egresados_con_detalles,
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'pages': pagination.pages
    }

def actualizar_egresado(codigo, data):
    """Actualizar un egresado existente"""
    egresado = Egresado.query.get(codigo)
    if not egresado:
        return {'error': 'Egresado no encontrado'}, 404
    
    try:
        # Actualizar campos
        for key, value in data.items():
            if hasattr(egresado, key):
                setattr(egresado, key, value)
        
        db.session.commit()
        return egresado.to_dict(), 200
        
    except Exception as e:
        db.session.rollback()
        return {'error': f'Error al actualizar el egresado: {str(e)}'}, 500

def eliminar_egresado_logico(codigo):
    """Eliminar egresado lógicamente (cambiar estado a 'I') con retry para manejo de errores de conexión"""
    from sqlalchemy.exc import OperationalError
    import time
    
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            egresado = Egresado.query.get(codigo)
            if not egresado:
                return {'error': 'Egresado no encontrado'}, 404
            
            egresado.estado = 'I'
            db.session.commit()
            return {'message': 'Egresado eliminado exitosamente'}, 200
        
        except OperationalError as e:
            if attempt < max_retries - 1:
                db.session.rollback()
                time.sleep(retry_delay)
                continue
            else:
                return {'error': 'Error de conexión con la base de datos. Por favor, intenta nuevamente.'}, 500
        except Exception as e:
            db.session.rollback()
            return {'error': f'Error al eliminar el egresado: {str(e)}'}, 500

def restaurar_egresado(codigo):
    """Restaurar egresado eliminado lógicamente con retry para manejo de errores de conexión"""
    from sqlalchemy.exc import OperationalError
    import time
    
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            egresado = Egresado.query.get(codigo)
            if not egresado:
                return {'error': 'Egresado no encontrado'}, 404
            
            egresado.estado = 'A'
            db.session.commit()
            return {'message': 'Egresado restaurado exitosamente'}, 200
        
        except OperationalError as e:
            if attempt < max_retries - 1:
                db.session.rollback()
                time.sleep(retry_delay)
                continue
            else:
                return {'error': 'Error de conexión con la base de datos. Por favor, intenta nuevamente.'}, 500
        except Exception as e:
            db.session.rollback()
            return {'error': f'Error al restaurar el egresado: {str(e)}'}, 500

def eliminar_egresado_fisico(codigo):
    """Eliminar egresado físicamente de la base de datos"""
    egresado = Egresado.query.get(codigo)
    if not egresado:
        return {'error': 'Egresado no encontrado'}, 404
    
    try:
        db.session.delete(egresado)
        db.session.commit()
        return {'message': 'Egresado eliminado permanentemente'}, 200
        
    except Exception as e:
        db.session.rollback()
        return {'error': f'Error al eliminar el egresado: {str(e)}'}, 500

def crear_egresado_con_detalle(data):
    """Crear egresado (cabecera) y detalle_egresado (detalle) en una sola transacción"""
    try:
        # Extraer datos de la estructura anidada
        datos_egresado = data.get('egresado', {})
        datos_detalle = data.get('detalle', {})
        
        # Validar que existan los objetos anidados
        if not datos_egresado:
            return {'error': 'El objeto "egresado" es requerido en la estructura anidada.'}, 400
        if not datos_detalle:
            return {'error': 'El objeto "detalle" es requerido en la estructura anidada.'}, 400

        # Validar DNI único
        if not validar_dni(datos_egresado['dni']):
            return {'error': 'El DNI ya está registrado.'}, 400

        # Validar Código único
        if not validar_codigo(datos_egresado['codigo']):
            return {'error': 'El código ya está registrado.'}, 400

        # Validar correo electrónico
        if not validar_correo(datos_egresado['correo']):
            return {'error': 'Correo electrónico inválido.'}, 400

        # Validar teléfono
        if datos_egresado.get('telefono') and not validar_telefono(datos_egresado['telefono']):
            return {'error': 'Número de teléfono inválido. Debe contener solo números y tener 9 dígitos.'}, 400

        # Validar nombre y apellidos
        if not validar_nombre_apellido(datos_egresado['nombre']):
            return {'error': 'El nombre contiene caracteres no válidos.'}, 400
        if not validar_nombre_apellido(datos_egresado['apellidos']):
            return {'error': 'Los apellidos contienen caracteres no válidos.'}, 400

        # Crear nuevo egresado (cabecera)
        nuevo_egresado = Egresado(
            codigo=datos_egresado['codigo'],
            nombre=datos_egresado['nombre'],
            apellidos=datos_egresado['apellidos'],
            dni=datos_egresado['dni'],
            fecha_nacimiento=datos_egresado.get('fecha_nacimiento'),
            sexo=datos_egresado.get('sexo'),
            direccion=datos_egresado.get('direccion'),
            telefono=datos_egresado.get('telefono', ''),
            telefono_referencia=datos_egresado.get('telefono_referencia'),
            correo=datos_egresado['correo'],
            es_conviviente=datos_egresado.get('es_conviviente', False),
            estado_civil_id=datos_egresado.get('estado_civil_id'),
            cantidad_hijos=datos_egresado.get('cantidad_hijos', 0),
            tiene_discapacidad=datos_egresado.get('tiene_discapacidad', False),
            carrera_id=datos_egresado['carrera_id'],
            anio_ingreso=datos_egresado.get('anio_ingreso'),
            anio_egreso=datos_egresado.get('anio_egreso'),
            es_titulado=datos_egresado.get('es_titulado', False),
            anio_titulacion=datos_egresado.get('anio_titulacion'),
            estado=datos_egresado.get('estado', 'A')
        )
        db.session.add(nuevo_egresado)

        # Remover el campo estado del detalle si viene (no se permite modificar en creación)
        if 'estado' in datos_detalle:
            del datos_detalle['estado']
        
        # Crear detalle del egresado (usar el código del egresado)
        # El estado siempre se establece como 'A' (activo) - no se permite modificar en creación
        nuevo_detalle = DetalleEgresado(
            codigo_egresado=datos_egresado['codigo'],  # Usar el código del egresado creado
            fecha_egreso=datos_detalle.get('fecha_egreso'),
            empresa_actual=datos_detalle.get('empresa_actual'),
            cargo_actual=datos_detalle.get('cargo_actual'),
            pais_residencia=datos_detalle.get('pais_residencia'),
            ciudad_residencia=datos_detalle.get('ciudad_residencia'),
            fecha_incorporacion=datos_detalle.get('fecha_incorporacion'),
            area_trabajo=datos_detalle.get('area_trabajo'),
            sueldo_actual=datos_detalle.get('sueldo_actual'),
            estado='A'  # Siempre se establece como 'A' (activo) - no se permite modificar
        )
        db.session.add(nuevo_detalle)

        # Commit de la transacción (todo o nada)
        db.session.commit()
        
        # Retornar ambos objetos creados
        return {
            'message': 'Egresado y detalle creados exitosamente en una sola transacción',
            'egresado': nuevo_egresado.to_dict(),
            'detalle': nuevo_detalle.to_dict()
        }, 201
        
    except Exception as e:
        db.session.rollback()
        return {'error': f'Error al crear el egresado con detalle: {str(e)}'}, 500

def actualizar_egresado_con_detalle(codigo, data):
    """Actualizar egresado (cabecera) y detalle_egresado (detalle) en una sola transacción"""
    try:
        # Obtener el egresado
        egresado = Egresado.query.get(codigo)
        if not egresado:
            return {'error': 'Egresado no encontrado'}, 404

        # Extraer datos de la estructura anidada
        datos_egresado = data.get('egresado', {})
        datos_detalle = data.get('detalle', {})

        # Validar DNI único si se está actualizando
        if datos_egresado.get('dni') and datos_egresado['dni'] != egresado.dni:
            if not validar_dni(datos_egresado['dni']):
                return {'error': 'El DNI ya está registrado.'}, 400

        # Validar correo electrónico si se está actualizando
        if datos_egresado.get('correo') and datos_egresado['correo'] != egresado.correo:
            if not validar_correo(datos_egresado['correo']):
                return {'error': 'Correo electrónico inválido.'}, 400

        # Validar teléfono si se está actualizando
        if datos_egresado.get('telefono') and not validar_telefono(datos_egresado['telefono']):
            return {'error': 'Número de teléfono inválido. Debe contener solo números y tener 9 dígitos.'}, 400

        # Validar nombre y apellidos si se están actualizando
        if datos_egresado.get('nombre') and not validar_nombre_apellido(datos_egresado['nombre']):
            return {'error': 'El nombre contiene caracteres no válidos.'}, 400
        if datos_egresado.get('apellidos') and not validar_nombre_apellido(datos_egresado['apellidos']):
            return {'error': 'Los apellidos contienen caracteres no válidos.'}, 400

        # Actualizar campos del egresado (solo los que vienen en datos_egresado)
        if datos_egresado:
            for key, value in datos_egresado.items():
                if hasattr(egresado, key) and value is not None:
                    setattr(egresado, key, value)

        # Buscar el detalle del egresado (puede haber múltiples, tomamos el primero activo o el primero)
        detalle = DetalleEgresado.query.filter_by(codigo_egresado=codigo).first()
        
        if datos_detalle:
            if not detalle:
                # Si no existe detalle, crear uno nuevo
                # El estado siempre se establece como 'A' (activo) - no se permite modificar en creación
                nuevo_detalle = DetalleEgresado(
                    codigo_egresado=codigo,
                    fecha_egreso=datos_detalle.get('fecha_egreso'),
                    empresa_actual=datos_detalle.get('empresa_actual'),
                    cargo_actual=datos_detalle.get('cargo_actual'),
                    pais_residencia=datos_detalle.get('pais_residencia'),
                    ciudad_residencia=datos_detalle.get('ciudad_residencia'),
                    fecha_incorporacion=datos_detalle.get('fecha_incorporacion'),
                    area_trabajo=datos_detalle.get('area_trabajo'),
                    sueldo_actual=datos_detalle.get('sueldo_actual'),
                    estado='A'  # Siempre se establece como 'A' (activo) - no se permite modificar
                )
                db.session.add(nuevo_detalle)
                detalle = nuevo_detalle
            else:
                # Actualizar campos del detalle (solo los que vienen en datos_detalle)
                for key, value in datos_detalle.items():
                    if hasattr(detalle, key) and value is not None:
                        setattr(detalle, key, value)

        # Commit de la transacción (todo o nada)
        db.session.commit()
        
        # Retornar ambos objetos actualizados
        return {
            'message': 'Egresado y detalle actualizados exitosamente en una sola transacción',
            'egresado': egresado.to_dict(),
            'detalle': detalle.to_dict() if detalle else None
        }, 200
        
    except Exception as e:
        db.session.rollback()
        return {'error': f'Error al actualizar el egresado con detalle: {str(e)}'}, 500

