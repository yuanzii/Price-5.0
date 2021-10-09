from flask import Blueprint

home = Blueprint('home',__name__)

# from user import login
from home import purchase_price
from home.Customer_Management import jia_yi_info_api_v1, jia_yi_info_api_v2, jia_yi_type_api_v1
from home.Product_Management import product_info_api_v1, product_category_api_v1, price_parameter_api
from home.api import cost_ratio_api_4_2