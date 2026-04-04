# Explicación del código

## Estructura del proyecto

```
solemne_1/
├── hora/
│   ├── main.py          # FastAPI app con endpoint
│   └── time_service.py  # Obtiene hora GMT desde servidor NTP
├── pyproject.toml       # Configuración del proyecto (uv)
└── .venv/               # Entorno virtual
```

## time_service.py

Obtiene la hora actual en GMT desde el servidor NTP del SHOA. Sin lógica de API, solo obtiene la hora.

### Función: `get_current_time()`

**Goal**: Consultar un servidor NTP y retornar la hora actual en GMT.

**Parámetros**: Ninguno.

**Return**: `datetime` — Objeto con fecha y hora en UTC/GMT.

**Excepciones**:
- `ntplib.NTPException` — El servidor NTP no responde correctamente
- `socket.gaierror` — No se puede resolver el hostname del servidor

### Línea por línea

```python
from datetime import datetime, timezone
```
- `datetime` — clase para representar fecha y hora
- `timezone` — clase para manejar zonas horarias (usamos `timezone.utc` para GMT)

```python
import ntplib
```
- Librería para hacer consultas a servidores NTP

```python
NTP_SERVER = "ntp.shoa.cl"
```
- Constante con el hostname del servidor NTP del SHOA (Servicio Hidrográfico y Oceanográfico de la Armada)

```python
client = ntplib.NTPClient()
```
- Crea un cliente NTP. Sin parámetros, solo es el objeto que hace la consulta.

```python
response = client.request(NTP_SERVER)
```
- `request(host)` — envía una solicitud al servidor NTP
  - `host` *(str)* — hostname del servidor
  - Retorna un objeto `NTPStats` con la respuesta

```python
response.tx_time
```
- Atributo de `NTPStats` que contiene el **timestamp Unix** (segundos desde 1970-01-01)

```python
datetime.fromtimestamp(response.tx_time, tz=timezone.utc)
```
- `fromtimestamp(timestamp, tz)` — convierte un timestamp Unix a un objeto `datetime`
  - `timestamp` *(float)* — el timestamp de `tx_time`
  - `tz` *(tzinfo)* — zona horaria. Con `timezone.utc` obtenemos GMT

---

## main.py

Define la API FastAPI con un endpoint que retorna la hora en formato JSON.

### Función: `read_time()`

**Goal**: Endpoint HTTP que retorna la hora actual en formato JSON.

**Parámetros**: Ninguno.

**Return**: `dict` — `{"datetime": "YYYY-MM-DD HH:MM:SS"}`

**Excepciones**: Hereda las de `get_current_time()` (ver arriba).

### Línea por línea

```python
from fastapi import FastAPI
```
- Importa FastAPI, framework web para crear APIs

```python
from hora.time_service import get_current_time
```
- Importa la función que obtiene la hora desde `time_service.py`

```python
app = FastAPI()
```
- Crea la aplicación FastAPI. Sin parámetros obligatorios.

```python
@app.get("/")
```
- Decorador que registra la función como handler del endpoint `GET /`
- **Sin `/`**: accederías en `http://localhost:8000/`
- **Con `/time`**: accederías en `http://localhost:8000/time`
- Siempre requiere un string con la ruta

```python
now = get_current_time()
```
- Llama a `get_current_time()` y almacena el resultado en `now`

```python
now.strftime("%Y-%m-%d %H:%M:%S")
```
- Formatea el `datetime` a string. El patrón:
  - `%Y` — año con 4 dígitos
  - `%m` — mes con 2 dígitos
  - `%d` — día con 2 dígitos
  - `%H` — hora en formato 24h
  - `%M` — minutos
  - `%S` — segundos

```python
return {"datetime": now.strftime("%Y-%m-%d %H:%M:%S")}
```
- Retorna un diccionario que FastAPI automáticamente convierte a JSON

---

## Cómo correr el código

```bash
uv run uvicorn hora.main:app --port 8000
```

Desglosado:

| Parte | Qué es | De dónde viene |
|-------|--------|----------------|
| `uv run` | Ejecuta comandos dentro del proyecto uv | Comando de `uv` (gestor de paquetes) |
| `uvicorn` | Servidor web que corre FastAPI | Dependency en `pyproject.toml` |
| `hora.main` | Módulo: carpeta `hora` + archivo `main.py` | Tu proyecto |
| `:app` | Nombre variable FastAPI en `main.py` | La línea `app = FastAPI()` |
| `--port 8000` | Puerto del servidor | Parámetro de uvicorn |

### Acceder a la API

1. El servidor levanta en `http://localhost:8000`
2. El endpoint es `/` (definido en el decorador)
3. **URL completa**: `http://localhost:8000/`

Desde la terminal:
```bash
curl http://localhost:8000/
```

Por navegador: simplemente abre `http://localhost:8000/` en Chrome/Firefox.

---

## Documentación oficial

| Librería | URL |
|---|---|
| `ntplib` | https://pypi.org/project/ntplib |
| `datetime` (stdlib) | https://docs.python.org/3/library/datetime.html |
| `FastAPI` | https://fastapi.tiangolo.com |
| `uvicorn` | https://www.uvicorn.org |
