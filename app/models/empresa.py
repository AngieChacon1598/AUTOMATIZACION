# Modelo de datos para empresas
from .. import db

class Empresa(db.Model):
    __tablename__ = 'empresa'

    id_empresa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    ruc = db.Column(db.String(11), unique=True, nullable=False)
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(15))
    correo = db.Column(db.String(120))
    estado = db.Column(db.String(1), nullable=False, default='A')  # A = activo, I = inactivo

    def to_dict(self):
        return {
            'id_empresa': self.id_empresa,
            'nombre': self.nombre,
            'ruc': self.ruc,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'correo': self.correo,
            'estado': self.estado
        }

