# GUÍA CRUD DETALLE EGRESADO

## INFORMACIÓN GENERAL

**URL Base:** `http://localhost:5001` (o la URL de tu backend)

**Prefijo de rutas:** `/detalle-egresados`

**Headers requeridos:**
```
Content-Type: application/json
```

---

## ESTRUCTURA DE DATOS

### Objeto DetalleEgresado

```typescript
interface DetalleEgresado {
  id_detalle: number;              // ID único (generado automáticamente)
  codigo_egresado: string;         // REQUERIDO - Código del egresado (FK)
  fecha_egreso: string | null;     // Fecha en formato ISO (YYYY-MM-DD)
  empresa_actual: string | null;   // Nombre de la empresa actual
  cargo_actual: string | null;     // Cargo actual
  pais_residencia: string | null;  // País de residencia
  ciudad_residencia: string | null;// Ciudad de residencia
  fecha_incorporacion: string | null; // Fecha de incorporación (YYYY-MM-DD)
  area_trabajo: string | null;     // Área de trabajo
  sueldo_actual: number | null;    // Sueldo actual (decimal)
  estado: string;                  // 'A' (Activo) o 'I' (Inactivo) - default: 'A'
  egresado_nombre?: string;        // Nombre completo del egresado (solo en respuesta)
}
```

---

## ENDPOINTS

### 1. LISTAR DETALLES DE EGRESADOS

**Request:**
- Método: `GET`
- URL: `http://localhost:5001/detalle-egresados`
- Headers:
  ```
  Content-Type: application/json
  ```

**Query Parameters (todos opcionales):**
- `estado`: `A` (activos) o `I` (inactivos)
- `codigo_egresado`: `EG001` - Filtrar por código de egresado específico
- `page`: `1` - Número de página (default: 1)
- `per_page`: `10` - Elementos por página (default: 10)

**Ejemplo de Request:**
```
GET /detalle-egresados?estado=A&codigo_egresado=EG001&page=1&per_page=10
```

**Respuesta exitosa (200):**
```json
{
  "detalles": [
    {
      "id_detalle": 1,
      "codigo_egresado": "EG001",
      "fecha_egreso": "2023-12-15",
      "empresa_actual": "TechSolutions S.A.",
      "cargo_actual": "Desarrollador Senior",
      "pais_residencia": "Perú",
      "ciudad_residencia": "Lima",
      "fecha_incorporacion": "2024-01-10",
      "area_trabajo": "Tecnología",
      "sueldo_actual": 5000.00,
      "estado": "A",
      "egresado_nombre": "Juan Pérez García"
    }
  ],
  "total": 25,
  "page": 1,
  "per_page": 10,
  "pages": 3
}
```

---

### 2. OBTENER DETALLE ESPECÍFICO

**Request:**
- Método: `GET`
- URL: `http://localhost:5001/detalle-egresados/{id_detalle}`
- Headers:
  ```
  Content-Type: application/json
  ```

**Ejemplo de Request:**
```
GET /detalle-egresados/1
```

**Respuesta exitosa (200):**
```json
{
  "id_detalle": 1,
  "codigo_egresado": "EG001",
  "fecha_egreso": "2023-12-15",
  "empresa_actual": "TechSolutions S.A.",
  "cargo_actual": "Desarrollador Senior",
  "pais_residencia": "Perú",
  "ciudad_residencia": "Lima",
  "fecha_incorporacion": "2024-01-10",
  "area_trabajo": "Tecnología",
  "sueldo_actual": 5000.00,
  "estado": "A",
  "egresado_nombre": "Juan Pérez García"
}
```

**Error (404):**
```json
{
  "message": "Detalle de egresado no encontrado"
}
```

---

### 3. CREAR NUEVO DETALLE DE EGRESADO

**Request:**
- Método: `POST`
- URL: `http://localhost:5001/detalle-egresados`
- Headers:
  ```
  Content-Type: application/json
  ```
- Body (raw JSON):

**Campos requeridos:**
- `codigo_egresado` (string) - DEBE existir en la tabla egresado

**Campos opcionales:**
- `fecha_egreso` (string) - Formato: "YYYY-MM-DD"
- `empresa_actual` (string)
- `cargo_actual` (string)
- `pais_residencia` (string)
- `ciudad_residencia` (string)
- `fecha_incorporacion` (string) - Formato: "YYYY-MM-DD"
- `area_trabajo` (string)
- `sueldo_actual` (number) - Decimal
- `estado` (string) - 'A' o 'I' (default: 'A')

