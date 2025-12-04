# GUÍA CRUD EGRESADOS


## 1. LOGIN

### Request
- Método: `POST`
- URL: `http://localhost:5001/login`
- Headers:
  ```
  Content-Type: application/json
  ```
- Body (raw JSON):
  ```json
  {
    "username": "admin",
    "password": "admin123"
  }
  ```

### Script Post-Response (guardar token automáticamente)
```javascript
if (pm.response.code === 200) {
    const response = pm.response.json();
    pm.environment.set("token", response.token);
    console.log("Token guardado:", response.token);
}
```

### Respuesta esperada
```json
{
  "message": "Login exitoso",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id_usuario": 1,
    "username": "admin",
    "email": "admin@sistema.com",
    "nombre": "Administrador",
    "apellidos": "Sistema",
    "rol": "admin",
    "estado": "A"
  }
}
```

---

## 2. LISTAR EGRESADOS

### Request
- Método: `GET`
- URL: `http://localhost:5001/egresados`
- Headers:
  ```
  Content-Type: application/json
  Authorization: Bearer {{token}}
  ```
- Query Params (opcionales):
  - `estado`: `A` (activos) o `I` (inactivos)
  - `page`: `1`
  - `per_page`: `10`
  - `apellidos`: `Pérez` (búsqueda parcial)
  - `dni`: `12345678` (búsqueda parcial)
  - `carrera`: `Ingeniería` (búsqueda parcial)

### Respuesta esperada
```json
{
  "egresados": [
    {
      "codigo": "EG001",
      "nombre": "María",
      "apellidos": "Pérez Gómez",
      "dni": "12345678",
      "fecha_nacimiento": "1995-03-15",
      "sexo": "F",
      "direccion": "Av. Principal 123",
      "telefono": "987654321",
      "telefono_referencia": "912345678",
      "correo": "maria.perez@example.com",
      "es_conviviente": false,
      "estado_civil_id": 1,
      "cantidad_hijos": 0,
      "tiene_discapacidad": false,
      "carrera_id": 2,
      "anio_ingreso": 2020,
      "anio_egreso": "2023",
      "es_titulado": true,
      "anio_titulacion": "2024",
      "estado": "A"
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 10,
  "pages": 1
}
```

---

## 3. OBTENER EGRESADO ESPECÍFICO

### Request
- Método: `GET`
- URL: `http://localhost:5001/egresados/EG001`
- Headers:
  ```
  Content-Type: application/json
  Authorization: Bearer {{token}}
  ```

### Respuesta esperada
```json
{
  "codigo": "EG001",
  "nombre": "María",
  "apellidos": "Pérez Gómez",
  "dni": "12345678",
  "fecha_nacimiento": "1995-03-15",
  "sexo": "F",
  "direccion": "Av. Principal 123",
  "telefono": "987654321",
  "telefono_referencia": "912345678",
  "correo": "maria.perez@example.com",
  "es_conviviente": false,
  "estado_civil_id": 1,
  "cantidad_hijos": 0,
  "tiene_discapacidad": false,
  "carrera_id": 2,
  "anio_ingreso": 2020,
  "anio_egreso": "2023",
  "es_titulado": true,
  "anio_titulacion": "2024",
  "estado": "A"
}
```

---

## 4. CREAR EGRESADO

### Request
- Método: `POST`
- URL: `http://localhost:5001/egresados`
- Headers:
  ```
  Content-Type: application/json
  Authorization: Bearer {{token}}
  ```
- Body (raw JSON):
  ```json
  {
    "codigo": "EG013",
    "nombre": "Juan",
    "apellidos": "Pérez García",
    "dni": "87654321",
    "fecha_nacimiento": "1990-01-01",
    "sexo": "M",
    "direccion": "Calle Real 123",
    "telefono": "999999999",
    "telefono_referencia": "888888888",
    "correo": "juan.perez@email.com",
    "es_conviviente": false,
    "estado_civil_id": 1,
    "cantidad_hijos": 0,
    "tiene_discapacidad": false,
    "carrera_id": 1,
    "anio_ingreso": 2020,
    "anio_egreso": "2023",
    "es_titulado": true,
    "anio_titulacion": "2024",
    "estado": "A"
  }
  ```

