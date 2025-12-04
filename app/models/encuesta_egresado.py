# Modelo de datos para encuestas de egresados
from .. import db


class EncuestaEgresado(db.Model):
    __tablename__ = 'encuesta_egresado'

    id_encuesta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo_egresado = db.Column(db.String(20), db.ForeignKey(
        'egresado.codigo'), nullable=False)
    fecha_aplicacion = db.Column(db.Date, nullable=False)

    # SITUACIÓN LABORAL
    trabaja_actualmente = db.Column(db.Boolean)
    # puesto_actual no existe en la base de datos actual - removido
    # 'Contrato de trabajo', 'Recibo por honorario', 'Ninguna'
    tipo_contrato = db.Column(db.String(50))
    # 'Institución pública', 'Empresa privada', 'Independiente'
    tipo_empleo = db.Column(db.String(50))
    ingreso_mensual = db.Column(db.String(50))  # Rangos de ingreso (acepta alias ingresos_mensuales)
    area_trabajo = db.Column(db.String(100))
    actividad_economica_id = db.Column(
        db.Integer, db.ForeignKey('actividad_economica.id_actividad'))
    # 'Directamente', 'Indirectamente', 'Nada relacionado'
    relacion_carrera = db.Column(db.String(50))

    # BÚSQUEDA DE EMPLEO
    # Múltiples opciones separadas por comas
    medios_busqueda = db.Column(db.String(255))
    cantidad_empleos_ultimo_ano = db.Column(db.Integer, default=0)
    cantidad_empleos_carrera = db.Column(db.Integer, default=0)

    # EMPRESA ACTUAL
    nombre_empresa_actual = db.Column(db.String(150))
    nombre_jefe_inmediato = db.Column(db.String(100))
    telefono_empresa = db.Column(db.String(15))
    pagina_web_empresa = db.Column(db.String(200))
    correo_empresa = db.Column(db.String(120))

    # TRABAJO INDEPENDIENTE
    tiene_negocio = db.Column(db.Boolean, default=False)
    # tipo_negocio no existe en la base de datos actual - removido
    cantidad_trabajadores = db.Column(db.String(50))  # Rangos de trabajadores
    # 'Persona natural con RUC', 'EIRL', 'SRL', etc.
    # Nota: La columna en BD se llama tipo_constituccion (doble 'c')
    tipo_constitucion = db.Column('tipo_constituccion', db.String(50))
    actividad_economica_negocio_id = db.Column(
        db.Integer, db.ForeignKey('actividad_economica.id_actividad'))

    # observaciones no existe en la base de datos actual - removido

    estado = db.Column(db.String(1), nullable=False, default='A')

    def to_dict(self):
        return {
            'id_encuesta': self.id_encuesta,
            'codigo_egresado': self.codigo_egresado,
            'fecha_aplicacion': self.fecha_aplicacion.isoformat() if self.fecha_aplicacion else None,
            'trabaja_actualmente': self.trabaja_actualmente,
            'tipo_contrato': self.tipo_contrato,
            'tipo_empleo': self.tipo_empleo,
            'ingreso_mensual': self.ingreso_mensual,
            'ingresos_mensuales': self.ingreso_mensual,  # Alias según manual
            'area_trabajo': self.area_trabajo,
            'actividad_economica_id': self.actividad_economica_id,
            'relacion_carrera': self.relacion_carrera,
            'medios_busqueda': self.medios_busqueda,
            'cantidad_empleos_ultimo_ano': self.cantidad_empleos_ultimo_ano,
            'cantidad_empleos_carrera': self.cantidad_empleos_carrera,
            'nombre_empresa_actual': self.nombre_empresa_actual,
            'nombre_jefe_inmediato': self.nombre_jefe_inmediato,
            'telefono_empresa': self.telefono_empresa,
            'pagina_web_empresa': self.pagina_web_empresa,
            'correo_empresa': self.correo_empresa,
            'tiene_negocio': self.tiene_negocio,
            'cantidad_trabajadores': self.cantidad_trabajadores,
            'tipo_constitucion': self.tipo_constitucion,
            'actividad_economica_negocio_id': self.actividad_economica_negocio_id,
            'estado': self.estado
        }
