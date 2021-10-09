from home import home
from flask import request, jsonify
import pandas as pd
import numpy as np

@home.route('/yuanzii_api/purchase_price_api', methods=["POST","GET","PUT"])
def purchase_price_api():
	import db.psql_psycopg2 as psql_psycopg2
	import db.psql_sqlalchemy as psql_sqlalchemy
	import db.pyodbc as pyodbc
	import db.mongodb as mongodb

	import importlib
	importlib.reload(psql_psycopg2)
	importlib.reload(psql_sqlalchemy)
	importlib.reload(pyodbc)
	importlib.reload(mongodb)

	from db.psql_psycopg2 import con
	from db.psql_sqlalchemy import engine_price
	from db.pyodbc import con_185_CF內配
	from db.mongodb import client

	try:

		if request.method == 'GET':

			# Postgresql
			cur = con.cursor()

			# Create Table purchase_price
			sql_create = """CREATE TABLE IF NOT EXISTS purchase_price(serial_id  SERIAL PRIMARY KEY ,
																	datetime  TIMESTAMP , 
																	id  INT ,
																	lei  INT ,
																	price  NUMERIC(15, 4)   
																	);"""
			cur.execute(sql_create)
			con.commit()

			# Create Table price
			sql_create = """CREATE TABLE IF NOT EXISTS price(id  INT PRIMARY KEY,
														s_price    NUMERIC(15, 4) ,
														cost_price    NUMERIC(15, 4) ,
														o_price      NUMERIC(15, 4)    ,
														kt_price      NUMERIC(15, 4)    
														);"""
			cur.execute(sql_create)
			con.commit()

			purchase_price = pd.read_sql("SELECT * from purchase_price ", con)
			price = pd.read_sql("SELECT * from price ", con)

			# MongoDB
			data = client['data']
			
			ji10001 = data['ji10001']
			mongo_ji10001 = pd.DataFrame(list(ji10001.find({}))).drop(columns='_id')
			mongo_ji10001 = mongo_ji10001[['日期','類編1','類編2','甲方','乙方','Y編','數量','進價','售價']]

			product_name = data['product_name']
			mongo_product_name = pd.DataFrame(list(product_name.find({}))).drop(columns='_id')
			mongo_product_name = mongo_product_name[['id','idname','mm_name','d_name']]

			# 获取当天的最高价钱
			S_O = mongo_ji10001.loc[(mongo_ji10001.類編1==42)&(mongo_ji10001.類編2==22)].sort_values(
				by='進價', ascending=False) 

			# 通过groupby id 然后选择最大的日期 来获取最后的S价
			Last_S = S_O.loc[S_O.groupby(["Y編"])["日期"].idxmax()].drop(columns=[ '類編2', '甲方', 
					'乙方', '數量', '售價'])
			Last_S.rename(columns={'類編1':'lei', 'Y編':'id', '日期':'datetime','進價':'price'}, inplace = True)

			Last_S = Last_S[['datetime','id','lei','price']]
			Last_S = Last_S.round(4)

			# 测试是否唯一
			duplicate = Last_S.duplicated('id') 

			# 通过两张表对比 id 和 s价钱 update 最新价钱
			Join = (Last_S.merge(purchase_price, on=['id','price'], how='left', indicator=True).query(
					'_merge == "left_only"')).drop(columns=['datetime_y', 'lei_y', '_merge'])
			Join.rename(columns={'datetime_x': 'datetime', 'lei_x': 'lei'},inplace=True)
			
			# Insert changed rows to psql --> purchase_price table
			Join.to_sql(name='purchase_price', con=engine_price, if_exists='append',index=False)

			# annalysis purchase_price table --> 一個id的最新价钱
			purchase_price = pd.read_sql("SELECT * from purchase_price ", con)
			# 为了获取当天最高价钱，倒序排列价钱
			purchase_price = purchase_price.loc[(purchase_price.lei==42)].sort_values(by='price', ascending=False) 
			purchase_price = purchase_price.loc[purchase_price.groupby(["id"])["datetime"].idxmax()]
			purchase_price = purchase_price.round(4)

			Join2 = (purchase_price.merge(price, left_on=['id','price'], right_on=['id','s_price'], how='left', 
					indicator=True).query('_merge == "left_only"'))
			# tempolary table
			Join2.to_sql('temp_table', con=engine_price, if_exists='replace')

			# Update s_price --> price table
			sql_update = """UPDATE price AS a SET s_price = b.price FROM temp_table AS b WHERE a.id = b.id"""
			cur.execute(sql_update)

			return jsonify(" ")

	except Exception:

		print("Error ！！！")
		return jsonify("Error ！！！")

	finally:
		
		con.close()
		cur.close()
		engine_price.dispose()
		con_185_CF內配.close()
		client.close()
		print("close")

