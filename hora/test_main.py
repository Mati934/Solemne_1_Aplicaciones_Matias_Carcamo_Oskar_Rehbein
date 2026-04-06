from datetime import datetime
from unittest.mock import patch

from fastapi.testclient import TestClient

from hora.main import app
from hora.time_service import TZ

client = TestClient(app)


def test_endpoint_retorna_json_con_datetime_formato_correcto():
    """Verifica que GET /time retorna JSON válido con datetime en formato YYYY-MM-DD HH:MM:SS."""
    mock_time = datetime(2026, 4, 4, 15, 30, 45, tzinfo=TZ)

    with patch("hora.main.get_current_time", return_value=mock_time):
        response = client.get("/time")

        assert response.status_code == 200
        assert "datetime" in response.json()
        assert response.json()["datetime"] == "2026-04-04 15:30:45"


def test_hora_retornada_es_cercana_a_hora_actual():
    """Verifica que la hora retornada es cercana a la hora actual del sistema."""
    response = client.get("/time")

    assert response.status_code == 200
    hora_respuesta = datetime.strptime(response.json()["datetime"], "%Y-%m-%d %H:%M:%S")
    hora_actual = datetime.now(TZ).replace(tzinfo=None)

    # Permite diferencia de ±5 segundos
    diferencia = abs((hora_respuesta - hora_actual).total_seconds())
    assert diferencia <= 5, f"Diferencia de {diferencia} segundos es mayor a 5"
