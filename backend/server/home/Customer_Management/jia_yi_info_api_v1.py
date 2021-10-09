from home import home
from flask import request, jsonify
import pandas as pd
import numpy as np

@home.route('/yuanzii_api/jia_yi_info_api_v1', methods=["POST","GET","PUT"])
def jia_yi_info_api_v1():
    import db.psql_psycopg2 as con
    import importlib
    importlib.reload(con)
    from db.psql_psycopg2 import con

    try:
        if request.method == 'GET':
            print("GET")
            A1001 = pd.read_sql("SELECT * from jia_yi_name ", con)

            A1002 = A1001.to_json(orient="records")
            con.close()
            return A1002

        if request.method == 'POST':
            post_data = request.json

            # Post jia_yi_idname / Get mm_name
            jia_yi_idname = post_data.get("jia_yi_idname")

            # Post Category ID
            id = post_data.get("id")
            c_id = post_data.get("c_id")
            level = post_data.get("level")
            print("POST")

            if jia_yi_idname == None:

                # Get Category Locations step by step
                A1001 = pd.read_sql("SELECT * from locations where c_id = '" + str(id) + "' ", con)

                A1002 = A1001.to_json(orient="records")
                con.close()
                return A1002

            else:

                # Get Jia Yi MM Name
                A1001 = pd.read_sql("SELECT * from jia_yi_name where idname ILIKE '" + jia_yi_idname + "' ", con)
                print(A1001)
                if A1001.empty:
                    print("输入错误！没有该数据！")
                    return "输入错误！没有该数据！"
                else:
                    A1002 = A1001.to_json(orient="records", lines=True)
                    con.close()
                    return A1002

        if request.method == 'PUT':

            put_data = request.json
            id = put_data.get("id")
            idname = put_data.get("idname")
            mm_name = put_data.get("mm_name")
            state = put_data.get("state")
            district = put_data.get("district")
            town_ship = put_data.get("town_ship")
            village_tract = put_data.get("village_tract")
            type = put_data.get("type")
            status = 1
            print("PUT")

            cur = con.cursor()

            # Add Coloum to sql jia_yi_name table
            sql_alter = """ALTER TABLE jia_yi_name ADD COLUMN IF NOT EXISTS state VARCHAR,ADD COLUMN IF NOT EXISTS 
            district VARCHAR,ADD COLUMN IF NOT EXISTS township VARCHAR,ADD COLUMN IF NOT EXISTS 
            village_tract VARCHAR,ADD COLUMN IF NOT EXISTS type VARCHAR,ADD COLUMN IF NOT EXISTS 
            status INT NOT NULL DEFAULT(0)"""
            cur.execute(sql_alter)

            # Update jia_yi locations to jia_yi_name table
            sql_update = """UPDATE jia_yi_name SET state = %s ,district = %s,township = %s ,
            village_tract = %s ,type = %s,status = %s WHERE id = %s"""
            val = (state, district, town_ship, village_tract, type, status, id)
            cur.execute(sql_update, val)

            con.commit()
            # con.close()

            return jsonify("")

    except Exception:
        print("Error:出错啦！！！")
        return jsonify("")