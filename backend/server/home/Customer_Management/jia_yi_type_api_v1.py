from home import home
from flask import request, jsonify
import pandas as pd
import numpy as np

@home.route('/yuanzii_api/jia_yi_type_api_v1', methods=["POST","GET","PUT"])
def jia_yi_type_api_v1():
    import db.psql_psycopg2 as con
    import importlib
    importlib.reload(con)
    from db.psql_psycopg2 import con

    try:
        # if request.method == 'GET':
        #     print("GET")
        #
        #     product_list = pd.read_sql("SELECT * from jia_yi_type ", con)
        #
        #     B2002 = product_list.to_json(orient="records")
        #     # con.close()
        #     print(B2002)
        #     return B2002

        if request.method == 'POST':
            post_data = request.json

            # Post Level and id(c_id) To Get Jia Yi Type step by step
            id = post_data.get("id")

            # Post category_name/c_id/level To SQL
            name = post_data.get("name")
            level = post_data.get("level")
            c_id = post_data.get("c_id")
            print("POST")

            if name == None:

                cur = con.cursor()
                sql_create = """CREATE TABLE IF NOT EXISTS jia_yi_type(id  SERIAL PRIMARY KEY,
                                        name           TEXT      NOT NULL,
                                        c_id            INT       NOT NULL,
                                        level        INT       NOT NULL
                                        );"""
                cur.execute(sql_create)
                con.commit()

                # Get Jia Yi Type step by step
                A1001 = pd.read_sql("SELECT * from jia_yi_type where level = '" + str(level) + "' \
                and c_id = '" + str(id) + "' order by id asc ", con)

                A1002 = A1001.to_json(orient="records")
                con.close()
                return A1002

            else:

                # Insert category_name/c_id/level To SQL
                cur = con.cursor()
                sql_insert = "INSERT INTO jia_yi_type (name, c_id,level) Values" \
                             "('" + name + "', '" + str(c_id) + "','" + str(level) + "')"
                cur.execute(sql_insert)
                # print(sql_insert)
                con.commit()
                # con.close()

                return jsonify("")

        if request.method == 'PUT':

            # PUT variable
            # IF variable == 1 / Delete row
            # IF variable == 0 / Delete row
            # IF variable == None / 檢查要刪除數據裏有沒有子數據
            put_data = request.json

            variable = put_data.get("variable")
            print(variable)

            # Put category_name/c_id/level To SQL
            id = put_data.get("id")
            name = put_data.get("name")
            c_id = put_data.get("c_id")
            level = put_data.get("level")

            print("PUT")

            if variable == 1:

                cur = con.cursor()
                sql_delete = "DELETE FROM jia_yi_type WHERE id = '" + str(id) + "'"
                cur.execute(sql_delete)
                print(sql_delete)

                con.commit()
                # con.close()

                return jsonify("")

            elif variable == 0:

                # 檢查要刪除數據裏有沒有子數據
                A1001 = pd.read_sql("SELECT * from jia_yi_type where \
                                c_id = '" + str(id) + "' order by id asc ", con)
                A1002 = A1001.to_json(orient="records")
                print(A1002)
                # con.close()

                return A1002

            else:
                # UPDATE：Edit category_name To SQL
                cur = con.cursor()
                sql_update = """UPDATE jia_yi_type SET name = %s WHERE id = %s"""
                val = (name, id)
                cur.execute(sql_update, val)

                con.commit()
                # con.close()

                return jsonify("")

    except Exception:
        print("Error:出错啦！！！")
        return jsonify("")