### Respuesta esperada (201 Created)
```json
{
  "message": "Egresado creado exitosamente",
  "egresado": {
    "codigo": "EG013",
    "nombre": "Juan",
    "apellidos": "Pérez García",
    "dni": "87654321",
    "fecha_nacimiento": "1990-01-01",
    "sexo": "M",
    "direccion": "Calle Real 123",
    "telefono": "999999999",
    "telefono_referencia": "888888888",
    "correo": "juan.perez@email.com",
    "es_conviviente": false,
    "estado_civil_id": 1,
    "cantidad_hijos": 0,
    "tiene_discapacidad": false,
    "carrera_id": 1,
    "anio_ingreso": 2020,
    "anio_egreso": "2023",
    "es_titulado": true,
    "anio_titulacion": "2024",
    "estado": "A"
  }
}
```

---

## 5. ACTUALIZAR EGRESADO

### Request
- Método: `PUT`
- URL: `http://localhost:5001/egresados/EG013`
- Headers:
  ```
  Content-Type: application/json
  Authorization: Bearer {{token}}
  ```
- Body (raw JSON) - Solo campos a actualizar:
  ```json
  {
    "nombre": "Juan Carlos",
    "correo": "juan.carlos@email.com",
    "telefono": "999888777"
  }
  ```

### Respuesta esperada (200 OK)
```json
{
  "message": "Egresado actualizado exitosamente",
  "egresado": {
    "codigo": "EG013",
    "nombre": "Juan Carlos",
    "apellidos": "Pérez García",
    "dni": "87654321",
    "fecha_nacimiento": "1990-01-01",
    "sexo": "M",
    "direccion": "Calle Real 123",
    "telefono": "999888777",
    "telefono_referencia": "888888888",
    "correo": "juan.carlos@email.com",
    "es_conviviente": false,
    "estado_civil_id": 1,
    "cantidad_hijos": 0,
    "tiene_discapacidad": false,
    "carrera_id": 1,
    "anio_ingreso": 2020,
    "anio_egreso": "2023",
    "es_titulado": true,
    "anio_titulacion": "2024",
    "estado": "A"
  }
}
```

---

## 6. ELIMINAR LÓGICAMENTE

### Request
- Método: `DELETE`
- URL: `http://localhost:5001/egresados/EG013`
- Headers:
  ```
  Content-Type: application/json
  Authorization: Bearer {{token}}
  ```

### Respuesta esperada (200 OK)
```json
{
  "message": "Egresado eliminado lógicamente"
}
```

---

## 7. RESTAURAR EGRESADO

### Request
- Método: `PUT`
- URL: `http://localhost:5001/egresados/restaurar/EG013`
- Headers:
  ```
  Content-Type: application/json
  Authorization: Bearer {{token}}
  ```

### Respuesta esperada (200 OK)
```json
{
  "message": "Egresado restaurado exitosamente"
}
```

---

## 8. ENDPOINTS AUXILIARES

### Carreras Profesionales
- Método: `GET`
- URL: `http://localhost:5001/carreras`
- Headers: `Authorization: Bearer {{token}}`

### Estados Civiles
- Método: `GET`
- URL: `http://localhost:5001/estados-civiles`
- Headers: `Authorization: Bearer {{token}}`

### Actividades Económicas
- Método: `GET`
- URL: `http://localhost:5001/actividades-economicas`
- Headers: `Authorization: Bearer {{token}}`

### Empresas
- Método: `GET`
- URL: `http://localhost:5001/empresas`
- Headers: `Authorization: Bearer {{token}}`

### Certificaciones
- Método: `GET`
- URL: `http://localhost:5001/certificaciones`
- Headers: `Authorization: Bearer {{token}}`
