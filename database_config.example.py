# =====================================================
# CONFIGURACIÓN DE BASE DE DATOS POSTGRESQL - EJEMPLO
# =====================================================

# Configuración de la base de datos
DB_CONFIG = {
    'type': 'postgresql',
    'user': 'tu_usuario',
    'password': 'tu_password',
    'host': 'tu_host.ejemplo.com',
    'port': '5432',
    'database': 'nombre_base_datos'
}

# URI de conexión para SQLAlchemy
SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?sslmode=require"

# String de conexión para psql (para ejecutar scripts manualmente)
PSQL_CONNECTION_STRING = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?sslmode=require&channel_binding=require"

print(f"Configuración de base de datos: {DB_CONFIG['type']}")
print(f"Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
print(f"Base de datos: {DB_CONFIG['database']}")
print(f"Usuario: {DB_CONFIG['user']}")

