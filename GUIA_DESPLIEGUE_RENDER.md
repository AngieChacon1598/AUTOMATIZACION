# Guía de Despliegue en Render

Esta guía te ayudará a desplegar tu backend Flask en Render.

## Prerrequisitos

1. Cuenta en [Render](https://render.com)
2. Repositorio Git (GitHub, GitLab o Bitbucket) con tu código
3. Base de datos PostgreSQL (puedes usar Neon, Render PostgreSQL, o cualquier otra)

## Opción 1: Despliegue usando render.yaml (Recomendado)

### Paso 1: Conectar tu repositorio

1. Inicia sesión en [Render Dashboard](https://dashboard.render.com)
2. Haz clic en **"New +"** y selecciona **"Blueprint"**
3. Conecta tu repositorio de Git
4. Render detectará automáticamente el archivo `render.yaml`
5. Revisa la configuración y haz clic en **"Apply"**

### Paso 2: Configurar variables de entorno

Después de crear el servicio, ve a la sección **"Environment"** y configura las siguientes variables:

#### Variables de Base de Datos
```
DB_TYPE=postgresql
DB_HOST=tu-host-de-postgresql
DB_PORT=5432
DB_NAME=tu-nombre-de-base-de-datos
DB_USER=tu-usuario
DB_PASSWORD=tu-contraseña (marcar como Secret)
DB_SSLMODE=require
```

#### Variables de JWT
```
JWT_SECRET_KEY=tu-clave-secreta-muy-segura (marcar como Secret)
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

#### Variables de Seguridad
```
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION_MINUTES=30
```

#### Variables de Google Script
```
GOOGLE_SCRIPT_URL=tu-url-de-google-script
```

#### Variables de Flask
```
FLASK_ENV=production
FLASK_DEBUG=False
GUNICORN_WORKERS=3
```

**Nota:** Las variables marcadas como "Secret" deben configurarse manualmente en el dashboard de Render por seguridad.

## Opción 2: Despliegue Manual

### Paso 1: Crear un nuevo Web Service

1. En el dashboard de Render, haz clic en **"New +"** → **"Web Service"**
2. Conecta tu repositorio de Git
3. Configura el servicio:
   - **Name:** `seguimiento-egresados-backend` (o el nombre que prefieras)
   - **Environment:** `Docker`
   - **Region:** Elige la región más cercana a tus usuarios
   - **Branch:** `develop` (o la rama que uses)
   - **Root Directory:** Dejar vacío (raíz del proyecto)
   - **Dockerfile Path:** `./Dockerfile`
   - **Docker Context:** `.`

### Paso 2: Configurar variables de entorno

En la sección **"Environment"**, agrega todas las variables mencionadas en la Opción 1.

### Paso 3: Configurar el servicio

- **Plan:** Starter (o el plan que prefieras)
- **Auto-Deploy:** Yes (para despliegues automáticos en cada push)

## Configuración de Base de Datos

### Si usas Render PostgreSQL:

1. Crea una nueva base de datos PostgreSQL en Render
2. Render te proporcionará automáticamente las variables de conexión
3. Puedes usar la opción **"Link Database"** para conectar automáticamente

### Si usas Neon u otra base de datos externa:

1. Obtén las credenciales de conexión de tu proveedor
2. Configura manualmente las variables de entorno en Render

## Verificación del Despliegue

1. Una vez desplegado, Render te proporcionará una URL (ej: `https://tu-app.onrender.com`)
2. Verifica que la aplicación esté funcionando accediendo a la URL
3. Revisa los logs en el dashboard de Render para verificar que no haya errores

## Comandos Útiles

### Ver logs en tiempo real:
Los logs están disponibles en el dashboard de Render en la sección **"Logs"**

### Reiniciar el servicio:
En el dashboard, ve a **"Manual Deploy"** → **"Clear build cache & deploy"**

## Solución de Problemas

### Error: "Cannot connect to database"
- Verifica que las variables de entorno de la base de datos estén correctamente configuradas
- Asegúrate de que `DB_SSLMODE=require` si tu base de datos requiere SSL
- Verifica que la base de datos permita conexiones desde la IP de Render

### Error: "Port already in use"
- Render configura automáticamente la variable `PORT`, no necesitas configurarla manualmente
- El Dockerfile ya está configurado para usar la variable `PORT` de Render

### Error: "Module not found"
- Verifica que `requirements.txt` incluya todas las dependencias necesarias
- Revisa los logs de build para ver qué dependencia falta

### La aplicación no inicia
- Revisa los logs en el dashboard de Render
- Verifica que todas las variables de entorno estén configuradas
- Asegúrate de que `FLASK_ENV=production` y `FLASK_DEBUG=False`

## Notas Importantes

1. **Variables Secretas:** Nunca subas archivos `config.env` con credenciales reales a Git. Usa siempre variables de entorno en Render.

2. **Puerto:** Render asigna automáticamente un puerto y lo expone mediante la variable de entorno `PORT`. El Dockerfile ya está configurado para usarlo.

3. **Base de Datos:** Si usas Neon o una base de datos externa, asegúrate de que permita conexiones desde cualquier IP (o configura el firewall para permitir las IPs de Render).

4. **Auto-Deploy:** Con Auto-Deploy habilitado, cada push a la rama configurada desplegará automáticamente la nueva versión.

5. **Sleep Mode:** En el plan gratuito, Render puede poner el servicio en "sleep" después de 15 minutos de inactividad. La primera solicitud después del sleep puede tardar unos segundos.

## Soporte

Si encuentras problemas, revisa:
- Los logs en el dashboard de Render
- La documentación de Render: https://render.com/docs
- Los issues en tu repositorio

