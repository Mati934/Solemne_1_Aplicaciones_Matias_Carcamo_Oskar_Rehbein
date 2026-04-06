# Solemne 1 - API Hora Actual

API REST con FastAPI que devuelve la hora actual en formato UTC-4 desde el servidor NTP del SHOA (`ntp.shoa.cl`).

**Integrantes:** Matias Carcamo, Oskar Rehbein

## Ejecucion local

```bash
uv sync
uv run uvicorn hora.main:app --port 8000
```

## Ejecucion con Docker

```bash
docker build -t solemne-01 .
docker run -p 8000:8000 solemne-01
```

## Ejecucion imagen DockerHub

```bash
docker pull oskarrehbein/hora-actual-MC-OR:master
docker run -p 8000:8000 oskarrehbein/hora-actual-MC-OR:master
```

## Probar el endpoint

Con curl:
```bash
curl -s http://localhost:8000/time
```

En el navegador: [http://localhost:8000/time](http://localhost:8000/time)

Respuesta esperada:
```json
{"datetime": "2026-04-04 15:30:45"}
```
