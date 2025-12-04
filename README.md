# Sistema de Seguimiento de Egresados


## **Configuración Inicial**

### **Paso 1: Clonar el proyecto**
```bash


### **Paso 2: Ejecutar setup automático**
```bash
python setup.py
```

Este script automáticamente:
- ✅ Crea el entorno virtual (`SegEgresados`)
- ✅ Instala todas las dependencias
- ✅ Crea el archivo `config.env` desde la plantilla
- ✅ Verifica que todo esté correcto

### **Paso 3: Configurar tu base de datos**

**IMPORTANTE:** Edita el archivo `config.env` y configura tus credenciales de PostgreSQL:

```env
DB_HOST=tu_host
DB_NAME=nombre_base_de_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_SSLMODE=require  # Para bases de datos en la nube (Neon, etc.)
```


```bash
# Primera vez después de clonar:
python setup.py              # Configura todo automáticamente
# Edita config.env con tus credenciales
SegEgresados\Scripts\Activate.ps1
python run.py                # Ejecuta la aplicación

# Próximas veces:
SegEgresados\Scripts\Activate.ps1
python run.py
```

**Nota:** Los archivos de configuración (`config.env` y `database_config.py`) ya vienen incluidos en el repositorio para facilitar la ejecución. Si necesitas modificar la configuración, edita estos archivos directamente.


### **ENDPOINTS PRINCIPALES:**

**EGRESADOS:**
- `GET /egresados` - Listar egresados
- `GET /egresados/{codigo}` - Obtener egresado
- `POST /egresados` - Crear egresado
- `PUT /egresados/{codigo}` - Actualizar egresado
- `DELETE /egresados/{codigo}` - Eliminar lógicamente
- `PUT /egresados/restaurar/{codigo}` - Restaurar egresado

**EMPRESAS:**
- `GET /empresas` - Listar empresas
- `POST /empresas` - Crear empresa
- `PUT /empresas/{id_empresa}` - Actualizar empresa
- `DELETE /empresas/{id_empresa}` - Eliminar lógicamente
- `PUT /empresas/restaurar/{id_empresa}` - Restaurar empresa

**CATÁLOGOS:**
- `GET /carreras` - Carreras profesionales
- `GET /estados-civiles` - Estados civiles
- `GET /actividades-economicas` - Actividades económicas
- `GET /certificaciones` - Certificaciones

**AUTENTICACIÓN:**
- `POST /login` - Iniciar sesión
- `POST /register` - Registrar nuevo usuario
- `GET /profile` - Obtener perfil de usuario
- `PUT /profile` - Actualizar perfil
- `PUT /change-password` - Cambiar contraseña

## Base de Datos

### Tablas Principales:
- `usuarios` - Usuarios del sistema
- `egresado` - Información básica de egresados
- `detalle_egresado` - Información laboral
- `empresa` - Empresas
- `certificacion` - Certificaciones
