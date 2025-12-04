# Modelo para la tabla actividad_economica
from .. import db

class ActividadEconomica(db.Model):
    __tablename__ = 'actividad_economica'

    id_actividad = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(150), unique=True, nullable=False)
    codigo = db.Column(db.String(10))
    estado = db.Column(db.String(1), default='A')

    def to_dict(self):
        return {
            'id_actividad': self.id_actividad,
            'nombre': self.nombre,
            'codigo': self.codigo,
            'estado': self.estado,
        }
