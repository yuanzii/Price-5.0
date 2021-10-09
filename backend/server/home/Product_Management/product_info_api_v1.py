from home import home
from flask import request, jsonify
import pandas as pd
import numpy as np

@home.route('/yuanzii_api/product_info_api', methods=["POST","GET","PUT"])
def product_info_api():
    import db.psql_psycopg2 as con
    import importlib
    importlib.reload(con)
    from db.psql_psycopg2 import con

    try:

        cur = con.cursor()

        if request.method == 'GET':
            try:
                print("GET")

                A1001 = pd.read_sql("SELECT * from product_name ", con)
                A1002 = pd.read_sql("SELECT * from product_info ", con)
                A1003 = pd.read_sql("SELECT * from product_category ", con)
                A1004 = pd.read_sql("SELECT * from product_description ", con)
                A1005 = pd.read_sql("SELECT * from duty_price ", con)

                Join1 = pd.merge(A1001, A1002, how='left', on='id', left_index=False,
                                 right_index=False, sort=True)
                Join2 = pd.merge(Join1, A1003, how='left', left_on='type', right_on='id', left_index=False,
                                 right_index=False, sort=True).drop(columns='id_y')
                Join2.rename(columns={'id_x': 'id', 'name': 'type_name', 'c_id': 'type_c_id', 'level': 'type_level'},
                             inplace=True)
                Join3 = pd.merge(Join2, A1004, how='left', on='id', left_index=False,
                                 right_index=False, sort=True)
                Join4 = pd.merge(Join3, A1005, how='left', left_on='duty', right_on='id', left_index=False,
                                 right_index=False, sort=True).drop(columns=['id_y'])
                Join4.rename(columns={'id_x': 'id', 'idname_x': 'idname', 'mm_name_x': 'mm_name', 'd_name_x': 'd_name',
                                      'idname_y': 'duty_idname', 'mm_name_y': 'duty_mm_name', 'd_name_y': 'duty_d_name',
                                      'price': 'duty_price'}, inplace=True)

                B1001 = Join4.to_json(orient="records")

                return B1001

            except Exception:

                try:
                    A1001 = pd.read_sql("SELECT * from product_name ", con)
                    A1002 = pd.read_sql("SELECT * from product_info ", con)
                    A1003 = pd.read_sql("SELECT * from product_category ", con)

                    Join1 = pd.merge(A1001, A1002, how='left', on='id', left_index=False,
                                 right_index=False, sort=True)
                    Join2 = pd.merge(Join1, A1003, how='left', left_on='type', right_on='id', left_index=False,
                                     right_index=False, sort=True).drop(columns='id_y')
                    Join2.rename(
                        columns={'id_x': 'id', 'name': 'type_name', 'c_id': 'type_c_id', 'level': 'type_level'},
                        inplace=True)

                    B1001 = Join2.to_json(orient="records")

                    return B1001

                except Exception:

                    A1001 = pd.read_sql("SELECT * from product_name ", con)
                    B1001 = A1001.to_json(orient="records")

                    return B1001

                return jsonify("Error")

        # if request.method == 'POST':
        #     post_data = request.json
        #
        #     variable = post_data.get("variable")
        #     id = post_data.get("id")  # id of product's category
        #     type = post_data.get("type")  # id of product's category
        #
        #     print("POST")
        #     print(variable)
        #     print(type)
        #
        #     try:
        #         A1001 = pd.read_sql("SELECT * from product_name ", con)
        #         A1002 = pd.read_sql("SELECT * from product_info ", con)
        #         A1003 = pd.read_sql("SELECT * from product_category ", con)
        #         A1004 = pd.read_sql("SELECT * from product_description ", con)
        #         A1005 = pd.read_sql("SELECT * from duty_price ", con)
        #
        #         Join1 = pd.merge(A1001, A1002, how='left', on='id', left_index=False,
        #                          right_index=False, sort=True)
        #         Join2 = pd.merge(Join1, A1003, how='left', left_on='type', right_on='id', left_index=False,
        #                          right_index=False, sort=True).drop(columns='id_y')
        #         Join2.rename(columns={'id_x': 'id', 'name': 'type_name', 'c_id': 'type_c_id', 'level': 'type_level'},
        #                      inplace=True)
        #         Join3 = pd.merge(Join2, A1004, how='left', on='id', left_index=False,
        #                          right_index=False, sort=True)
        #         Join4 = pd.merge(Join3, A1005, how='left', left_on='duty', right_on='id', left_index=False,
        #                          right_index=False, sort=True).drop(columns=['id_y'])
        #         Join4.rename(columns={'id_x': 'id', 'idname_x': 'idname', 'mm_name_x': 'mm_name', 'd_name_x': 'd_name',
        #                               'idname_y': 'duty_idname', 'mm_name_y': 'duty_mm_name', 'd_name_y': 'duty_d_name',
        #                               'price': 'duty_price'}, inplace=True)
        #
        #         try:
        #             print("try")
        #             A1001 = pd.read_sql("SELECT id FROM product_info WHERE type = '" + str(type) + "'", con)
        #             Join1 = pd.merge(Join4, A1001, on='id', left_index=False, right_index=False, sort=True)
        #             B2002 = Join1.to_json(orient="records")
        #             return B2002
        #
        #         except:
        #             print("except")
        #             B2002 = Join4.to_json(orient="records")
        #             return B2002
        #
        #     except:
        #
        #         try:  # variable != None: else: variable = id name
        #             print("product_info_api1")
        #             # Get Jia Yi MM Name
        #             A1001 = pd.read_sql("SELECT * from product_name where idname ILIKE '" + variable + "' ", con)
        #             print(A1001)
        #             # if A1001.empty:
        #             #     print("输入错误！没有该数据！")
        #             #     return "输入错误！没有该数据！"
        #             # else:
        #             A1002 = A1001.to_json(orient="records", lines=True)
        #             print("A1002"+A1002)
        #
        #             return A1002
        #
        #         except:
        #
        #             try:  # variable == None:
        #                 print("product_info_api2")
        #                 # Get Product Category step by step
        #                 A1001 = pd.read_sql("SELECT * from product_category where c_id = '" + str(id) + "' ", con)
        #
        #                 A1002 = A1001.to_json(orient="records")
        #
        #                 return A1002
        #
        #             except:
        #
        #                 if variable == -1:  # variable == -1:
        #                     print("product_info_api3")
        #                     # Get Type Of Product That was inserted in product_info
        #                     A1001 = pd.read_sql("SELECT * from product_info ", con)
        #                     A1002 = pd.read_sql("SELECT * from product_category ", con)
        #                     duplicate_A1001 = A1001.drop_duplicates('type')
        #                     Join1 = pd.merge(duplicate_A1001, A1002, how='left', left_on='type', right_on='id',
        #                                      left_index=False,right_index=False, sort=True).drop(columns='id_y')
        #                     Join1.rename(
        #                         columns={'id_x': 'id', 'name': 'type_name', 'c_id': 'type_c_id', 'level': 'type_level'},
        #                         inplace=True)
        #
        #                     B2002 = Join1.to_json(orient="records")
        #
        #                     return B2002
        #
        #                 else:  # variable == -2:
        #                     print("product_info_api4")
        #                     # Get Name Of Duty From duty_price Datatable
        #                     A1001 = pd.read_sql("SELECT * from duty_price ", con)
        #                     B2002 = A1001.to_json(orient="records")
        #                     print(B2002)
        #
        #                     return B2002

        if request.method == 'POST':
            post_data = request.json

            variable = post_data.get("variable")
            id = post_data.get("id")  # id of product's category
            type = post_data.get("type")  # id of product's category

            print("POST")
            print(variable)

            if variable == -1:
                # Load Data
                A1001 = pd.read_sql("SELECT * from product_name ", con)
                A1002 = pd.read_sql("SELECT * from product_info ", con)
                A1003 = pd.read_sql("SELECT * from product_category ", con)
                A1004 = pd.read_sql("SELECT * from product_description ", con)
                A1005 = pd.read_sql("SELECT * from duty_price ", con)

                Join1 = pd.merge(A1001, A1002, how='left', on='id', left_index=False,
                                 right_index=False, sort=True)
                Join2 = pd.merge(Join1, A1003, how='left', left_on='type', right_on='id', left_index=False,
                                 right_index=False, sort=True).drop(columns='id_y')
                Join2.rename(columns={'id_x': 'id', 'name': 'type_name', 'c_id': 'type_c_id', 'level': 'type_level'},
                             inplace=True)
                Join3 = pd.merge(Join2, A1004, how='left', on='id', left_index=False,
                                 right_index=False, sort=True)
                Join4 = pd.merge(Join3, A1005, how='left', left_on='duty', right_on='id', left_index=False,
                                 right_index=False, sort=True).drop(columns=['id_y'])
                Join4.rename(columns={'id_x': 'id', 'idname_x': 'idname', 'mm_name_x': 'mm_name', 'd_name_x': 'd_name',
                                      'idname_y': 'duty_idname', 'mm_name_y': 'duty_mm_name', 'd_name_y': 'duty_d_name',
                                      'price': 'duty_price'}, inplace=True)
                try:
                    print("try --> to get only product that was selected type of product")
                    A1001 = pd.read_sql("SELECT id FROM product_info WHERE type = '" + str(type) + "'", con)
                    Join1 = pd.merge(Join4, A1001, on='id', left_index=False, right_index=False, sort=True)
                    B2002 = Join1.to_json(orient="records")
                    return B2002

                except:
                    print("except --> to get all product")
                    B2002 = Join4.to_json(orient="records")
                    return B2002

            elif variable == -2:

                print("Get Type List Of Product That was inserted in product_info")

                # Get Type List Of Product That was inserted in product_info
                A1001 = pd.read_sql("SELECT * from product_info ", con)
                A1002 = pd.read_sql("SELECT * from product_category ", con)
                duplicate_A1001 = A1001.drop_duplicates('type')
                Join1 = pd.merge(duplicate_A1001, A1002, how='left', left_on='type', right_on='id',
                                 left_index=False,right_index=False, sort=True).drop(columns='id_y')
                Join1.rename(
                    columns={'id_x': 'id', 'name': 'type_name', 'c_id': 'type_c_id', 'level': 'type_level'},
                    inplace=True)

                B2002 = Join1.to_json(orient="records")

                return B2002

            elif variable == -3:

                print("Get Name Of Duty From duty_price Datatable")

                # Get Name Of Duty From duty_price Datatable
                A1001 = pd.read_sql("SELECT * from duty_price ", con)
                B2002 = A1001.to_json(orient="records")

                return B2002

            elif variable != None:  # variable == id name

                print("Get Jia Yi MM Name")

                # Get Jia Yi MM Name
                A1001 = pd.read_sql("SELECT * from product_name where idname ILIKE '" + variable + "' ", con)
                print(A1001)
                if A1001.empty:
                    print("Error!empty data.")
                    return "Error!empty data."
                else:
                    A1002 = A1001.to_json(orient="records", lines=True)

                return A1002

            else:  # variable == None:

                print("Get Product Category step by step")

                # Get Product Category step by step
                A1001 = pd.read_sql("SELECT * from product_category where c_id = '" + str(id) + "' ", con)
                A1002 = A1001.to_json(orient="records")

                return A1002

        if request.method == 'PUT':

            put_data = request.json

            variable = put_data.get("variable")

            id = put_data.get("id")  # id of product
            type = put_data.get("type")  # id of type (type of product)
            duty = put_data.get("duty")  # id of duty
            weight = put_data.get("weight")  # weight of product
            status = 1

            print("PUT")

            # Create Table product_info
            sql_create = """CREATE TABLE IF NOT EXISTS product_info(id  INT PRIMARY KEY,
                                                                type           INT      NOT NULL,
                                                                duty            INT      ,
                                                                status        INT       NOT NULL
                                                                );"""
            cur.execute(sql_create)

            # Create Table product_description insert weight
            sql_create = """CREATE TABLE IF NOT EXISTS product_description(id  INT PRIMARY KEY,
                                                                            weight    Float    NOT NULL
                                                                            );"""
            cur.execute(sql_create)

            if variable == -1:

                # Insert and Update Weight

                sql_insert_update = "INSERT INTO product_description (id,weight) Values" \
                             "('" + str(id) + "', '" + str(weight) + "') ON conflict(id)" \
                             "DO UPDATE SET weight = '" + str(weight) + "'"
                cur.execute(sql_insert_update)

                con.commit()

                return jsonify("Insert and Update Weight")

            elif variable == -2:

                # UPDATE：id of duty To SQL

                sql_update = """UPDATE product_info SET duty = %s WHERE type = %s"""
                val = (duty, type)

                cur.execute(sql_update, val)
                con.commit()

                return jsonify("Update duty To product_info(SQL)")

            else:  # variable == type: type id of product

                # Insert and Update id/type/duty/status To SQL

                sql_insert_update = "INSERT INTO product_info (id,type,status) Values" \
                                    "('" + str(id) + "', '" + str(type) + "', '" + str(status) + "')" \
                                     "ON conflict(id) DO UPDATE SET type = '" + str(type) + "'"
                cur.execute(sql_insert_update)
                con.commit()

                return jsonify("Insert and Update type To SQL")

    except Exception:
        print("Error_Finally:出错啦！！！")
        return jsonify("Error_Finally:  မှားသွားပြီ။")

    finally:
        cur.close()
        con.close()
        print("close")