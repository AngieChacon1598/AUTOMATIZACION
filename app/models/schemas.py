# Schemas de Marshmallow para validación de usuarios
from marshmallow import Schema, fields, validate

class UsuarioSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=100))
    apellidos = fields.String(required=True, validate=validate.Length(min=1, max=100))
    rol = fields.String(validate=validate.OneOf(['admin', 'usuario', 'moderador']), load_default='usuario')

class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

# Schema de Marshmallow para validaciones de Egresado
class EgresadoSchema(Schema):
    codigo = fields.String(required=True)
    nombre = fields.String(required=True, validate=validate.Length(min=1))
    apellidos = fields.String(required=True, validate=validate.Length(min=1))
    dni = fields.String(required=True, validate=validate.Length(equal=8))
    fecha_nacimiento = fields.Date(allow_none=True)
    sexo = fields.String(allow_none=True)
    direccion = fields.String(allow_none=True)
    telefono = fields.String(allow_none=True)
    telefono_referencia = fields.String(allow_none=True)
    correo = fields.Email(required=True)
    es_conviviente = fields.Boolean(allow_none=True)
    estado_civil_id = fields.Integer(allow_none=True)
    cantidad_hijos = fields.Integer(allow_none=True)
    tiene_discapacidad = fields.Boolean(allow_none=True)
    carrera_id = fields.Integer(required=True)
    anio_ingreso = fields.Integer(allow_none=True)
    anio_egreso = fields.Integer(allow_none=True)
    es_titulado = fields.Boolean(allow_none=True)
    anio_titulacion = fields.Integer(allow_none=True)
    estado = fields.String(validate=validate.OneOf(["A", "I"]), load_default="A")

# Schema para actualizaciones de Egresado (campos opcionales)
class EgresadoUpdateSchema(Schema):
    codigo = fields.String(allow_none=True)
    nombre = fields.String(allow_none=True, validate=validate.Length(min=1))
    apellidos = fields.String(allow_none=True, validate=validate.Length(min=1))
    dni = fields.String(allow_none=True, validate=validate.Length(equal=8))
    fecha_nacimiento = fields.Date(allow_none=True)
    sexo = fields.String(allow_none=True)
    direccion = fields.String(allow_none=True)
    telefono = fields.String(allow_none=True)
    telefono_referencia = fields.String(allow_none=True)
    correo = fields.Email(allow_none=True)
    es_conviviente = fields.Boolean(allow_none=True)
    estado_civil_id = fields.Integer(allow_none=True)
    cantidad_hijos = fields.Integer(allow_none=True)
    tiene_discapacidad = fields.Boolean(allow_none=True)
    carrera_id = fields.Integer(allow_none=True)
    anio_ingreso = fields.Integer(allow_none=True)
    anio_egreso = fields.Integer(allow_none=True)
    es_titulado = fields.Boolean(allow_none=True)
    anio_titulacion = fields.Integer(allow_none=True)
    estado = fields.String(validate=validate.OneOf(["A", "I"]), allow_none=True)

# Schema de Marshmallow para validaciones de Detalle Egresado
class DetalleEgresadoSchema(Schema):
    codigo_egresado = fields.String(required=True)
    fecha_egreso = fields.Date(allow_none=True)
    empresa_actual = fields.String(allow_none=True)
    cargo_actual = fields.String(allow_none=True)
    pais_residencia = fields.String(allow_none=True)
    ciudad_residencia = fields.String(allow_none=True)
    fecha_incorporacion = fields.Date(allow_none=True)
    area_trabajo = fields.String(allow_none=True)
    sueldo_actual = fields.Decimal(allow_none=True)
    # estado no se permite en creación - se establece automáticamente como 'A'
    estado = fields.String(dump_only=True)  # Solo para serialización, no se acepta en creación

# Schema para DetalleEgresado sin codigo_egresado (se asigna automáticamente)
class DetalleEgresadoSinCodigoSchema(Schema):
    fecha_egreso = fields.Date(allow_none=True)
    empresa_actual = fields.String(allow_none=True)
    cargo_actual = fields.String(allow_none=True)
    pais_residencia = fields.String(allow_none=True)
    ciudad_residencia = fields.String(allow_none=True)
    fecha_incorporacion = fields.Date(allow_none=True)
    area_trabajo = fields.String(allow_none=True)
    sueldo_actual = fields.Decimal(allow_none=True)
    # estado no se permite en creación - se establece automáticamente como 'A'
    estado = fields.String(dump_only=True)  # Solo para serialización, no se acepta en creación

# Schema combinado para crear Egresado con Detalle en una sola transacción (estructura anidada)
class EgresadoConDetalleSchema(Schema):
    # Campos del Egresado (cabecera) - estructura anidada
    egresado = fields.Nested(EgresadoSchema, required=True)
    
    # Campos del DetalleEgresado (detalle) - estructura anidada
    detalle = fields.Nested(DetalleEgresadoSinCodigoSchema, required=True)

