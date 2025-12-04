# =====================================================
# CONFIGURACIÓN DE BASE DE DATOS POSTGRESQL (NEON)
# =====================================================

# Configuración de la base de datos Neon
DB_CONFIG = {
    'type': 'postgresql',
    'user': 'neondb_owner',
    'password': 'npg_ueY7Mml0PzkZ',
    'host': 'ep-orange-frost-ad09m9xe-pooler.c-2.us-east-1.aws.neon.tech',
    'port': '5432',
    'database': 'neondb'
}

# URI de conexión para SQLAlchemy
SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?sslmode=require"

# String de conexión para psql (para ejecutar scripts manualmente)
PSQL_CONNECTION_STRING = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?sslmode=require&channel_binding=require"

print(f"Configuración de base de datos: {DB_CONFIG['type']}")
print(f"Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
print(f"Base de datos: {DB_CONFIG['database']}")
print(f"Usuario: {DB_CONFIG['user']}")
