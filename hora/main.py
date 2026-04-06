from fastapi import FastAPI
from starlette.responses import JSONResponse

from hora.time_service import get_current_time

app = FastAPI()


@app.get("/time")
def read_time():
    """Retorna la hora actual en UTC-4 como JSON.

    Returns:
        dict: {"datetime": "YYYY-MM-DD HH:MM:SS"}

    Raises:
        ntplib.NTPException: Si el servidor NTP no responde.
        socket.gaierror: Si no se puede resolver el hostname.
    """
    try:
        now = get_current_time()
        return {"datetime": now.strftime("%Y-%m-%d %H:%M:%S")}
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"error": "Unable to fetch time from NTP server"},
        )
