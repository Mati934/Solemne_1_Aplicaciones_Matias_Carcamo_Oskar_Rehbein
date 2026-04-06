from datetime import datetime
from unittest.mock import patch

from hora.time_service import TZ, get_current_time


def test_obtiene_datetime_en_utc():
    """Verifica que get_current_time retorna datetime en la zona horaria configurada."""
    mock_response = type("MockResponse", (), {"tx_time": 1712222400})()

    with patch("ntplib.NTPClient") as mock_client_class:
        mock_client = mock_client_class.return_value
        mock_client.request.return_value = mock_response

        result = get_current_time()

        assert isinstance(result, datetime)
        assert result.tzinfo == TZ
        mock_client.request.assert_called_once_with("ntp.shoa.cl")
