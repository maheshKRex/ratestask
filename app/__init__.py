from flask import Flask, jsonify, request
from psycopg2.extras import RealDictCursor
from database import get_db_connection
from marshmallow import fields, Schema
from marshmallow.exceptions import ValidationError
import re
import datetime

app = Flask(__name__)
app.config.from_object('config.DevConfig')

def validate_date_format(value):
    try:
        datetime.datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        raise ValidationError("Invalid date format")

def validate_origin_destination(value):
    if not value:
        raise ValidationError("Origin or destination cannot be empty.")
    return value

class QueryParamSchema(Schema):
    date_from = fields.Str(required=True, validate=validate_date_format)
    date_to = fields.Str(required=True, validate=validate_date_format)
    origin = fields.Str(required=True, validate=validate_origin_destination)
    destination = fields.Str(required=True, validate=validate_origin_destination)

@app.route("/rates", methods=['GET'])
def rates():
    # validations of from, to dates (the date pattern and actual date values) and origin, destination strings
    schema = QueryParamSchema()
    try:
        query_params = schema.load(request.args)
    except ValidationError as err:
        response = jsonify({"errors": err.messages})
        response.status_code = 400
        return response
    
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        """
            WITH search_prices AS (
                SELECT p.*
                FROM prices p
                LEFT JOIN ports o_port ON p.orig_code = o_port.code
                LEFT JOIN ports d_port ON p.dest_code = d_port.code
                WHERE p.day BETWEEN %(date_from)s AND %(date_to)s
                AND (p.orig_code = %(origin)s OR o_port.parent_slug = %(origin)s)
                AND (p.dest_code = %(destination)s OR d_port.parent_slug = %(destination)s)
            ), average_prices AS (
                SELECT 
                    CASE
                        WHEN COUNT(*) < 3 THEN null
                        ELSE ROUND(AVG(price))
                    END AS average_price,
                    day
                FROM search_prices
                GROUP BY day
            )
            SELECT average_price, to_char(day, 'YYYY-MM-DD') AS day
            FROM average_prices
            ORDER BY day ASC;
        """,
        {
            'date_from': request.args.get("date_from"),
            'date_to': request.args.get("date_to"),
            'origin': request.args.get("origin"),
            'destination': request.args.get("destination")
        }
    )

    rates = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(rates)

if __name__ == "__main__":
    cli()