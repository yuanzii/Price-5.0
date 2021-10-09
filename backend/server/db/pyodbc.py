import pyodbc
import platform
server = '192.168.1.202'
database = '簡程序'
username = 'sa'
password = '123041316'

# PORT :1433
if platform.system() == 'Windows':
    con_185_CF內配 = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    con_185_CF內配_cursor = con_185_CF內配.cursor()
    print("1")

else:
    con_185_CF內配 = pyodbc.connect('DRIVER=/usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so;SERVER='+ server +';PORT=1433;DATABASE='+ database +';UID='+ username +';PWD='+ password +';TDS_VERSION=7.0')
    con_185_CF內配_cursor = con_185_CF內配.cursor()
    print("2")

# con_204_收發.close()