from datetime import datetime, timezone

import ntplib

NTP_SERVER = "ntp.shoa.cl"


def get_current_time() -> datetime:
    """Obtiene la hora actual en GMT desde el servidor NTP del SHOA.

    Returns:
        datetime: Fecha y hora en UTC/GMT.

    Raises:
        ntplib.NTPException: Si el servidor NTP no responde.
        socket.gaierror: Si no se puede resolver el hostname.
    """
    client = ntplib.NTPClient()
    response = client.request(NTP_SERVER)
    return datetime.fromtimestamp(response.tx_time, tz=timezone.utc)
