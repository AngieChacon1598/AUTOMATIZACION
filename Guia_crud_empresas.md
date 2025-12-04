# GUÍA CRUD EMPRESAS

### CAMPOS:
- `id_empresa` (SERIAL, PK) - ID único de la empresa
- `nombre` (VARCHAR(100), UNIQUE, NOT NULL) - Nombre de la empresa
- `ruc` (VARCHAR(11), UNIQUE, NOT NULL) - RUC de la empresa
- `direccion` (VARCHAR(200)) - Dirección de la empresa
- `telefono` (VARCHAR(15)) - Teléfono de contacto
- `correo` (VARCHAR(120)) - Correo electrónico
- `estado` (CHAR(1), DEFAULT 'A') - Estado del registro (A/I)

## 1. LISTAR EMPRESAS

### Request
- Método: `GET`
- URL: `http://localhost:5001/empresas`

### Ejemplo de Request:
```
GET /empresas?estado=A&nombre=Tech&page=1&per_page=5
```

## 2. OBTENER EMPRESA ESPECÍFICA

### Request
- Método: `GET`
- URL: `http://localhost:5001/empresas/1`
- Headers:
  ```
  Content-Type: application/json
  Authorization: Bearer {{token}}
  ```

### Respuesta esperada:
```json
{
  "id_empresa": 1,
  "nombre": "TechSolutions Perú S.A.C.",
  "ruc": "20567890123",
  "direccion": "Av. Principal 123",
  "telefono": "987654321",
  "correo": "contacto@techsolutions.pe",
  "estado": "A"
}
```

---

## 3. CREAR EMPRESA

### Request
- Método: `POST`
- URL: `http://localhost:5001/empresas`
- Headers:
  ```
  Content-Type: application/json
  Authorization: Bearer {{token}}
  ```
- Body (raw JSON):
  ```json
  {
    "nombre": "TechSolutions Perú S.A.C.",
    "ruc": "20567890123",
    "direccion": "Av. Javier Prado Este 4200, La Molina",
    "telefono": "012345678",
    "correo": "contacto@techsolutions.pe",
    "estado": "A"
  }
  ```

## 4. ACTUALIZAR EMPRESA

### Request
- Método: `PUT`
- URL: `http://localhost:5001/empresas/1`
- Headers:
  ```
  Content-Type: application/json
  Authorization: Bearer {{token}}
  ```
- Body (raw JSON) - Solo campos a actualizar:
  ```json
  {
    "nombre": "TechSolutions Actualizada S.A.C.",
    "direccion": "Nueva Dirección 789",
    "telefono": "999888777"
  }
  ```

## 5. ELIMINAR EMPRESA LÓGICAMENTE

### Request
- Método: `DELETE`
- URL: `http://localhost:5001/empresas/1`
- Headers:
  ```
  Content-Type: application/json
  Authorization: Bearer {{token}}
  ```

### Respuesta esperada (200 OK):
```json
{
  "message": "Empresa eliminada exitosamente"
}
```

## 6. RESTAURAR EMPRESA

### Request
- Método: `PUT`
- URL: `http://localhost:5001/empresas/restaurar/1`
- Headers:
  ```
  Content-Type: application/json
  Authorization: Bearer {{token}}
  ```

### Respuesta esperada (200 OK):
```json
{
  "message": "Empresa restaurada exitosamente"
}
```
