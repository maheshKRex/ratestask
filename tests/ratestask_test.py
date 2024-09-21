
import pytest
from flask import Flask, jsonify, request
from app import app 

@pytest.mark.parametrize(
    "date_from, date_to, origin, destination, expected_status_code, expected_response",
    [
        ("2016-01-01", "2016-01-10", "CNSGH", "north_europe_main", 200, [{"average_price":"1077","day":"2016-01-01"},{"average_price":"1077","day":"2016-01-02"},{"average_price":"1116","day":"2016-01-05"},{"average_price":"1117","day":"2016-01-06"},{"average_price":"1110","day":"2016-01-07"},{"average_price":"1094","day":"2016-01-08"},{"average_price":"1094","day":"2016-01-09"},{"average_price":"1094","day":"2016-01-10"}]),
        ("2016-01-01", "2016-01-10", "CNSGH", "", 400, [{"average_price":"1077","day":"2016-01-01"},{"average_price":"1077","day":"2016-01-02"},{"average_price":"1116","day":"2016-01-05"},{"average_price":"1117","day":"2016-01-06"},{"average_price":"1110","day":"2016-01-07"},{"average_price":"1094","day":"2016-01-08"},{"average_price":"1094","day":"2016-01-09"},{"average_price":"1094","day":"2016-01-10"}])
    ]
)
def test_rates(
    date_from,
    date_to,
    origin,
    destination,
    expected_status_code,
    expected_response,
):
    client = app.test_client()
    response = client.get(
        "/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main"
    )

    assert response.status_code == expected_status_code
    assert response.json == expected_response