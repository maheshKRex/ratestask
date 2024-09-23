
import pytest
from flask import Flask, jsonify, request
from app import app 

@pytest.mark.parametrize(
    "date_from, date_to, origin, destination, expected_status_code, expected_response",
    [
        ("2016-01-01", "2016-01-10", "CNSGH", "north_europe_main", 200, [{"average_price":"1077","day":"2016-01-01"},{"average_price":"1077","day":"2016-01-02"},{"average_price":"1116","day":"2016-01-05"},{"average_price":"1117","day":"2016-01-06"},{"average_price":"1110","day":"2016-01-07"},{"average_price":"1094","day":"2016-01-08"},{"average_price":"1094","day":"2016-01-09"},{"average_price":"1094","day":"2016-01-10"}]),
        ("2016-01-01", "2016-01-104", "CNSGH", "north_europe_main", 400, {'errors': {'date_to': ['Invalid date format']}}),
        ("2016-01-012", "2016-01-10", "CNSGH", "north_europe_main", 400, {'errors': {'date_from': ['Invalid date format']}}),
        ("2016-01-51", "2016-01-10", "CNSGH", "north_europe_main", 400, {'errors': {'date_from': ['Invalid date format']}}),
        ("2016-01-01", "2016-01", "CNSGH", "north_europe_main", 400, {'errors': {'date_to': ['Invalid date format']}}),
        ("2016/01/01", "2016-01", "CNSGH", "north_europe_main", 400, {'errors': {'date_from': ['Invalid date format'], 'date_to': ['Invalid date format']}}),
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
        "/rates",
        query_string={
                "date_from": date_from,
                "date_to": date_to,
                "origin": origin,
                "destination": destination
            }
    )
    print("response", response)
    assert response.status_code == expected_status_code
    assert response.json == expected_response