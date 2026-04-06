from datetime import datetime, timedelta, timezone

import ntplib

NTP_SERVER = "ntp.shoa.cl"
TZ = timezone(timedelta(hours=-4))


def get_current_time() -> datetime:
    """Obtiene la hora actual en UTC-4 desde el servidor NTP del SHOA.

    Returns:
        datetime: Fecha y hora en UTC-4.

    Raises:
        ntplib.NTPException: Si el servidor NTP no responde.
        socket.gaierror: Si no se puede resolver el hostname.
    """
    client = ntplib.NTPClient()
    response = client.request(NTP_SERVER)
    return datetime.fromtimestamp(response.tx_time, tz=TZ)
