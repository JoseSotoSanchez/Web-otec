import pymysql

# def obtener_conexion():
#     return pymysql.connect(host="iccapacitacionlaboral.cl"
#     , user="iccapaci1_admin"
#     , password="gQ9Pb$$PKh", 
#     db="iccapaci1_iccaplabv2")

def obtener_conexion():
    return pymysql.connect(host="localhost"
    , user="root"
    , password="", 
    db="icaplab2")