**Ejemplo de Request:**
```json
{
  "codigo_egresado": "EG001",
  "fecha_egreso": "2023-12-15",
  "empresa_actual": "TechSolutions S.A.",
  "cargo_actual": "Desarrollador Senior",
  "pais_residencia": "Perú",
  "ciudad_residencia": "Lima",
  "fecha_incorporacion": "2024-01-10",
  "area_trabajo": "Tecnología",
  "sueldo_actual": 5000.00,
  "estado": "A"
}
```

**Ejemplo mínimo (solo campos requeridos):**
```json
{
  "codigo_egresado": "EG001"
}
```

**Respuesta exitosa (201):**
```json
{
  "id_detalle": 1,
  "codigo_egresado": "EG001",
  "fecha_egreso": "2023-12-15",
  "empresa_actual": "TechSolutions S.A.",
  "cargo_actual": "Desarrollador Senior",
  "pais_residencia": "Perú",
  "ciudad_residencia": "Lima",
  "fecha_incorporacion": "2024-01-10",
  "area_trabajo": "Tecnología",
  "sueldo_actual": 5000.00,
  "estado": "A",
  "egresado_nombre": "Juan Pérez García"
}
```

**Errores:**

**400 - Error de validación:**
```json
{
  "message": "Error de validación",
  "errors": {
    "codigo_egresado": ["Este campo es requerido"],
    "estado": ["Debe ser uno de: A, I"]
  }
}
```

**404 - Egresado no encontrado:**
```json
{
  "message": "Egresado no encontrado"
}
```

**500 - Error del servidor:**
```json
{
  "message": "Error al crear el detalle: [descripción del error]"
}
```

---

### 4. ACTUALIZAR DETALLE DE EGRESADO

**Request:**
- Método: `PUT`
- URL: `http://localhost:5001/detalle-egresados/{id_detalle}`
- Headers:
  ```
  Content-Type: application/json
  ```
- Body (raw JSON) - Solo incluir campos a actualizar:

**Ejemplo de Request:**
```json
{
  "cargo_actual": "Tech Lead",
  "sueldo_actual": 6500.00,
  "fecha_incorporacion": "2024-06-01"
}
```

**Nota:** Puedes enviar solo los campos que quieres actualizar, no es necesario enviar todos.

**Respuesta exitosa (200):**
```json
{
  "id_detalle": 1,
  "codigo_egresado": "EG001",
  "fecha_egreso": "2023-12-15",
  "empresa_actual": "TechSolutions S.A.",
  "cargo_actual": "Tech Lead",
  "pais_residencia": "Perú",
  "ciudad_residencia": "Lima",
  "fecha_incorporacion": "2024-06-01",
  "area_trabajo": "Tecnología",
  "sueldo_actual": 6500.00,
  "estado": "A",
  "egresado_nombre": "Juan Pérez García"
}
```

**Errores:**

**404 - Detalle no encontrado:**
```json
{
  "message": "Detalle de egresado no encontrado"
}
```

**400 - Error de validación:**
```json
{
  "message": "Error de validación",
  "errors": {
    "estado": ["Debe ser uno de: A, I"]
  }
}
```

**500 - Error del servidor:**
```json
{
  "message": "Error al actualizar el detalle: [descripción del error]"
}
```

---

### 5. ELIMINAR DETALLE (ELIMINACIÓN LÓGICA)

**Request:**
- Método: `DELETE`
- URL: `http://localhost:5001/detalle-egresados/{id_detalle}`
- Headers:
  ```
  Content-Type: application/json
  ```

**Ejemplo de Request:**
```
DELETE /detalle-egresados/1
```

**Respuesta exitosa (200):**
```json
{
  "message": "Detalle eliminado exitosamente"
}
```

**Error (404):**
```json
{
  "message": "Detalle de egresado no encontrado"
}
```

**Error (500):**
```json
{
  "message": "Error al eliminar el detalle: [descripción del error]"
}
```

**Nota:** Este endpoint cambia el estado a 'I' (Inactivo), pero no elimina físicamente el registro.

---

### 6. RESTAURAR DETALLE ELIMINADO

**Request:**
- Método: `PUT`
- URL: `http://localhost:5001/detalle-egresados/restaurar/{id_detalle}`
- Headers:
  ```
  Content-Type: application/json
  ```

**Ejemplo de Request:**
```
PUT /detalle-egresados/restaurar/1
```

**Respuesta exitosa (200):**
```json
{
  "message": "Detalle restaurado exitosamente"
}
```

**Error (404):**
```json
{
  "message": "Detalle de egresado no encontrado"
}
```

**Nota:** Este endpoint cambia el estado de 'I' (Inactivo) a 'A' (Activo).

---

### 7. ELIMINAR DETALLE FÍSICAMENTE

**Request:**
- Método: `DELETE`
- URL: `http://localhost:5001/detalle-egresados/fisico/{id_detalle}`
- Headers:
  ```
  Content-Type: application/json
  ```

