# cost_ratio_api_4.1
# 直接拿最后进货次数的数量>库存来获得成本，数据更准确
# 开销 13:30前的数据删掉
# 計4編 --> 目前爲止完全沒有重複數據!!!
# 實現水泥和雜貨開銷,公平且準確
# 同一產品每日開銷差距>0.5%的 insert 到數據表
# 運行時間 大概30分鐘
# 分類了供貨商和倉庫 --> 查詢的時候更方便，代碼更加整結了
# 增加了 "中介"倉庫 再從該倉庫進貨到倉庫12
# 庫存in stock是o_ku_jin --> 今天歸零的庫存 ，防止去誤算今天進的貨，因爲今天進的貨成本還不出來
# 單獨進一車的全部產品額外以價錢區分 （價錢存在漲跌）
# 單獨進一車的產品 如果貨不滿車則排除該筆 （防止進賬錯）
from home import home
from flask import request, jsonify
import pandas as pd
import numpy as np

@home.route('/yuanzii_api/cost_ratio_api', methods=["POST","GET","PUT"])
def cost_ratio_api():
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

			import datetime
			import pytz

			import dateutil.parser
			from dateutil.relativedelta import relativedelta

			import requests
			import json

			tz = pytz.timezone('Asia/Yangon')  # 缅甸时间 TimeZone
			d = datetime.datetime.now(tz=tz).strftime('%Y-%m-%d')  # only date

			dt = datetime.datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M:%S')  # date time

			two_years = datetime.datetime.now(tz=tz) - relativedelta(months=24)
			two_years = datetime.datetime.strftime(two_years, '%Y-%m-%d')  # two years ago

			five_years = datetime.datetime.now(tz=tz) - relativedelta(months=60)
			five_years = datetime.datetime.strftime(five_years, '%Y-%m-%d')  # five years ago

			print(d)
			print(dt)
			print(two_years)
			print(five_years)

			# 開始運行的時間
			start_time_main = datetime.datetime.now()
			print(start_time_main)

			# Postgresql
			cur = con.cursor()

			# Create Table cost subsidy(補貼)
			sql_create = """CREATE TABLE IF NOT EXISTS inventory_cost(serial_id  SERIAL PRIMARY KEY ,
																		id  INT , 
																		datetime  TIMESTAMPTZ , 
																		s_price  NUMERIC(15, 2) ,
																		cost_ratio  NUMERIC(15, 4) ,
																		price  NUMERIC(15, 2) ,   
																		subsidy  NUMERIC(15, 2) 
																		);"""
			cur.execute(sql_create)
			con.commit()

			# MongoDB
			data = client['data']

			# ji10001 兩年的资料
			ji10001_all = data['ji10001_all']
			ji10001_2y = pd.DataFrame(list(ji10001_all.find({"日期": {"$gte": dateutil.parser.parse(two_years), "$lt":
							dateutil.parser.parse(d)}}))).drop(columns='_id').sort_values(by='日期', ascending=False)

			ji10001_2y_df = ji10001_2y[['進貨編','日期','歸零日期','類編1','類編2','甲方','乙方','Y編','數量','進價','售價',
										'計4編']]

			# 分類后的數據jia_yi_info
			jia_yi_info_tb = pd.read_sql("SELECT * from jia_yi_info", con)

			str_convert_int = jia_yi_info_tb.to_dict('records')  # str convert to int
			jia_yi_info_json_list = pd.json_normalize(str_convert_int, 'type', ['id', 'shop'])  # have list

			cate_shop12 = jia_yi_info_json_list.loc[
				(jia_yi_info_json_list.shop == 1) | (jia_yi_info_json_list.shop == 2)]  # 店鋪12
			cate_shop123 = jia_yi_info_json_list.loc[
				(jia_yi_info_json_list.shop == 1) | (jia_yi_info_json_list.shop == 2) |
				(jia_yi_info_json_list.shop == 3)]  # 店鋪123
			cate_shop4 = jia_yi_info_json_list.loc[(jia_yi_info_json_list.shop == 4)]  # 店鋪4

			cate_supplier = cate_shop12.loc[(cate_shop12.obj_id == 2)]  # 供貨商

			cate_ware_room12 = cate_shop12.loc[cate_shop12.obj_id == 3]  # 倉庫12

			cate_ware_room123 = cate_shop123.loc[cate_shop123.obj_id == 3]  # 倉庫123

			cate_ware_room4 = cate_shop4.loc[cate_shop4.obj_id == 3]  # 倉庫4

			# 合并供貨商和倉庫4  .drop_duplicates() 去重目前沒必要
			cate_supplier_ware_room4 = pd.concat([cate_supplier, cate_ware_room4])

			# 進價
			進價1001_pyodbc = pd.read_sql("SELECT * from 進價1001", con_185_CF內配)

			# 存放在shwethe1/2/3的倉庫的進價
			ware_room123_df = pd.merge(進價1001_pyodbc, cate_ware_room123, how='left', left_on=['甲方'], right_on=['id'],
									left_index=False, right_index=False, sort=True).dropna(subset=['id']
									).drop_duplicates().drop(columns=['obj_id', 'id', 'shop', ])

			last_s_df = ware_room123_df.groupby("Y編").agg({'進價': 'max'}).reset_index().rename(
				columns={'Y編': 'id', '進價': 's_price'})

			# 供貨商和中介倉庫(倉庫4)
			supplier_df = pd.merge(ji10001_2y_df, cate_supplier_ware_room4, how='left', left_on=['甲方'],
								right_on=['id'], left_index=False, right_index=False, sort=True).dropna(
								subset=['id']).drop_duplicates().drop(columns=['obj_id', 'id', 'shop', ])

			# 進貨 --> 倉庫12
			supplier_to_ware_room12 = pd.merge(supplier_df, cate_ware_room12, how='left', left_on=['乙方'],
											right_on=['id'], left_index=False, right_index=False, sort=True
											).dropna(subset=['id']).drop_duplicates().sort_values(by='歸零日期',
											ascending=False).drop(columns=['obj_id', 'id', 'shop', ])

			# pyodbc --> 近兩年的資料
			進100402 = pd.read_sql("SELECT * from 進100402 where 歸零日期>=dateadd(month,-24,getdate()) ", con_185_CF內配)
			進100402 = 進100402.sort_values(by='歸零日期', ascending=False)

			# 這個進貨編號沒有今天歸零的數據
			purchase_code_x = 進100402[['進貨編', '歸零日期', '類編2', 'Y編', '數量', 's開銷', 's貨款', '計4編']]

			# pyodbc
			# pd.set_option('display.max_columns', None)
			進2001 = pd.read_sql("SELECT * from 進2001 where 日期1>=dateadd(month,-24,getdate())", con_185_CF內配)
			進2001 = 進2001.sort_values(by='歸零日期', ascending=False)

			purchase_code_y = 進2001[['進貨編', '歸零日期', '備忘錄m', '商品分類']]

			purchase_code = pd.merge(purchase_code_x, purchase_code_y, how='left', on=['進貨編', '歸零日期'],
									 left_index=False, right_index=False,
									 sort=True).sort_values(by='歸零日期', ascending=False)

			# 刪除商品分類isnull()的數據
			purchase_code = purchase_code.dropna(subset=['商品分類'])

			# 排除當天同時有兩筆進出的數據
			for idx, data in purchase_code.iterrows():

				count_minus = data[4]

				# 为了得出当天 进出 的 (-)数量 的index
				if count_minus < 0:

					# 得到日期
					df = purchase_code.loc[(purchase_code['歸零日期'] == data[1])]
					# 同一日期下的同一个商品
					df = df.loc[(df['Y編'] == data[3])]

					# 得出当天 进出 的 (+)数量 的index
					count_plus = count_minus * -1
					index_count_plus = df[df.數量 == count_plus].index

					# 判断：当天有同时进出的两笔则删除
					if index_count_plus != None:
						# 删除 有(-)的数据
						drop_index_df_1 = purchase_code.drop(index=idx, axis=1)

						# 在drop_index_df_1基础上删除(+)数据
						purchase_code = drop_index_df_1.drop(index=index_count_plus, axis=1)

		# 檢查計4編有沒有問題
		purchase_code_ji4 = purchase_code.dropna(subset=['s貨款']).sort_values(by='計4編', ascending=False)
		purchase_code_ji4 = purchase_code_ji4.loc[(purchase_code_ji4.歸零日期 == d)]

		# 排除當天同時有兩筆進出的數據
		for for1_idx, for1_data in supplier_to_ware_room12.iterrows():

			count_minus = for1_data[8]

			# 为了得出当天 进出 的 (-)数量 的index
			if count_minus < 0:

				# 得到日期
				datetime_0_df = supplier_to_ware_room12.loc[(supplier_to_ware_room12['歸零日期'] == for1_data[2])]
				# 同一日期下的同一个商品
				id_df = datetime_0_df.loc[(datetime_0_df['Y編'] == for1_data[7])]  # 从0开始数到7列

				# 得出当天 进出 的 (+)数量 的index
				count_plus = count_minus * -1
				index_count_plus_list = id_df[id_df.數量 == count_plus].index.values.tolist()

				# 判断：当天有同时进出的两笔则删除
				if index_count_plus_list != []:

					for index_count_plus in index_count_plus_list:

						進貨編 = id_df.loc[index_count_plus, '進貨編']

						if 進貨編 == 0:
							# 删除 有(-)的数据
							drop_index_df_1 = supplier_to_ware_room12.drop(index=for1_idx, axis=1)

							# 在drop_index_df_1基础上删除(+)数据
							supplier_to_ware_room12 = drop_index_df_1.drop(index=index_count_plus, axis=1)
							break


		# 檢查計4編有沒有問題
		supplier_to_ware_room12_ji4 = supplier_to_ware_room12.loc[(supplier_to_ware_room12.歸零日期 == d)
										].sort_values(by='計4編', ascending=False)

		# 比較計4編
		# 計4編_y = NaN --> 1.可能是0開銷，2.供應商(S)沒有裝進去，所以漏了
		# 計4編_x != 計4編_y --> 極大可能ji出錯了，得暫停運行
		ji4_compare = pd.merge(purchase_code_ji4, supplier_to_ware_room12_ji4, how='left', on=['進貨編','歸零日期','類編2','Y編','數量'],
					  left_index=False,right_index=False, sort=True).sort_values(by='歸零日期', ascending=False)
		ji4_compare = ji4_compare[['進貨編','Y編','乙方','計4編_x','計4編_y']]

		ji4_not_equare = ji4_compare.loc[ji4_compare.計4編_x != ji4_compare.計4編_y]

		# 如果有ji4不等於，則停止運行
		if len(ji4_not_equare) != 0:
			print("停止運行")
		else:
			print("繼續")

		# 爲了防止漏掉進貨的時候沒有進貨編的數據(没有进货编'零开销'的也带) --> 計4編 防止重複數據
		# purchase --> 进货
		purchase = pd.merge(supplier_to_ware_room12, purchase_code, how='left', on=['Y編', '歸零日期', '數量', '計4編'],
							left_index=False, right_index=False,
							sort=True).sort_values(by='歸零日期', ascending=False)

		purchase['類編2_x'] = purchase['類編2_x'].fillna(purchase['類編2_y'])
		purchase = purchase.drop(columns=['類編2_y', '進貨編_x'])
		purchase = purchase.rename(columns={'類編2_x': '類編2', 'Y編': 'id', '進貨編_y': '進貨編'})

		# 删除数量（-）的笔数 --> 无效数据 退回去的商品没有开销还会占笔数
		purchase = purchase.drop(purchase[(purchase['數量'] <= 0)].index)

		# qty api
		o_ku_jin_api = requests.get("http://192.168.1.85/mongodb_data_api/api/v1/data/o_ku_jin/qty")
		o_ku_jin = pd.DataFrame(json.loads(o_ku_jin_api.json())).round(2)

		# 庫存
		in_stock = pd.merge(o_ku_jin, cate_ware_room12, how='left', left_on=['jia_fang'], right_on=['id'],
							left_index=False, right_index=False, sort=True).dropna(subset=['id']
							).groupby("product_id").agg({'product_qty': 'sum'}).reset_index().rename(
							columns={'product_id': 'id', 'product_qty': 'stock'})

		# Join --> purchase & in_stock
		purchase_in_stock = pd.merge(purchase, in_stock, how='outer', on='id', left_index=False, right_index=False,
									 sort=True).sort_values(by='歸零日期', ascending=False)

		tz = pytz.timezone('Asia/Yangon')  # 缅甸时间 TimeZone
		d = datetime.datetime.now(tz=tz).strftime('%Y-%m-%d')
		dt = d + " 13:30:00"
		print(d)
		print(dt)

		# # 排除當天和當天13：30前的數據
		# purchase_in_stock = purchase_in_stock.drop(purchase_in_stock[(purchase_in_stock['歸零日期'] >= d)&
		#                 (purchase_in_stock['歸零日期'] < dt)].index)

		# 排除重複數據
		purchase_in_stock = purchase_in_stock.drop_duplicates()

		# 這一條可刪除 待定
		purchase_in_stock['數量'] = purchase_in_stock['數量'].fillna(0)

		# 計算成本
		cost = purchase_code.groupby("進貨編").agg({'s開銷': 'sum', 's貨款': 'sum'}).reset_index()
		cost['cost_ratio'] = cost['s開銷'] / cost['s貨款']
		cost = cost.drop(columns=['s開銷', 's貨款'])

		purchase_in_stock_cost = pd.merge(purchase_in_stock, cost, how='left', on='進貨編', left_index=False,
										  right_index=False, sort=True).sort_values(by='歸零日期', ascending=False)

		# cost_ratio = NaN 代表沒有开销 --> 替換成 0
		purchase_in_stock_cost['cost_ratio'] = purchase_in_stock_cost['cost_ratio'].fillna(0)

		# cost_ratio = inf 代表数据无效 --> 替換成 NaN --> 刪除
		purchase_in_stock_cost = purchase_in_stock_cost.replace([np.inf, -np.inf], np.nan).dropna(axis=0, subset=[
			'cost_ratio'])

		purchase_in_stock_cost = purchase_in_stock_cost[['進貨編', '日期', '歸零日期', '類編1', '類編2', '甲方', '乙方',
														 'id', '數量', '進價', '售價', '計4編', 's開銷', 's貨款',
														 '備忘錄m', '商品分類', 'stock', 'cost_ratio']]

		tz = pytz.timezone('Asia/Yangon')  # 缅甸时间 TimeZone
		d = datetime.datetime.now(tz=tz).strftime('%Y-%m-%d')
		print(d)

		one_product = purchase_in_stock_cost[purchase_in_stock_cost['商品分類'].notnull()]
		one_product = one_product.loc[(one_product.商品分類 != 341)]  # 排除是雜貨的車

		# 查詢只有一個商品的進貨編
		for one_product_idx, data in one_product.iterrows():

			df = one_product.loc[(one_product['進貨編'] == data[0])].sort_values(by="歸零日期",ascending=False)
			id_count = len(df.groupby("id"))

			if one_product_idx in one_product.index and id_count > 1:
				one_product = one_product.drop(df.index)

		one_product = one_product.sort_values(by='進貨編', ascending=False)

		# 一張車能裝多少產品表格
		car_net_qty_tb = pd.read_sql("SELECT id,type_car,net_qty from car_net_qty", con)
		not_trailer = car_net_qty_tb.loc[car_net_qty_tb.type_car != 438]

		cate_one_product = one_product
		# 刪除獨立產品的數量不滿車的數據
		for cate_one_product_idx, cate_one_product_data in cate_one_product.iterrows():

			cate_one_product_id = cate_one_product_data[[7]]
			cate_one_product_car = cate_one_product_data[[15]]

			if float(cate_one_product_id) in not_trailer[['id']].values:
				not_trailer_df = not_trailer.loc[(not_trailer.id == float(cate_one_product_id))]
				type_car_df = not_trailer_df.loc[(not_trailer_df.type_car == float(cate_one_product_car))]

				if type_car_df.index.values.tolist() != [] and cate_one_product_data[8] != float(
						type_car_df['net_qty']):
					cate_one_product = cate_one_product.drop(cate_one_product_idx)

		# 一張車僅帶一個產品的成本 --> 獨立產品
		one_product_per_car = cate_one_product.groupby(["id", "進價"]).agg(
			{'cost_ratio': 'mean'}).reset_index().round(4)

		# 只單獨拿水泥的id
		product_info_x = pd.read_sql("SELECT * from product_info ", con)
		product_category_x = pd.read_sql("SELECT * from product_category ", con)

		# 連起來
		product_info_y = pd.merge(product_info_x, product_category_x, how='left', left_on='type',
								  right_on='id').merge(
			product_category_x, how='left', left_on='c_id', right_on='id', left_index=False, right_index=False,
			sort=True).drop(
			columns={'id_y', 'id', 'duty', 'status', 'c_id_y', 'level_x', 'level_y'}).rename(
			columns={'type': 'c_id1', 'id_x': 'id', 'name_x': 'c_name1', 'c_id_x': 'c_id2', 'name_y': 'c_name2'})

		# 30 --> 水泥的類編
		cement = product_info_y.loc[product_info_y.c_id2 == 30]

		# 合并水泥和獨立產品，去重，只拿id
		cement_and_product_per_car = pd.concat(
			[one_product_per_car[['id']], cement[['id']]]).drop_duplicates().rename(columns={'id': 'both_id'})

		stock_ratio_test = purchase_in_stock_cost.sort_values(by='歸零日期', ascending=False)

		# 刪除多于庫存的進貨筆數
		for stock_ratio_test_idx, stock_ratio_test_data in stock_ratio_test.iterrows():

			print(stock_ratio_test_idx)

			if stock_ratio_test_idx in stock_ratio_test.index:

				print("index exist")

				# 以id來區分循環數據
				df = stock_ratio_test.loc[(stock_ratio_test['id'] == stock_ratio_test_data[7])]  # 從0開始數的列位置
				# 循環到第几次 -->初始為0
				count = 0
				# 相加后的采購数量總和 -->初始為0
				purchase_qty = 0

				for df_idx, df_data in df.iterrows():

					count += 1
					# 采购数量相加
					purchase_qty += df_data[8]
					# 庫存
					stock = df_data[16]

					# 當循環到的進貨的數量大於庫存，刪除剩餘的數據，推出循環
					if purchase_qty >= stock:
						# 要刪除的數量
						drop_qty = len(df) - count
						index_drop_qty = df.tail(drop_qty).index
						# 刪除
						stock_ratio_test = stock_ratio_test.drop(index=index_drop_qty, axis=1)

						# 退出循環
						break

		stock_ratio_test = stock_ratio_test.rename(columns={'進貨編': '進貨編_2'})

		# 先把獨立產品和水泥排在前面，再去排剩下的產品
		sort_purchase_in_stock_cost = pd.merge(purchase_in_stock_cost, cement_and_product_per_car, how='left',
											   left_on='id', right_on='both_id', left_index=False,
											   right_index=False, sort=True).sort_values(by='both_id',
																						 ascending=True)

		# 簡短數據-->
		stock_ratio = pd.merge(sort_purchase_in_stock_cost,
							stock_ratio_test[['進貨編_2', '歸零日期', 'id', '數量', '進價', '計4編', 's貨款']],
							how='left', left_on=['進貨編', '歸零日期', 'id', '數量', '計4編'], right_on=['進貨編_2',
							'歸零日期', 'id', '數量', '計4編'], left_index=False, right_index=False, sort=True).drop(
							columns={'進價_y', 's貨款_y'}).rename(columns={'進價_x': '進價', 's貨款_x': 's貨款'})

		# 刪除進貨編不在stock_ratio df裏的
		for stock_ratio_idx, stock_ratio_data in stock_ratio.iterrows():
			# 進貨編 = NaN 的話無效
			df = stock_ratio.loc[(stock_ratio['進貨編'] == stock_ratio_data[0])]
			if stock_ratio_data[0] not in df[['進貨編_2']].values:
				stock_ratio = stock_ratio.drop(df.index)

		stock_ratio = stock_ratio.sort_values(by='both_id', ascending=True)

		# 先計算獨立產品和水泥的開銷，再把剩餘的開銷以金額為准分給其他產品
		count = 0
		for stock_ratio_idx, stock_ratio_data in stock_ratio.iterrows():
			count += 1
			print(count)
			stock_ratio_進貨編 = stock_ratio_data[0]
			stock_ratio_cost = stock_ratio_data[17]
			stock_ratio_id = stock_ratio_data[7]
			purchase_price = stock_ratio_data[9]
			stock_ratio_car = stock_ratio_data[15]

			df = stock_ratio.loc[(stock_ratio['進貨編'] == stock_ratio_進貨編)]  #
			id_count = len(df.groupby("id"))

			# 刪除獨立產品的數量不滿車的數據
			if id_count == 1 and stock_ratio_cost != 0 and stock_ratio_id in car_net_qty_tb[['id']].values:
				car_net_qty_df = car_net_qty_tb.loc[(car_net_qty_tb.id == stock_ratio_id)]
				type_car_df = car_net_qty_df.loc[(car_net_qty_df.type_car == stock_ratio_car)]

				if type_car_df.index.values.tolist() != [] and stock_ratio_data[8] != float(type_car_df['net_qty']):
					stock_ratio = stock_ratio.drop(df.index)

			# 代表這張車不僅有一個產品 & 不算開銷為0的商品
			elif id_count > 1 and stock_ratio_cost != 0:

				products_payment_per_car = []
				products_spending_per_car = []

				cements_spending_not_per_car = []

				cements_spending_per_car = []

				cements_index = []
				cements_id = []

				cements_payment = []
				cements_spending = []

				# 排查一張車-->進貨編
				for df_idx, df_data in df.iterrows():
					df_id = df_data[7]
					#             print(df_id)

					# 除水泥外的獨立商品
					if df_id in one_product_per_car[['id']].values and df_id not in cement[['id']].values:
						#                 print("one_product_per_car_not_cement")
						# 貨款
						product_payment = df.loc[df_idx, 's貨款']
						products_payment_per_car.append(product_payment)
						# 開銷
						product_spending = df.loc[df_idx, 's貨款'] * df.loc[df_idx, 'cost_ratio']
						products_spending_per_car.append(product_spending)
					# 不是獨立商品的水泥
					elif df_id not in one_product_per_car[['id']].values and df_id in cement[['id']].values:
						#                 print("cement_not_per_car")
						if stock_ratio_idx != df_idx:  # 不能是現在大循環到的id
							# 開銷
							cement_spending_not_per_car = df.loc[df_idx, 's貨款'] * df.loc[df_idx, 'cost_ratio']
							cements_spending_not_per_car.append(cement_spending_not_per_car)
					# 獨立水泥
					elif df_id in one_product_per_car[['id']].values:
						#                 print("cement_per_car")
						# 開銷
						cement_spending = df.loc[df_idx, 's貨款'] * df.loc[df_idx, 'cost_ratio']
						cements_spending_per_car.append(cement_spending)

					# 在這張車的水泥
					if df_id in cement[['id']].values:
						#                 print("cement")
						# 獲取水泥的index
						cements_index.append(df_idx)
						# 獲取水泥的id
						cement_id = df.loc[df_idx, 'id']
						cements_id.append(cement_id)
						# 獲取水泥的貨款
						cement_payment = df.loc[df_idx, 's貨款']
						cements_payment.append(cement_payment)
						# 獲取水泥的開銷
						cement_spending = df.loc[df_idx, 's貨款'] * df.loc[df_idx, 'cost_ratio']
						cements_spending.append(cement_spending)

				# 獲取現在循環的商品的id
				stock_ratio_id = stock_ratio.loc[stock_ratio_idx, 'id']

				# 現在循環的商品是水泥
				if stock_ratio_id in cements_id:
					# 該水泥存在在獨立商品，有獨立成本
					if stock_ratio_id in one_product_per_car[['id']].values:
						#                 print("in")

						cement_per_car_df = one_product_per_car.loc[one_product_per_car.id == stock_ratio_id]
						cement_price_per_car_df = cement_per_car_df.loc[cement_per_car_df.進價 == purchase_price]
						if len(cement_price_per_car_df) != 0:
							cement_cost_ratio = float(cement_price_per_car_df['cost_ratio'])
							stock_ratio.loc[stock_ratio_idx, 'cost_ratio'] = cement_cost_ratio

						else:
							# 平均
							cement_price_per_car_df = cement_per_car_df.groupby('id').agg(
								{'cost_ratio': 'mean'}).reset_index().round(4)
							cement_cost_ratio = float(cement_price_per_car_df['cost_ratio'])
							stock_ratio.loc[stock_ratio_idx, 'cost_ratio'] = cement_cost_ratio

						# 最後一條
					#                     cement_cost_ratio = float(cement_price_per_car_df.tail(1)['cost_ratio'])
					#                     stock_ratio.loc[stock_ratio_idx, 'cost_ratio'] = cement_cost_ratio

					# 該水泥不存在在獨立商品，需要計算
					else:
						#                 print("not in")

						# 除水泥之外的獨立商品 --> 獨立商品開銷相加(以防有兩個)
						sum_products_spending_per_car = np.sum(products_spending_per_car, axis=0)
						# 獨立水泥 --> 水泥開銷相加(以防有兩個)
						sum_cements_spending_per_car = np.sum(cements_spending_per_car, axis=0)
						# 不在獨立的水泥 --> 水泥開銷相加(以防有兩個)
						sum_cements_spending_not_per_car = np.sum(cements_spending_not_per_car, axis=0)
						# 以上三個相加
						both_spending = sum_products_spending_per_car + sum_cements_spending_per_car + sum_cements_spending_not_per_car

						df_groupby = df.groupby("進貨編").agg({'s貨款': 'sum'}).reset_index()  # 整車貨款

						# spending --> 整車所花的開銷或者支出
						spending = float(df_groupby['s貨款'] * stock_ratio.loc[stock_ratio_idx, 'cost_ratio'])

						# 目前循環到的水泥的開銷 --> 整車開銷減(獨立商品+獨立水泥開銷+不在獨立的水泥)
						this_cement_spending = spending - both_spending

						cement_cost_ratio = float(this_cement_spending / stock_ratio.loc[stock_ratio_idx, 's貨款'])

						stock_ratio.loc[stock_ratio_idx, 'cost_ratio'] = cement_cost_ratio
				#                 print(cement_cost_ratio)

				# 現在循環的商品是除水泥之外的商品-->除去水泥后計算其餘商品成本
				else:
					#             print("else")
					# 除水泥之外的獨立商品
					if stock_ratio_id in one_product_per_car[['id']].values:
						#                 print("in ---- one_product_per_car")

						product_per_car_df = one_product_per_car.loc[one_product_per_car.id == stock_ratio_id]
						product_price_per_car_df = product_per_car_df.loc[product_per_car_df.進價 == purchase_price]
						if len(product_price_per_car_df) != 0:
							product_cost_ratio = float(product_price_per_car_df['cost_ratio'])
							stock_ratio.loc[stock_ratio_idx, 'cost_ratio'] = product_cost_ratio

					# 除水泥之外的不是獨立商品的商品
					else:
						#                 print("not in ---- one_product_per_car")

						df_groupby = df.groupby("進貨編").agg({'s貨款': 'sum'}).reset_index()  # 整車貨款
						# spending --> 整車所花的開銷或者支出
						spending = float(df_groupby['s貨款'] * stock_ratio.loc[stock_ratio_idx, 'cost_ratio'])

						# 除水泥之外的獨立商品 --> 獨立商品開銷相加(以防有兩個)
						sum_products_spending_per_car = np.sum(products_spending_per_car, axis=0)
						# 水泥 --> 水泥開銷相加(以防有兩個)
						sum_cements_spending = np.sum(cements_spending, axis=0)
						both_spending = sum_products_spending_per_car + sum_cements_spending  # 以上兩個相加
						# 剩餘的開銷 --> 整車開銷減(除水泥外的獨立商品+全部水泥開銷)
						products_spending = spending - both_spending

						if spending > 0 and products_spending < 0:
							#                     print("stock_ratio = 0")
							stock_ratio.loc[stock_ratio_idx, 'cost_ratio'] = 0
						#                     print(product_cost_ratio)

						else:
							#                     print("正常")

							# 除水泥之外的獨立商品 --> 獨立商品貨款相加(以防有兩個)
							sum_products_payment_per_car = np.sum(products_payment_per_car, axis=0)
							# 水泥 --> 水泥貨款相加(以防有兩個)
							sum_cements_payment = np.sum(cements_payment, axis=0)
							both_payment = sum_products_payment_per_car + sum_cements_payment  # 以上兩個相加
							# 剩餘的貨款 --> 整車貨款減(除水泥外的獨立商品+全部水泥貨款)
							products_payment = df_groupby['s貨款'] - both_payment

							# 剩餘貨款的成本比例 --> 以金額為准來計算百分比
							product_cost_ratio = float(products_spending / products_payment)

							stock_ratio.loc[stock_ratio_idx, 'cost_ratio'] = product_cost_ratio

		stock_ratio = stock_ratio.sort_values(by='歸零日期', ascending=False)

		# 刪除多餘庫存的進貨筆數
		for stock_ratio_idx, stock_ratio_data in stock_ratio.iterrows():

			print(stock_ratio_idx)

			if stock_ratio_idx in stock_ratio.index:

				print("index exist")

				# 以id來區分循環數據
				df = stock_ratio.loc[(stock_ratio['id'] == stock_ratio_data[7])]  # 從0開始數的列位置
				# 循環到第几次 -->初始為0
				count = 0
				# 相加后的采購数量總和 -->初始為0
				purchase_qty = 0

				for df_idx, df_data in df.iterrows():

					count += 1
					# 采购数量相加
					purchase_qty += df_data[8]
					# 庫存
					stock = df_data[16]

					# 當循環到的進貨的數量大於庫存，刪除剩餘的數據，推出循環
					if purchase_qty >= stock:
						# 要刪除的數量
						drop_qty = len(df) - count
						index_drop_qty = df.tail(drop_qty).index
						# 刪除
						stock_ratio = stock_ratio.drop(index=index_drop_qty, axis=1)

						# 退出循環
						break

		# 刪除沒有庫存的商品
		stock_ratio = stock_ratio.drop(stock_ratio[stock_ratio['stock'].isnull()].index)
		print(len(stock_ratio))

		# 平均成本
		cost_ratio_mean = stock_ratio.groupby("id").agg(
			{'數量': 'sum', 'cost_ratio': 'mean', 'stock': 'mean'}).reset_index().round(4)

		# cost_ratio = inf 代表数据无效 --> 替換成 NaN --> 刪除
		cost_ratio_mean = cost_ratio_mean.replace([np.inf, -np.inf], np.nan).dropna(axis=0, subset=['cost_ratio'])

		# 计算当前时间 TimeZone
		tz = pytz.timezone('Asia/Yangon')  # 缅甸时间 TimeZone
		dt = datetime.datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M:%S %Z')  # .strftime('%Y-%m-%d %H:%M:%S %Z%z')
		print(dt)

		# 商品的最新價錢
		s_price_cost = pd.merge(cost_ratio_mean, last_s_df, how='outer', on='id', left_index=False,
								right_index=False, sort=True)
		s_price_cost['datetime'] = dt
		s_price_cost['s_price'] = s_price_cost['s_price'].fillna(0)  # NaN convert 0
		s_price_cost = s_price_cost[['id', 'datetime', 's_price', 'cost_ratio']]

		# 从数据库叫出 inventory_cost 表 最新商品價錢及成本
		# 为了获取当天最高cost_ratio的同時s_price也是最高價
		inventory_cost_tb = pd.read_sql("SELECT * from inventory_cost", con).sort_values(
			by=['cost_ratio', 's_price'], ascending=False)
		# 最新的成本
		inventory_cost_tb = inventory_cost_tb.loc[inventory_cost_tb.groupby(["id"])["datetime"].idxmax()]

		# 有更新的數據 --> 相比下s_price 和 cost_ratio不同的
		update_s_price_cost = (s_price_cost.merge(inventory_cost_tb, on=['id', 's_price', 'cost_ratio'],
								how='left', indicator=True).query('_merge == "left_only"')).drop(
								columns=['serial_id', 'datetime_y', 'price', 'subsidy', '_merge'])

		update_s_price_cost.rename(columns={'datetime_x': 'datetime'}, inplace=True)

		# 對比有更新的數據
		compared = pd.merge(update_s_price_cost, inventory_cost_tb[['id', 's_price', 'cost_ratio']], how='left',
							on='id', left_index=False, right_index=False, sort=True)
		compared['s_price_x'] = compared['s_price_x'].round(2)

		# 新數據
		new_data = compared.loc[compared['cost_ratio_y'].isnull()]  # NaN 新出來的不在原表的數據

		# 新的s_price
		s_price_dif = compared.loc[compared['s_price_x'] != compared['s_price_y']]  # s價錢和老價錢不一樣

		# cost_ratio漲跌>0.5%
		cost_ratio_dif = compared.loc[(compared.cost_ratio_x - compared.cost_ratio_y > 0.005) |  # 成本漲大於0.5%
									  (compared.cost_ratio_x - compared.cost_ratio_y < -0.005)  # 成本跌大於0.5%
									  ]

		# 合并 .drop_duplicates()去重
		cost_ratio_s_price_dif = pd.concat([new_data, s_price_dif, cost_ratio_dif]).drop_duplicates().drop(
									columns={'cost_ratio_y', 's_price_y'}).rename(
									columns={'cost_ratio_x': 'cost_ratio', 's_price_x': 's_price'})

		# 計算成本
		s_price = cost_ratio_s_price_dif['s_price']
		cost_ratio = cost_ratio_s_price_dif['cost_ratio']
		cost_ratio_s_price_dif['price'] = (s_price * cost_ratio) + s_price

		# Insert changed rows to psql --> cost table
		cost_ratio_s_price_dif.to_sql('inventory_cost', con=engine_price, if_exists='append', index=False)

		# # 从数据库叫出 inventory_cost 表
		# # 倒序排序 --> 为了获取s_price最高的同時cost_ratio最高價
		# new_inventory_cost_tb = pd.read_sql("SELECT * from inventory_cost", con).sort_values(
		# 						by=['s_price', 'cost_ratio'], ascending=False)
		# # 最新的進價及成本
		# new_data = new_inventory_cost_tb.loc[new_inventory_cost_tb.groupby(["id"])["datetime"].idxmax()]
		#
		# # DataFrame to json
		# B2002 = new_data.to_json(orient="records")
		# return B2002

		return jsonify("yohu")

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

		end_time_main = datetime.datetime.now()
		print((end_time_main - start_time_main))

