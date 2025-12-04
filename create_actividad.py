# Script to ensure actividad_economica table exists and insert a sample record
import os
from app import app, db
from app.models.actividad_economica import ActividadEconomica

with app.app_context():
    # Create tables (if not exist)
    db.create_all()
    # Check if a record exists
    if not ActividadEconomica.query.filter_by(nombre='Administración Pública').first():
        ae = ActividadEconomica(nombre='Administración Pública', codigo='AP')
        db.session.add(ae)
        db.session.commit()
        print('ActividadEconomica record inserted')
    else:
        print('ActividadEconomica record already exists')
