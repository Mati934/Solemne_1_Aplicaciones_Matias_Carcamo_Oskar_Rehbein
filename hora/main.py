from fastapi import FastAPI

from hora.time_service import get_current_time

app = FastAPI()


@app.get("/")
def read_time():
    """Retorna la hora actual en GMT como JSON.

    Returns:
        dict: {"datetime": "YYYY-MM-DD HH:MM:SS"}

    Raises:
        ntplib.NTPException: Si el servidor NTP no responde.
        socket.gaierror: Si no se puede resolver el hostname.
    """
    now = get_current_time()
    return {"datetime": now.strftime("%Y-%m-%d %H:%M:%S")}
