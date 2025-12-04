# Configuración (DB, variables de entorno, etc.)
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno desde config.env si existe (para desarrollo local)
# En producción (Render), las variables de entorno se configuran directamente
config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.env')
if os.path.exists(config_path):
    load_dotenv(config_path)
else:
    # En producción, cargar desde variables de entorno del sistema
    load_dotenv(override=True)

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Configuración JWT desde variables de entorno
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'tu_clave_secreta_muy_segura_cambiar_en_produccion')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', '24'))
MAX_LOGIN_ATTEMPTS = int(os.getenv('MAX_LOGIN_ATTEMPTS', '5'))
LOCKOUT_DURATION_MINUTES = int(os.getenv('LOCKOUT_DURATION_MINUTES', '30'))

# URL del script de Google desde variables de entorno
GOOGLE_SCRIPT_URL = os.getenv('GOOGLE_SCRIPT_URL', 'https://script.google.com/macros/s/AKfycbzI_811QN5p0WNsmcjpYxzfvLmMQJL6ZrkKFqKNqye9MSJQ6hVYbOVvOYnf1FYof74B/exec')

# Configuración de base de datos desde variables de entorno
DB_CONFIG = {
    'type': os.getenv('DB_TYPE', 'postgresql'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '5432')),
    'database': os.getenv('DB_NAME', 'seguimiento_egresados'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres')
}

# URI de conexión para SQLAlchemy
if DB_CONFIG['type'] == 'postgresql':
    # SSL opcional - configurable desde env
    sslmode = os.getenv('DB_SSLMODE', 'require')  # require para producción (cambiar a disable solo para desarrollo local)
    # Agregar parámetros adicionales para mejorar la estabilidad de la conexión
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?sslmode={sslmode}&connect_timeout=10"
else:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_CONFIG['database']}.db"

print(f"Configuración de base de datos: {DB_CONFIG['type']}")
print(f"Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
print(f"Base de datos: {DB_CONFIG['database']}")
print(f"Usuario: {DB_CONFIG['user']}")
if os.path.exists(config_path):
    print(f"Archivo config.env cargado desde: {config_path}")
else:
    print("Usando variables de entorno del sistema (producción)")

def test_connection():
    try:
        if DB_CONFIG.get('type') == 'sqlite':
            import sqlite3
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), DB_CONFIG['database'])
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT sqlite_version();")
            version = cursor.fetchone()
            print(f"Conexión exitosa a SQLite: {version[0]}")
            cursor.close()
            conn.close()
            return True
        else:
            import psycopg2
            conn = psycopg2.connect(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                database=DB_CONFIG['database'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                sslmode='require'
            )
            
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"Conexión exitosa a PostgreSQL: {version[0]}")
            
            cursor.close()
            conn.close()
            return True
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return False

if __name__ == "__main__":
    test_connection()
