# Modelo de datos para certificaciones
from .. import db

class Certificacion(db.Model):
    __tablename__ = 'certificacion'

    id_certificacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo_egresado = db.Column(db.String(20), db.ForeignKey('egresado.codigo'), nullable=False)
    nombre = db.Column(db.String(150), nullable=False)
    institucion = db.Column(db.String(150), nullable=False)
    fecha_obtencion = db.Column(db.Date, nullable=False)
    archivo = db.Column(db.String(255))
    estado = db.Column(db.String(1), nullable=False, default='A')  # A = activo, I = inactivo

    # Relación con Egresado
    egresado = db.relationship('Egresado', backref='certificaciones')

    def to_dict(self):
        return {
            'id_certificacion': self.id_certificacion,
            'codigo_egresado': self.codigo_egresado,
            'nombre': self.nombre,
            'institucion': self.institucion,
            'fecha_obtencion': self.fecha_obtencion.isoformat() if self.fecha_obtencion else None,
            'archivo': self.archivo,
            'estado': self.estado
        }

