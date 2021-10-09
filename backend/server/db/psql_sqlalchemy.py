from sqlalchemy import create_engine

engine_price = create_engine('postgresql+psycopg2:'
                             '//postgres:yuan7142'
                             '@localhost:5432/price_4',
                             echo=False
                             )