# Modelo de datos para detalle de egresados
from .. import db

class DetalleEgresado(db.Model):
    __tablename__ = 'detalle_egresado'

    id_detalle = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo_egresado = db.Column(db.String(20), db.ForeignKey('egresado.codigo'), nullable=False)
    fecha_egreso = db.Column(db.Date)
    empresa_actual = db.Column(db.String(100))
    cargo_actual = db.Column(db.String(100))
    pais_residencia = db.Column(db.String(50))
    ciudad_residencia = db.Column(db.String(50))
    fecha_incorporacion = db.Column(db.Date)
    area_trabajo = db.Column(db.String(50))
    sueldo_actual = db.Column(db.Numeric(10, 2))
    estado = db.Column(db.String(1), nullable=False, default='A')  # A = activo, I = inactivo

    # Relación con Egresado
    egresado = db.relationship('Egresado', backref='detalles')

    def to_dict(self):
        return {
            'id_detalle': self.id_detalle,
            'codigo_egresado': self.codigo_egresado,
            'fecha_egreso': self.fecha_egreso.isoformat() if self.fecha_egreso else None,
            'empresa_actual': self.empresa_actual,
            'cargo_actual': self.cargo_actual,
            'pais_residencia': self.pais_residencia,
            'ciudad_residencia': self.ciudad_residencia,
            'fecha_incorporacion': self.fecha_incorporacion.isoformat() if self.fecha_incorporacion else None,
            'area_trabajo': self.area_trabajo,
            'sueldo_actual': float(self.sueldo_actual) if self.sueldo_actual else None,
            'estado': self.estado,
            'egresado_nombre': f"{self.egresado.nombre} {self.egresado.apellidos}" if self.egresado else None
        }

