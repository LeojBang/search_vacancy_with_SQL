from unittest.mock import patch

import pytest
import requests

from src.hh_api import HeadHunterAPI


@patch("requests.get")
def test_http_error_hh_api(mock_request):
    mock_request.return_value.status_code = 400

    with pytest.raises(requests.HTTPError):
        hh = HeadHunterAPI()
        hh._load_vacancies()


@patch("requests.get")
def test_hh_api(mock_request, vacancy):
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = {"items": vacancy}

    hh = HeadHunterAPI()
    hh._load_vacancies()

    assert hh.vacancies[0]["address"] == vacancy[0]["address"]
    assert len(hh.vacancies) == 40
    for vacancy in hh.vacancies:
        assert vacancy["salary"] is not None
        assert vacancy["address"] is not None