**Ejemplo de Request:**
```
DELETE /detalle-egresados/fisico/1
```

**Respuesta exitosa (200):**
```json
{
  "message": "Detalle eliminado permanentemente"
}
```

**Error (404):**
```json
{
  "message": "Detalle de egresado no encontrado"
}
```

**⚠️ ADVERTENCIA:** Este endpoint elimina permanentemente el registro de la base de datos. Úsalo con precaución.

---

## VALIDACIONES IMPORTANTES

1. **codigo_egresado**: 
   - Es REQUERIDO al crear un detalle
   - DEBE existir en la tabla `egresado`
   - Tipo: string

2. **estado**: 
   - Solo acepta valores: `'A'` (Activo) o `'I'` (Inactivo)
   - Default: `'A'`

3. **fecha_egreso y fecha_incorporacion**: 
   - Formato: `YYYY-MM-DD` (ISO 8601)
   - Son opcionales

4. **sueldo_actual**: 
   - Tipo: number (decimal)
   - Opcional

---

## CÓDIGOS DE RESPUESTA HTTP

- **200 OK**: Operación exitosa (GET, PUT, DELETE)
- **201 Created**: Recurso creado exitosamente (POST)
- **400 Bad Request**: Error de validación en los datos enviados
- **404 Not Found**: Recurso no encontrado
- **500 Internal Server Error**: Error del servidor

---

## EJEMPLOS DE USO EN FRONTEND

### Ejemplo con JavaScript/TypeScript (fetch)

```typescript
const API_BASE = 'http://localhost:5001';

// Listar detalles
async function listarDetalles(filtros = {}) {
  const params = new URLSearchParams({
    estado: filtros.estado || 'A',
    page: filtros.page || '1',
    per_page: filtros.perPage || '10',
    ...(filtros.codigoEgresado && { codigo_egresado: filtros.codigoEgresado })
  });
  
  const response = await fetch(`${API_BASE}/detalle-egresados?${params}`);
  return await response.json();
}

// Crear detalle
async function crearDetalle(detalle: Partial<DetalleEgresado>) {
  const response = await fetch(`${API_BASE}/detalle-egresados`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(detalle)
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Error al crear detalle');
  }
  
  return await response.json();
}

// Actualizar detalle
async function actualizarDetalle(idDetalle: number, cambios: Partial<DetalleEgresado>) {
  const response = await fetch(`${API_BASE}/detalle-egresados/${idDetalle}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(cambios)
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Error al actualizar detalle');
  }
  
  return await response.json();
}

// Eliminar lógicamente
async function eliminarDetalle(idDetalle: number) {
  const response = await fetch(`${API_BASE}/detalle-egresados/${idDetalle}`, {
    method: 'DELETE'
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Error al eliminar detalle');
  }
  
  return await response.json();
}
```

### Ejemplo con Axios

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5001',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Listar detalles
export const listarDetalles = (params = {}) => 
  api.get('/detalle-egresados', { params });

// Obtener detalle específico
export const obtenerDetalle = (idDetalle: number) =>
  api.get(`/detalle-egresados/${idDetalle}`);

// Crear detalle
export const crearDetalle = (data: Partial<DetalleEgresado>) =>
  api.post('/detalle-egresados', data);

// Actualizar detalle
export const actualizarDetalle = (idDetalle: number, data: Partial<DetalleEgresado>) =>
  api.put(`/detalle-egresados/${idDetalle}`, data);

// Eliminar lógicamente
export const eliminarDetalle = (idDetalle: number) =>
  api.delete(`/detalle-egresados/${idDetalle}`);

// Restaurar
export const restaurarDetalle = (idDetalle: number) =>
  api.put(`/detalle-egresados/restaurar/${idDetalle}`);

// Eliminar físicamente
export const eliminarDetalleFisico = (idDetalle: number) =>
  api.delete(`/detalle-egresados/fisico/${idDetalle}`);
```

---

## NOTAS ADICIONALES

1. **Relación con Egresado**: El campo `codigo_egresado` es una clave foránea. Asegúrate de que el egresado exista antes de crear un detalle.

2. **Paginación**: El endpoint de listado siempre devuelve datos paginados. Usa `page` y `per_page` para navegar entre páginas.

3. **Filtros**: Puedes combinar filtros. Por ejemplo: `/detalle-egresados?estado=A&codigo_egresado=EG001&page=1`

4. **Formato de fechas**: Las fechas se envían y reciben en formato ISO 8601: `YYYY-MM-DD`

5. **Campos opcionales**: Todos los campos excepto `codigo_egresado` son opcionales al crear un detalle.


