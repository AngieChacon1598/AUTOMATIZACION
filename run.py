# Punto de entrada para ejecutar la aplicación
import os
from dotenv import load_dotenv
from app import app, db

# Cargar variables de entorno
load_dotenv('config.env')

if __name__ == '__main__':
    with app.app_context():
        # Crear tablas si no existen
        db.create_all()
        print("Tablas de base de datos creadas/verificadas")
    
    # Obtener configuración desde variables de entorno
    # Render usa PORT, pero mantenemos FLASK_PORT para compatibilidad local
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('PORT', os.getenv('FLASK_PORT', '5001')))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Ejecutar la aplicación
    app.run(debug=debug, host=host, port=port)