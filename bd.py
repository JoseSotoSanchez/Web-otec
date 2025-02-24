import pymysql

#PRD
# def obtener_conexion():
#     return pymysql.connect(host="iccapacitacionlaboral.cl"
#     , user="iccapaci1_admin"
#     , password="gQ9Pb$$PKh", 
#     db="ccapaci1_iccaplabv2")

#QA
# def obtener_conexion():
#     return pymysql.connect(host="iccapacitacionlaboral.cl"
#     , user="iccapaci1_admin"
#     , password="gQ9Pb$$PKh", 
#     db="iccapaci1_iccaplabv2_QA")

def obtener_conexion():
   return pymysql.connect(host="127.0.0.1"
   , user="root"
   , password="", 
   db="iccapaci1_iccaplabv2",
   port=3307 )