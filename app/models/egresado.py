# Modelo de datos para egresados
from .. import db

class Egresado(db.Model):
    __tablename__ = 'egresado'

    codigo = db.Column(db.String(20), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(8), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.Date)
    sexo = db.Column(db.String(1))
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(15))
    telefono_referencia = db.Column(db.String(15))
    correo = db.Column(db.String(120), unique=True, nullable=False)
    es_conviviente = db.Column(db.Boolean, default=False)
    estado_civil_id = db.Column(db.Integer)
    cantidad_hijos = db.Column(db.Integer, default=0)
    tiene_discapacidad = db.Column(db.Boolean, default=False)
    carrera_id = db.Column(db.Integer, nullable=False)
    anio_ingreso = db.Column(db.Integer)
    anio_egreso = db.Column(db.Integer)
    es_titulado = db.Column(db.Boolean, default=False)
    anio_titulacion = db.Column(db.Integer)
    estado = db.Column(db.String(1), nullable=False, default='A')  # A = activo, I = inactivo

    def to_dict(self):
        return {
            'codigo': self.codigo,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'dni': self.dni,
            'fecha_nacimiento': self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            'sexo': self.sexo,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'telefono_referencia': self.telefono_referencia,
            'correo': self.correo,
            'es_conviviente': self.es_conviviente,
            'estado_civil_id': self.estado_civil_id,
            'cantidad_hijos': self.cantidad_hijos,
            'tiene_discapacidad': self.tiene_discapacidad,
            'carrera_id': self.carrera_id,
            'anio_ingreso': self.anio_ingreso,
            'anio_egreso': self.anio_egreso,
            'es_titulado': self.es_titulado,
            'anio_titulacion': self.anio_titulacion,
            'estado': self.estado
        }

