import psycopg2

con = psycopg2.connect(
        host="127.0.0.1",
        database="price_5",
        user="postgres",
        password="yuan7142",
        port=5432
    )