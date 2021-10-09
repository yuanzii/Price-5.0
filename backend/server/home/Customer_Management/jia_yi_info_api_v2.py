from home import home
from flask import request, jsonify
import pandas as pd
import numpy as np

@home.route('/yuanzii_api/jia_yi_info_api_v2', methods=["POST","GET","PUT"])
def jia_yi_info_api_v2():
    import db.psql_psycopg2 as con
    import importlib
    importlib.reload(con)
    from db.psql_psycopg2 import con

    try:
        if request.method == 'GET':
            print("GET")
            # 有BUG
            A1001 = pd.read_sql("SELECT * from jia_yi_name ", con)
            A1002 = pd.read_sql("SELECT * from jia_yi_info_1 ", con)
            A1003 = pd.read_sql("SELECT * from locations ", con)
            A1004 = pd.read_sql("SELECT * from jia_yi_type ", con)

            Join1 = pd.merge(A1001, A1002, how='left', on='id', left_index=False,
                             right_index=False, sort=True)

            Join2 = pd.merge(Join1, A1003, how='left', left_on='township', right_on='id', left_index=False,
                             right_index=False, sort=True).drop(columns='id_y')
            Join2.rename(
                columns={'id_x': 'id', 'name': 'township_name', 'c_id': 'township_c_id', 'level': 'township_level'},
                inplace=True)

            Join3 = pd.merge(Join2, A1004, how='left', left_on='type', right_on='id', left_index=False,
                             right_index=False, sort=True).drop(columns='id_y')
            Join3.rename(columns={'id_x': 'id', 'name': 'type_name', 'c_id': 'type_c_id', 'level': 'type_level'},
                         inplace=True)

            B1001 = Join3.to_json(orient="records")
            con.close()
            return B1001

        if request.method == 'POST':
            post_data = request.json

            # Post variable
            # IF variable != None / Get mm_name
            # IF variable == None / Get Jia Yi Locations step by step
            # IF variable == 1 / Get [list of jia_yi_type]
            variable = post_data.get("variable")

            # Post Category ID
            id = post_data.get("id") # id of category
            c_id = post_data.get("c_id")
            level = post_data.get("level")

            print("POST")

            if variable == None:

                # Get Category Locations step by step
                A1001 = pd.read_sql("SELECT * from locations where c_id = '" + str(id) + "' ", con)

                A1002 = A1001.to_json(orient="records")
                con.close()
                return A1002

            elif variable == 0:

                # Get[list of jia_yi_type]
                A1001 = pd.read_sql("SELECT * from shop_category ", con)

                A1002 = A1001.to_json(orient="records")
                con.close()
                return A1002

            elif variable == -1:

                # Get[list of jia_yi_type]
                A1001 = pd.read_sql("SELECT * from object_category ", con)

                A1002 = A1001.to_json(orient="records")
                con.close()
                return A1002

            else:
                # Get Jia Yi MM Name
                A1001 = pd.read_sql("SELECT * from jia_yi_name where idname ILIKE '" + variable + "' ", con)
                # print(A1001)
                if A1001.empty:
                    print("输入错误！没有该数据！")
                    return "输入错误！没有该数据！"
                else:
                    A1002 = A1001.to_json(orient="records", lines=True)
                    print(A1002)
                    con.close()
                    return A1002


        if request.method == 'PUT':

            # Update Table
            put_data = request.json
            id = put_data.get("id")  # id of jia_yi_name
            township = put_data.get("township")  # id of township
            shop = put_data.get("shop")  # id of shop
            type = put_data.get("type")  # id of object
            status = 1
            print("PUT")

            cur = con.cursor()

            # Create Table jia_yi_info
            sql_create = """CREATE TABLE IF NOT EXISTS jia_yi_info(id  INT PRIMARY KEY,
                                                    shop           INT      NOT NULL,
                                                    type            jsonb       NOT NULL,
                                                    status        INT       NOT NULL
                                                    );"""
            cur.execute(sql_create)

            import json
            type = json.dumps(type)

            # Insert id/township/type/status To SQL
            sql_insert = "INSERT INTO jia_yi_info (id,shop,type,status) Values" \
                         "('" + str(id) + "', '" + str(shop) + "', '" + type + "','" + str(status) + "')"
            cur.execute(sql_insert)
            con.commit()

            # con.close()

            return jsonify("")

    except Exception:
        print("Error:出错啦！！！")
        return jsonify("")