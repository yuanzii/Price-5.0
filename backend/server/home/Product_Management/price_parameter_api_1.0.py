from home import home
from flask import request, jsonify
import pandas as pd
import numpy as np

@home.route('/yuanzii_api/price_parameter_api', methods=["POST","GET","PUT"])
def price_parameter_api():
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
            return jsonify("")

        if request.method == 'POST':
            post_data = request.json
            variable = post_data.get("type")
            print("POST")
            print(variable)

            A1001 = pd.read_sql("SELECT * from product_info ", con)
            A1002 = pd.read_sql("SELECT * from product_description ", con)  # product weight
            A1003 = pd.read_sql("SELECT * from product_name ", con)
            A1004 = pd.read_sql("SELECT * from duty_price ", con)

            kt_price = pd.read_sql("SELECT * from kt_price ", con)
            # 为了获取当天最高价钱，倒序排列价钱
            kt_price = kt_price.loc[(kt_price.lei == 31)].sort_values(by='price', ascending=False)
            A1005 = kt_price.loc[kt_price.groupby(["id"])["datetime"].idxmax()]

            Join1 = pd.merge(pd.merge(A1001, A1002, how='left', on='id'), A1003, how='left', on='id', left_index=False,
                             right_index=False, sort=True)
            Join2 = pd.merge(Join1, A1004, how='left', left_on='duty', right_on='id', left_index=False,
                             right_index=False, sort=True).drop(
                columns=['id_y', 'idname_y', 'mm_name_y', 'd_name_y', 'duty'])
            Join2.rename(columns={'id_x': 'id', 'idname_x': 'idname', 'mm_name_x': 'mm_name', 'd_name_x': 'd_name',
                                  'price': 'duty_price'}, inplace=True)
            Join3 = pd.merge(Join2, A1005, how='left', on='id', left_index=False,
                             right_index=False, sort=True)

            if variable == None:
                B2002 = Join3.to_json(orient="records")
                print(B2002)
                return B2002

            else:  # variable == type of product
                A1001 = pd.read_sql("SELECT id FROM product_info WHERE type = '" + str(variable) + "'", con)
                Join1 = pd.merge(Join3, A1001, on='id', left_index=False, right_index=False, sort=True)
                B2002 = Join1.to_json(orient="records")
                return B2002

        if request.method == 'PUT':
            post_data = request.json

            variable = post_data.get("variable")

            type = post_data.get("type")  # id of product type
            id = post_data.get("id")  # id of product
            datetime = post_data.get("datetime")  # datetime
            duty_ratio = post_data.get("duty_ratio")  # duty_ratio
            percentage = post_data.get("percentage")  # percentage

            print("PUT")

            # Create Table product_info
            sql_create = """CREATE TABLE IF NOT EXISTS kt_price(  serial_id  SERIAL PRIMARY KEY,
                                                                  id  INT ,
                                                                  datetime        TIMESTAMP   ,
                                                                  duty_ratio            FLOAT      ,
                                                                  percentage        FLOAT       ,
                                                                  lei      INT    ,
                                                                  price      NUMERIC(15, 6)       
                                                                                  );"""
            cur.execute(sql_create)
            con.commit()

            if variable == -1:

                # Insert Many Rows：DataTable kt_price duty_ratio and percentage

                A1001 = pd.read_sql("SELECT id FROM product_info WHERE type = '" + str(type) + "'", con)
                A1001['datetime'] = datetime
                A1001['duty_ratio'] = duty_ratio
                A1001['percentage'] = percentage
                A1001['lei'] = 31
                A1001.to_sql(name='kt_price', con=engine_price, if_exists='append', index=False)

                return jsonify("Insert Many Rows： duty_ratio and percentage")

            else:  # variable == -2:

                # Insert id/datetime/duty_ratio/percentage/lei to kt_price datatable
                sql_insert = "INSERT INTO kt_price(id, datetime, duty_ratio, percentage, lei) Values" \
                             "('" + str(id) + "', '" + str(datetime) + "', '" + str(duty_ratio) + "'" \
                             ", '" + str(percentage) + "', '" + str(31) + "')"
                cur.execute(sql_insert)
                con.commit()

                return jsonify("Insert Only One Row To kt_price：duty_ratio and percentage")

    except Exception:
        print("Error:出错啦！！！")
        return jsonify("Error:出错啦！！！")

    finally:

        # calculate kt price to insert into kt_price datatable

        A1001 = pd.read_sql("SELECT * from product_info ", con)
        A1002 = pd.read_sql("SELECT * from product_description ", con)  # product weight
        A1003 = pd.read_sql("SELECT * from duty_price ", con)
        A1004 = pd.read_sql("SELECT * from kt_price ", con)
        A1005 = pd.read_sql("SELECT * from price ", con)
        Join1 = pd.merge(pd.merge(A1001, A1002, how='left', on='id'), A1003, how='left', left_on='duty',
                         right_on='id', left_index=False, right_index=False, sort=True).drop(
            columns=['id_y', 'status', 'idname', 'mm_name', 'd_name'])
        Join1.rename(columns={'id_x': 'id', 'price': 'duty_price'}, inplace=True)
        Join2 = pd.merge(pd.merge(Join1, A1004, how='left', on='id'), A1005, how='left', on='id',
                         left_index=False, right_index=False, sort=True)
        Join2['price'] = ((Join2['weight'] * Join2['duty_price'] * Join2['duty_ratio']) + Join2[
            's_price']) * Join2['percentage']
        Join2 = Join2.round(6)
        Join2.to_sql('temp_table', con=engine_price, if_exists='replace')
        sql_update = """
                            UPDATE kt_price AS a SET price = b.price FROM temp_table AS b WHERE a.serial_id = b.serial_id
                        """
        cur.execute(sql_update)
        con.commit()

        # insert kt price into price data table

        kt_price = pd.read_sql("SELECT * from kt_price ", con)
        # 为了获取当天最高价钱，倒序排列价钱
        kt_price = kt_price.loc[(kt_price.lei == 31)].sort_values(by='price', ascending=False)
        # 通过 group by id 然后选择最大的日期 来获取最后的 KT 价
        kt_price = kt_price.loc[kt_price.groupby(["id"])["datetime"].idxmax()]
        kt_price = kt_price.round(6)
        # 测试是否唯一
        # duplicate = kt_price.duplicated('id')
        # print(duplicate)
        price = pd.read_sql("SELECT * from price ", con)
        price['kt_price'] = price['kt_price'].astype(float)
        # 通过两张表对比 id 和 价钱 // update最新价钱 和 新数据
        Join_price = (kt_price.merge(price, left_on=['id', 'price'], right_on=['id', 'kt_price'], how='left',
                                     indicator=True).query('_merge == "left_only"'))
        Join_price.to_sql('temp_table', con=engine_price, if_exists='replace')
        sql_update = """
                            UPDATE price AS a
                            SET kt_price = b.price
                            FROM temp_table AS b
                            WHERE a.id = b.id
                        """
        cur.execute(sql_update)
        con.commit()

        cur.close()
        con.close()
        print("close")