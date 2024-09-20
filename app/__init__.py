from flask import Flask, jsonify, request
from psycopg2.extras import RealDictCursor
from flask_parameter_validation import ValidateParameters, Json, Query
from database import get_db_connection

app = Flask(__name__)
app.config.from_object('config.DevConfig')

@app.route("/rates", methods=['GET'])
@ValidateParameters()
def rates(
    date_from: str = Query(pattern=r"^\d{4}-\d{2}-\d{2}$"),
    date_to: str = Query(pattern=r"^\d{4}-\d{2}-\d{2}$"),
    origin: str = Query(),
    destination: str = Query(),
):
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