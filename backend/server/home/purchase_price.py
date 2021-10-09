from home import home
from flask import request, jsonify
import pandas as pd
import numpy as np

@home.route('/yuanzii_api/purchase_s_price_api', methods=["GET","POST","PUT"])
def purchase_s_price_api():
    import db.psql_psycopg2 as con
    import db.psql_sqlalchemy as con_2
    import importlib
    importlib.reload(con)
    importlib.reload(con_2)
    from db.psql_psycopg2 import con
    from db.psql_sqlalchemy import engine_price

    try:

        cur = con.cursor()

        if request.method == 'GET':
            print("GET")

            A1001 = pd.read_sql("SELECT * from product_name ", con)
            A1002 = pd.read_sql("SELECT * from price ", con)
            A1003 = pd.read_sql("SELECT * from product_description ", con)
            Join1 = pd.merge(pd.merge(A1001, A1002, on='id'), A1003, on='id', how='left', left_index=False,
                             right_index=False, sort=True)
            B2002 = Join1.to_json(orient="records")
            return B2002

            # A1001 = pd.read_sql("SELECT * from product_name ", con)
            # A1002 = pd.read_sql("SELECT * from product_description ", con)  # product weight
            # A1003 = pd.read_sql("SELECT * from product_info ", con)
            # A1004 = pd.read_sql("SELECT * from duty_price ", con)
            # A1005 = pd.read_sql("SELECT * from kt_price ", con)
            # A1006 = pd.read_sql("SELECT * from price ", con)
            #
            # Join1 = pd.merge(A1001, A1002, how='left', on='id', left_index=False,
            #                  right_index=False, sort=True)
            # Join2 = pd.merge(Join1, A1003, how='left', on='id', left_index=False,
            #                  right_index=False, sort=True).drop(columns=['type', 'status'])
            # Join3 = pd.merge(Join2, A1004, how='left', left_on='duty', right_on='id', left_index=False,
            #                  right_index=False, sort=True).drop(
            #                  columns=['id_y', 'idname_y', 'mm_name_y', 'd_name_y', 'duty'])
            # Join3.rename(columns={'id_x': 'id', 'idname_x': 'idname', 'mm_name_x': 'mm_name', 'd_name_x': 'd_name',
            #                       'price': 'duty_price'}, inplace=True)
            # Join4 = pd.merge(Join3, A1005, how='left', left_on='id', right_on='id', left_index=False,
            #                  right_index=False, sort=True).drop(columns=['price'])
            # Join5 = pd.merge(Join4, A1006, how='left', left_on='id', right_on='id', left_index=False,
            #                  right_index=False, sort=True)
            # Join5['kt_price'] = ((Join5['weight']*Join5['duty_price']*Join5['duty_ratio'])+Join5['s_price'])\
            #                      *Join5['percentage']

            # price = pd.read_sql("SELECT * from price ", con)
            # price['kt_price'] = price['kt_price'].astype(float)
            # # # 通过两张表对比 id 和 价钱 update 最新价钱
            # Join = (Join5.merge(price, on=['id', 'kt_price'], how='left', indicator=True).query('_merge == "left_only"')
            #         ).drop(columns=['idname', 'mm_name', 'd_name', 'weight', 'duty_price', 'duty_ratio', 'percentage',
            #                         's_price_y','o_price_y', '_merge'])
            # Join.rename(columns={'s_price_x': 's_price', 'o_price_x': 'o_price'}, inplace=True)
            # Join.to_sql(name='price_temp', con=engine_price, if_exists='replace', index=False)
            # cur.execute('delete from price where id in (select id from price_temp)')
            # # 删除临时表
            # con.commit()
            # Join.to_sql(name='price', con=engine_price, if_exists='append', index=False)

            # B2002 = Join5.to_json(orient="records")
            # return B2002

        if request.method == 'POST':
            post_data = request.json
            type = post_data.get("type")
            print("POST")

            A1001 = pd.read_sql("SELECT * from product_name ", con)
            A1002 = pd.read_sql("SELECT * from price ", con)
            A1003 = pd.read_sql("SELECT id FROM product_info WHERE type = '" + str(type) + "'", con)
            A1004 = pd.read_sql("SELECT * from product_description ", con)
            Join1 = pd.merge(pd.merge(A1001, A1002, on='id'), A1003, on='id', left_index=False,
                             right_index=False, sort=True)
            Join2 = pd.merge(Join1, A1004, on='id', how='left', left_index=False,
                             right_index=False, sort=True)
            B2002 = Join2.to_json(orient="records")
            return B2002

    except Exception:
        print("Error:出错啦！！！")
        return jsonify("")

    finally:
        cur.close()
        con.close()
        print("close")