from home import home
from flask import request, jsonify
import pandas as pd
import numpy as np

@home.route('/yuanzii_api/product_category_api', methods=["POST","GET","PUT"])
def product_category_api():
    import db.psql_psycopg2 as con
    import importlib
    importlib.reload(con)
    from db.psql_psycopg2 import con

    try:

        cur = con.cursor()

        if request.method == 'POST':
            post_data = request.json

            # Post Level and id(c_id) To Get Category Locations step by step
            id = post_data.get("id")

            # Post category_name/c_id/level To SQL
            name = post_data.get("name")
            c_id = post_data.get("c_id")
            level = post_data.get("level")
            print("POST")

            # Create Table product_category
            cur = con.cursor()
            sql_create = """CREATE TABLE IF NOT EXISTS product_category(id  SERIAL  PRIMARY KEY,
                                                                                name           TEXT      NOT NULL,
                                                                                c_id            INT       NOT NULL,
                                                                                level        INT       NOT NULL
                                                                                );"""
            cur.execute(sql_create)

            if name == None:

                # Get Category Locations step by step
                A1001 = pd.read_sql("SELECT * from product_category where level = '" + str(level) + "' \
                and c_id = '" + str(id) + "' order by id asc ", con)
                A1002 = pd.read_sql("SELECT * from product_category ", con)

                Join1 = pd.merge(A1001, A1002, how='left', left_on='c_id', right_on='id', left_index=False,
                                 right_index=False, sort=True)

                A1003 = Join1.to_json(orient="records")
                # con.close()
                print(Join1)
                return A1003

            else:
                print("level")

                # Insert category_name/c_id/level To SQL
                sql_insert = "INSERT INTO product_category(name, c_id,level) Values" \
                             "('" + name + "', '" + str(c_id) + "', '" + str(level) + "')"
                cur.execute(sql_insert)
                print(sql_insert)
                con.commit()

                return jsonify("Insert category_name/c_id/level To SQL")

        if request.method == 'PUT':

            put_data = request.json

            # PUT variable
            # IF variable == 1 / Delete row
            # IF variable == 0 / Delete row
            # IF variable == None / 檢查要刪除數據裏有沒有子數據

            variable = put_data.get("variable")

            print(variable)

            # Put category_name/c_id/level To SQL
            id = put_data.get("id")
            name = put_data.get("name")
            c_id = put_data.get("c_id")
            level = put_data.get("level")

            print("PUT")
            print(id)

            if variable == 1:

                cur = con.cursor()
                sql_delete = "DELETE FROM product_category WHERE id = '" + str(id) + "'"
                cur.execute(sql_delete)
                print(sql_delete)

                con.commit()
                # con.close()

                return jsonify("")

            elif variable == 0:

                # 檢查要刪除數據裏有沒有子數據
                A1001 = pd.read_sql("SELECT * from product_category where \
                                c_id = '" + str(id) + "' order by id asc ", con)
                A1002 = A1001.to_json(orient="records")
                # con.close()

                return A1002

            elif variable == 2:

                # 查詢該等級的父類c_name，所以當前等級-1; level-1
                A1001 = pd.read_sql("SELECT * from product_category where \
                                level = '" + str(level-1) + "' order by id asc ", con)
                A1002 = A1001.to_json(orient="records")
                # con.close()

                return A1002

            else:
                # UPDATE：Edit category_name To SQL
                cur = con.cursor()
                sql_update = """UPDATE product_category SET name = %s,c_id = %s WHERE id = %s"""
                val = (name, c_id, id)
                cur.execute(sql_update, val)

                con.commit()
                # con.close()

                return jsonify("")

    except Exception:
        print("Error:出错啦！！！")
        return jsonify("Error:出错啦！！！")

    finally:
        cur.close()
        con.close()
        print("close")