# Schema para actualizar DetalleEgresado sin codigo_egresado (todos opcionales)
class DetalleEgresadoUpdateSchema(Schema):
    fecha_egreso = fields.Date(allow_none=True)
    empresa_actual = fields.String(allow_none=True)
    cargo_actual = fields.String(allow_none=True)
    pais_residencia = fields.String(allow_none=True)
    ciudad_residencia = fields.String(allow_none=True)
    fecha_incorporacion = fields.Date(allow_none=True)
    area_trabajo = fields.String(allow_none=True)
    sueldo_actual = fields.Decimal(allow_none=True)
    estado = fields.String(validate=validate.OneOf(["A", "I"]), allow_none=True)

# Schema combinado para actualizar Egresado con Detalle en una sola transacción (estructura anidada)
class EgresadoConDetalleUpdateSchema(Schema):
    # Campos del Egresado (cabecera) - estructura anidada (todos opcionales)
    egresado = fields.Nested(EgresadoUpdateSchema, allow_none=True)
    
    # Campos del DetalleEgresado (detalle) - estructura anidada (todos opcionales)
    detalle = fields.Nested(DetalleEgresadoUpdateSchema, allow_none=True)

# Schema de Marshmallow para validaciones de Encuesta Egresado
# Solo incluye campos que existen en la base de datos actual
class EncuestaEgresadoSchema(Schema):
    codigo_egresado = fields.String(required=True, validate=validate.Length(min=1))
    fecha_aplicacion = fields.Date(required=True)
    trabaja_actualmente = fields.Boolean(allow_none=True)
    tiene_negocio = fields.Boolean(allow_none=True)
    ingreso_mensual = fields.String(allow_none=True)
    ingresos_mensuales = fields.String(allow_none=True)  # Alias de ingreso_mensual
    tipo_contrato = fields.String(allow_none=True)
    tipo_empleo = fields.String(allow_none=True)
    area_trabajo = fields.String(allow_none=True)
    actividad_economica_id = fields.Integer(allow_none=True)
    relacion_carrera = fields.String(allow_none=True)
    medios_busqueda = fields.String(allow_none=True)
    cantidad_empleos_ultimo_ano = fields.Integer(allow_none=True)
    cantidad_empleos_carrera = fields.Integer(allow_none=True)
    nombre_empresa_actual = fields.String(allow_none=True)
    nombre_jefe_inmediato = fields.String(allow_none=True)
    telefono_empresa = fields.String(allow_none=True)
    pagina_web_empresa = fields.String(allow_none=True)
    correo_empresa = fields.String(allow_none=True)
    cantidad_trabajadores = fields.String(allow_none=True)
    tipo_constitucion = fields.String(allow_none=True)
    actividad_economica_negocio_id = fields.Integer(allow_none=True)
    estado = fields.String(validate=validate.OneOf(["A", "I"]), load_default="A", allow_none=True)

# Schema para actualizar Encuesta Egresado (todos los campos opcionales excepto los requeridos)
# Solo incluye campos que existen en la base de datos actual
class EncuestaEgresadoUpdateSchema(Schema):
    codigo_egresado = fields.String(allow_none=True, validate=validate.Length(min=1))
    fecha_aplicacion = fields.Date(allow_none=True)
    trabaja_actualmente = fields.Boolean(allow_none=True)
    tiene_negocio = fields.Boolean(allow_none=True)
    ingreso_mensual = fields.String(allow_none=True)
    ingresos_mensuales = fields.String(allow_none=True)  # Alias de ingreso_mensual
    tipo_contrato = fields.String(allow_none=True)
    tipo_empleo = fields.String(allow_none=True)
    area_trabajo = fields.String(allow_none=True)
    actividad_economica_id = fields.Integer(allow_none=True)
    relacion_carrera = fields.String(allow_none=True)
    medios_busqueda = fields.String(allow_none=True)
    cantidad_empleos_ultimo_ano = fields.Integer(allow_none=True)
    cantidad_empleos_carrera = fields.Integer(allow_none=True)
    nombre_empresa_actual = fields.String(allow_none=True)
    nombre_jefe_inmediato = fields.String(allow_none=True)
    telefono_empresa = fields.String(allow_none=True)
    pagina_web_empresa = fields.String(allow_none=True)
    correo_empresa = fields.String(allow_none=True)
    cantidad_trabajadores = fields.String(allow_none=True)
    tipo_constitucion = fields.String(allow_none=True)
    actividad_economica_negocio_id = fields.Integer(allow_none=True)
    estado = fields.String(validate=validate.OneOf(["A", "I"]), allow_none=True)