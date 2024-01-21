from flask import Flask, render_template, request, redirect, flash,url_for, session,jsonify, json, Response
from flask_paginate import Pagination, get_page_args ,get_page_parameter  
from flask import Flask, request, render_template, jsonify, json
from bd import obtener_conexion
from correo import enviarEmail, upperFirst, enviarEmailAceptacion, obtenerMes, enviarEmailPago, enviarEmailBienvenida, enviarEmailBienvenidaIEMCE
from datetime import datetime
import csv
from io import StringIO
import locale



app = Flask(__name__)

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
#local
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'otec'

#web
#mydb = mysql.connector.connect(host="iccapacitacionlaboral.cl", user="iccapaci1_admin", passwd="gQ9Pb$$PKh", database="iccapaci1_iccaplab")

ROWS_PER_PAGE = 5
cursoActivo = 0
idAlumnoEstado = 0
idGlobal = 0
rutGlobal = ''
nombreGlobal = ''
estadoGlobal = 0
idAlumnoSearch = 0
# http://localhost:5000/pythonlogin/ - the following will be our login page, which will use both GET and POST requests
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'usuario' in request.form and 'clave' in request.form:
    # Create variables for easy access
        usuario = request.form['usuario']
        clave = request.form['clave']
        hostname = request.remote_addr
        IPAddr = request.environ['REMOTE_ADDR']
        hostnameAddr = hostname + " / "+IPAddr
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nick, nombre FROM Usuario WHERE nick = %s AND clave = %s", (usuario, clave,))
            account = cursor.fetchone()
        conexion.close()
        if account:
             #LOG login
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute('INSERT INTO LogUsuario (nick, clave, estado, fecha, ip) VALUES (%s, %s, "OK",now(), %s)', (usuario, clave, hostnameAddr,))
                conexion.commit()
            conexion.close()
            session['loggedin'] = True
            session['id'] = account[0]
            session['usuario'] = account[1]
            session['nombre'] = account[2]
            # Redirect to home page
            flash('Login correcto!', category='success')
            return redirect(url_for('index'))
        else:
            #LOG login
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute('INSERT INTO LogUsuario (nick, clave, estado, fecha, ip) VALUES (%s, %s, "Fallido", now(), %s)', (usuario, clave, hostnameAddr,))
                conexion.commit()
            conexion.close()
            flash('Usuario y/o contraseña incorrectas!', category='error')
    return render_template('login.html', msg='')

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('usuario', None)
   # Redirect to login page
   return redirect(url_for('login'))

   # http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'usuario' in request.form and 'usuario' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
         # Check if account exists using MySQL
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
            account = cursor.fetchone()
        conexion.close()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/privacidad')
def privacidad():
    return render_template('privacidad.html')

@app.route('/asistente-aula', methods=['GET', 'POST'])
def asistenteAula():
    if request.method == 'POST' and 'nombre' in request.form and 'apellido' in request.form and 'rut' in request.form and 'sexo' in request.form and 'edad' in request.form and 'nacionalidad' in request.form and 'ecivil' in request.form and 'email' in request.form and 'telefono' in request.form and 'profesion' in request.form and 'nestudios' in request.form and 'slaboral' in request.form and 'direccion' in request.form and 'region' in request.form and 'curso' in request.form and 'ingreso' in request.form:
        nombre = upperFirst(request.form['nombre'].lower())
        apellido = upperFirst(request.form['apellido'].lower())
        rut = request.form['rut']
        sexo = request.form['sexo']
        edad = request.form['edad']
        nacionalidad = request.form['nacionalidad']
        ecivil = request.form['ecivil']
        correo = request.form['email']
        telefono = request.form['telefono']
        profesion = request.form['profesion']
        nestudios = request.form['nestudios']
        slaboral = request.form['slaboral']
        direccion = request.form['direccion']
        region = request.form['region']
        curso = request.form['curso']
        ingreso = request.form['ingreso']
        hostname = request.remote_addr
        IPAddr = request.environ['REMOTE_ADDR']
        hostnameAddr = hostname + " / "+IPAddr
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno (nombre, apellido, rut, sexo, edad, nacionalidad, estado_civil, email, telefono, profesion, nivel_estudios, situacion_laboral, direccion, region, fecha, id_curso, id_subsidio, ingreso) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, now(), %s, 1, %s)', (nombre,apellido,rut,sexo,edad,nacionalidad,ecivil,correo,telefono,profesion,nestudios,slaboral,direccion,region,curso, ingreso))
            id = cursor.lastrowid
            cursor.execute('INSERT INTO Alumno_Estado(id_alumno, id_estado, fecha,id_usuario) VALUES (%s, 6, now(),1)', (id))
            cursor.execute('INSERT INTO LogUsuario (estado, fecha, ip, curso, idAlumno) VALUES ("postulación de curso",now(), %s, %s, %s)', (hostnameAddr,curso, id))
        conexion.commit()
        conexion.close()
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT c.id, c.nombre, c.codigo_curso, c.fecha_inicio, c.fecha_fin, h.rango, d.rango FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id WHERE c.id = %s', (curso))
            curso_ = cursor.fetchall()
        conexion.close()
        nombre = nombre + ' ' + apellido
        curso = curso_[0][1]
        mes = curso_[0][3].month
        nombreMes = obtenerMes(mes)
        mesFin = curso_[0][4].month
        nombreMesFin = obtenerMes(mesFin)
        enviarEmail(nombre, telefono, curso, correo, curso_[0][3].strftime("%d de "+nombreMes+" del %Y") , curso_[0][4].strftime("%d de "+nombreMesFin+" del %Y"), curso_[0][2], curso_[0][5], curso_[0][6])
        flash('Postulación enviada correctamente!', category='success')
    else:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT c.id, c.nombre, c.codigo_curso, h.rango, d.rango, c.fecha_inicio, c.fecha_fin FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id WHERE c.activo = 1 ORDER BY c.id DESC')# WHERE id = %s', (session['id'],))
            cursos = cursor.fetchall()
        conexion.close()
        return render_template('cursos/asistente-aula.html',
                            cursos=cursos,
                            )
    return redirect(url_for('index'))

@app.route('/inspector-educacional', methods=['GET', 'POST'])
def inspectorEducacional():
    if request.method == 'POST' and 'nombre' in request.form and 'apellido' in request.form and 'rut' in request.form and 'sexo' in request.form and 'edad' in request.form and 'nacionalidad' in request.form and 'ecivil' in request.form and 'email' in request.form and 'telefono' in request.form and 'profesion' in request.form and 'nestudios' in request.form and 'slaboral' in request.form and 'direccion' in request.form and 'region' in request.form and 'curso' in request.form and 'ingreso' in request.form:
        nombre = upperFirst(request.form['nombre'].lower())
        apellido = upperFirst(request.form['apellido'].lower())
        rut = request.form['rut']
        sexo = request.form['sexo']
        edad = request.form['edad']
        nacionalidad = request.form['nacionalidad']
        ecivil = request.form['ecivil']
        correo = request.form['email']
        telefono = request.form['telefono']
        profesion = request.form['profesion']
        nestudios = request.form['nestudios']
        slaboral = request.form['slaboral']
        direccion = request.form['direccion']
        region = request.form['region']
        curso = request.form['curso']
        ingreso = request.form['ingreso']
        hostname = request.remote_addr
        IPAddr = request.environ['REMOTE_ADDR']
        hostnameAddr = hostname + " / "+IPAddr
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno (nombre, apellido, rut, sexo, edad, nacionalidad, estado_civil, email, telefono, profesion, nivel_estudios, situacion_laboral, direccion, region, fecha, id_curso, id_subsidio, ingreso) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, now(), %s, 1, %s)', (nombre,apellido,rut,sexo,edad,nacionalidad,ecivil,correo,telefono,profesion,nestudios,slaboral,direccion,region,curso, ingreso))
            id = cursor.lastrowid
            cursor.execute('INSERT INTO Alumno_Estado(id_alumno, id_estado, fecha,id_usuario) VALUES (%s, 6, now(),1)', (id))
            cursor.execute('INSERT INTO LogUsuario (estado, fecha, ip, curso, idAlumno) VALUES ("postulación de curso",now(), %s, %s, %s)', (hostnameAddr,curso, id))
        conexion.commit()
        conexion.close()
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT c.id, c.nombre, c.codigo_curso, c.fecha_inicio, c.fecha_fin, h.rango, d.rango FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id WHERE c.id = %s', (curso))
            curso_ = cursor.fetchall()
        conexion.close()
        nombre = nombre + ' ' + apellido
        curso = curso_[0][1]
        mes = curso_[0][3].month
        nombreMes = obtenerMes(mes)
        mesFin = curso_[0][4].month
        nombreMesFin = obtenerMes(mesFin)
        enviarEmail(nombre, telefono, curso, correo, curso_[0][3].strftime("%d de "+nombreMes+" del %Y") , curso_[0][4].strftime("%d de "+nombreMesFin+" del %Y"), curso_[0][2], curso_[0][5], curso_[0][6])
        flash('Postulación enviada correctamente!', category='success')
    else:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT c.id, c.nombre, c.codigo_curso, h.rango, d.rango, c.fecha_inicio, c.fecha_fin FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id WHERE c.activo = 1 ORDER BY c.id DESC')
            cursos = cursor.fetchall()
        conexion.close()
        return render_template('cursos/inspector-educacional.html',
                            cursos=cursos,
                            )
    return redirect(url_for('index'))

@app.route('/asistente-administrativo-contable', methods=['GET', 'POST'])
def asistenteContable():
    if request.method == 'POST' and 'nombre' in request.form and 'apellido' in request.form and 'rut' in request.form and 'sexo' in request.form and 'edad' in request.form and 'nacionalidad' in request.form and 'ecivil' in request.form and 'email' in request.form and 'telefono' in request.form and 'profesion' in request.form and 'nestudios' in request.form and 'slaboral' in request.form and 'direccion' in request.form and 'region' in request.form and 'curso' in request.form and 'ingreso' in request.form:
        nombre = upperFirst(request.form['nombre'].lower())
        apellido = upperFirst(request.form['apellido'].lower())
        rut = request.form['rut']
        sexo = request.form['sexo']
        edad = request.form['edad']
        nacionalidad = request.form['nacionalidad']
        ecivil = request.form['ecivil']
        correo = request.form['email']
        telefono = request.form['telefono']
        profesion = request.form['profesion']
        nestudios = request.form['nestudios']
        slaboral = request.form['slaboral']
        direccion = request.form['direccion']
        region = request.form['region']
        curso = request.form['curso']
        ingreso = request.form['ingreso']
        hostname = request.remote_addr
        IPAddr = request.environ['REMOTE_ADDR']
        hostnameAddr = hostname + " / "+IPAddr
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno (nombre, apellido, rut, sexo, edad, nacionalidad, estado_civil, email, telefono, profesion, nivel_estudios, situacion_laboral, direccion, region, fecha, id_curso, id_subsidio, ingreso) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, now(), %s, 1, %s)', (nombre,apellido,rut,sexo,edad,nacionalidad,ecivil,correo,telefono,profesion,nestudios,slaboral,direccion,region,curso, ingreso))
            id = cursor.lastrowid
            cursor.execute('INSERT INTO Alumno_Estado(id_alumno, id_estado, fecha,id_usuario) VALUES (%s, 6, now(),1)', (id))
            cursor.execute('INSERT INTO LogUsuario (estado, fecha, ip, curso, idAlumno) VALUES ("postulación de curso",now(), %s, %s, %s)', (hostnameAddr,curso, id))
        conexion.commit()
        conexion.close()
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT c.id, c.nombre, c.codigo_curso, c.fecha_inicio, c.fecha_fin, h.rango, d.rango FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id WHERE c.id = %s', (curso))
            curso_ = cursor.fetchall()
        conexion.close()
        nombre = nombre + ' ' + apellido
        curso = curso_[0][1]
        mes = curso_[0][3].month
        nombreMes = obtenerMes(mes)
        mesFin = curso_[0][4].month
        nombreMesFin = obtenerMes(mesFin)
        enviarEmail(nombre, telefono, curso, correo, curso_[0][3].strftime("%d de "+nombreMes+" del %Y") , curso_[0][4].strftime("%d de "+nombreMesFin+" del %Y"), curso_[0][2], curso_[0][5], curso_[0][6])
        flash('Postulación enviada correctamente!', category='success')
    else:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT c.id, c.nombre, c.codigo_curso, h.rango, d.rango, c.fecha_inicio, c.fecha_fin FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id WHERE c.activo = 1 ORDER BY c.id DESC')
            cursos = cursor.fetchall()
        conexion.close()
        return render_template('cursos/asistente-administrativo-contable.html',
                            cursos=cursos,
                            )
    return redirect(url_for('index'))

@app.route('/cajero-bancario', methods=['GET', 'POST'])
def cajeroBancario():
    if request.method == 'POST' and 'nombre' in request.form and 'apellido' in request.form and 'rut' in request.form and 'sexo' in request.form and 'edad' in request.form and 'nacionalidad' in request.form and 'ecivil' in request.form and 'email' in request.form and 'telefono' in request.form and 'profesion' in request.form and 'nestudios' in request.form and 'slaboral' in request.form and 'direccion' in request.form and 'region' in request.form and 'curso' in request.form and 'ingreso' in request.form:
        nombre = upperFirst(request.form['nombre'].lower())
        apellido = upperFirst(request.form['apellido'].lower())
        rut = request.form['rut']
        sexo = request.form['sexo']
        edad = request.form['edad']
        nacionalidad = request.form['nacionalidad']
        ecivil = request.form['ecivil']
        correo = request.form['email']
        telefono = request.form['telefono']
        profesion = request.form['profesion']
        nestudios = request.form['nestudios']
        slaboral = request.form['slaboral']
        direccion = request.form['direccion']
        region = request.form['region']
        curso = request.form['curso']
        ingreso = request.form['ingreso']
        hostname = request.remote_addr
        IPAddr = request.environ['REMOTE_ADDR']
        hostnameAddr = hostname + " / "+IPAddr
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno (nombre, apellido, rut, sexo, edad, nacionalidad, estado_civil, email, telefono, profesion, nivel_estudios, situacion_laboral, direccion, region, fecha, id_curso, id_subsidio, ingreso) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, now(), %s, 1, %s)', (nombre,apellido,rut,sexo,edad,nacionalidad,ecivil,correo,telefono,profesion,nestudios,slaboral,direccion,region,curso, ingreso))
            id = cursor.lastrowid
            cursor.execute('INSERT INTO Alumno_Estado(id_alumno, id_estado, fecha,id_usuario) VALUES (%s, 6, now(),1)', (id))
            cursor.execute('INSERT INTO LogUsuario (estado, fecha, ip, curso, idAlumno) VALUES ("postulación de curso",now(), %s, %s, %s)', (hostnameAddr,curso, id))
        conexion.commit()
        conexion.close()
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT c.id, c.nombre, c.codigo_curso, c.fecha_inicio, c.fecha_fin, h.rango, d.rango FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id WHERE c.id = %s', (curso))
            curso_ = cursor.fetchall()
        conexion.close()
        nombre = nombre + ' ' + apellido
        curso = curso_[0][1]
        mes = curso_[0][3].month
        nombreMes = obtenerMes(mes)
        mesFin = curso_[0][4].month
        nombreMesFin = obtenerMes(mesFin)
        enviarEmail(nombre, telefono, curso, correo, curso_[0][3].strftime("%d de "+nombreMes+" del %Y") , curso_[0][4].strftime("%d de "+nombreMesFin+" del %Y"), curso_[0][2], curso_[0][5], curso_[0][6])
        flash('Postulación enviada correctamente!', category='success')
    else:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT c.id, c.nombre, c.codigo_curso, h.rango, d.rango, c.fecha_inicio, c.fecha_fin FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id WHERE c.activo = 1 ORDER BY c.id DESC')
            cursos = cursor.fetchall()
        conexion.close()
        return render_template('cursos/cajero-bancario.html',
                            cursos=cursos,
                            )
    return redirect(url_for('index'))

@app.route('/convivencia-escolar', methods=['GET', 'POST'])
def convivenciaEscolar():
    if request.method == 'POST' and 'nombre' in request.form and 'apellido' in request.form and 'rut' in request.form and 'sexo' in request.form and 'edad' in request.form and 'nacionalidad' in request.form and 'ecivil' in request.form and 'email' in request.form and 'telefono' in request.form and 'profesion' in request.form and 'nestudios' in request.form and 'slaboral' in request.form and 'direccion' in request.form and 'region' in request.form and 'curso' in request.form and 'ingreso' in request.form:
        nombre = upperFirst(request.form['nombre'].lower())
        apellido = upperFirst(request.form['apellido'].lower())
        rut = request.form['rut']
        sexo = request.form['sexo']
        edad = request.form['edad']
        nacionalidad = request.form['nacionalidad']
        ecivil = request.form['ecivil']
        correo = request.form['email']
        telefono = request.form['telefono']
        profesion = request.form['profesion']
        nestudios = request.form['nestudios']
        slaboral = request.form['slaboral']
        direccion = request.form['direccion']
        region = request.form['region']
        curso = request.form['curso']
        ingreso = request.form['ingreso']
        hostname = request.remote_addr
        IPAddr = request.environ['REMOTE_ADDR']
        hostnameAddr = hostname + " / "+IPAddr
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno (nombre, apellido, rut, sexo, edad, nacionalidad, estado_civil, email, telefono, profesion, nivel_estudios, situacion_laboral, direccion, region, fecha, id_curso, id_subsidio, ingreso) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, now(), %s, 1, %s)', (nombre,apellido,rut,sexo,edad,nacionalidad,ecivil,correo,telefono,profesion,nestudios,slaboral,direccion,region,curso, ingreso))
            id = cursor.lastrowid
            cursor.execute('INSERT INTO Alumno_Estado(id_alumno, id_estado, fecha,id_usuario) VALUES (%s, 6, now(),1)', (id))
            cursor.execute('INSERT INTO LogUsuario (estado, fecha, ip, curso, idAlumno) VALUES ("postulación de curso",now(), %s, %s, %s)', (hostnameAddr,curso, id))
        conexion.commit()
        conexion.close()
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT c.id, c.nombre, c.codigo_curso, c.fecha_inicio, c.fecha_fin, h.rango, d.rango FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id WHERE c.id = %s', (curso))
            curso_ = cursor.fetchall()
        conexion.close()
        nombre = nombre + ' ' + apellido
        curso = curso_[0][1]
        mes = curso_[0][3].month
        nombreMes = obtenerMes(mes)
        mesFin = curso_[0][4].month
        nombreMesFin = obtenerMes(mesFin)
        enviarEmail(nombre, telefono, curso, correo, curso_[0][3].strftime("%d de "+nombreMes+" del %Y") , curso_[0][4].strftime("%d de "+nombreMesFin+" del %Y"), curso_[0][2], curso_[0][5], curso_[0][6])
        flash('Postulación enviada correctamente!', category='success')
    else:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT c.id, c.nombre, c.codigo_curso, h.rango, d.rango, c.fecha_inicio, c.fecha_fin FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id WHERE c.activo = 1 ORDER BY c.id DESC')
            cursos = cursor.fetchall()
        conexion.close()
        return render_template('cursos/convivencia-escolar.html',
                            cursos=cursos,
                            )
    return redirect(url_for('index'))

@app.route('/tea', methods=['GET', 'POST'])
def tea():
    if request.method == 'POST' and 'nombre' in request.form and 'apellido' in request.form and 'rut' in request.form and 'sexo' in request.form and 'edad' in request.form and 'nacionalidad' in request.form and 'ecivil' in request.form and 'email' in request.form and 'telefono' in request.form and 'profesion' in request.form and 'nestudios' in request.form and 'slaboral' in request.form and 'direccion' in request.form and 'region' in request.form and 'curso' in request.form and 'ingreso' in request.form:
        nombre = upperFirst(request.form['nombre'].lower())
        apellido = upperFirst(request.form['apellido'].lower())
        rut = request.form['rut']
        sexo = request.form['sexo']
        edad = request.form['edad']
        nacionalidad = request.form['nacionalidad']
        ecivil = request.form['ecivil']
        correo = request.form['email']
        telefono = request.form['telefono']
        profesion = request.form['profesion']
        nestudios = request.form['nestudios']
        slaboral = request.form['slaboral']
        direccion = request.form['direccion']
        region = request.form['region']
        curso = request.form['curso']
        ingreso = request.form['ingreso']
        hostname = request.remote_addr
        IPAddr = request.environ['REMOTE_ADDR']
        hostnameAddr = hostname + " / "+IPAddr
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno (nombre, apellido, rut, sexo, edad, nacionalidad, estado_civil, email, telefono, profesion, nivel_estudios, situacion_laboral, direccion, region, fecha, id_curso, id_subsidio, ingreso) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, now(), %s, 1, %s)', (nombre,apellido,rut,sexo,edad,nacionalidad,ecivil,correo,telefono,profesion,nestudios,slaboral,direccion,region,curso, ingreso))
            id = cursor.lastrowid
            cursor.execute('INSERT INTO Alumno_Estado(id_alumno, id_estado, fecha,id_usuario) VALUES (%s, 6, now(),1)', (id))
            cursor.execute('INSERT INTO LogUsuario (estado, fecha, ip, curso, idAlumno) VALUES ("postulación de curso",now(), %s, %s, %s)', (hostnameAddr,curso, id))
        conexion.commit()
        conexion.close()
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT c.id, c.nombre, c.codigo_curso, c.fecha_inicio, c.fecha_fin, h.rango, d.rango FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id WHERE c.id = %s', (curso))
            curso_ = cursor.fetchall()
        conexion.close()
        nombre = nombre + ' ' + apellido
        curso = curso_[0][1]
        mes = curso_[0][3].month
        nombreMes = obtenerMes(mes)
        mesFin = curso_[0][4].month
        nombreMesFin = obtenerMes(mesFin)
        enviarEmail(nombre, telefono, curso, correo, curso_[0][3].strftime("%d de "+nombreMes+" del %Y") , curso_[0][4].strftime("%d de "+nombreMesFin+" del %Y"), curso_[0][2], curso_[0][5], curso_[0][6])
        flash('Postulación enviada correctamente!', category='success')
    else:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT c.id, c.nombre, c.codigo_curso, h.rango, d.rango, c.fecha_inicio, c.fecha_fin FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id WHERE c.activo = 1 ORDER BY c.id DESC')
            cursos = cursor.fetchall()
        conexion.close()
        return render_template('cursos/tea.html',
                            cursos=cursos,
                            )
    return redirect(url_for('index'))
    
@app.route('/rrhh', methods=['GET', 'POST'])
def rrhh():
    if request.method == 'POST' and 'nombre' in request.form and 'apellido' in request.form and 'rut' in request.form and 'sexo' in request.form and 'edad' in request.form and 'nacionalidad' in request.form and 'ecivil' in request.form and 'email' in request.form and 'telefono' in request.form and 'profesion' in request.form and 'nestudios' in request.form and 'slaboral' in request.form and 'direccion' in request.form and 'region' in request.form and 'curso' in request.form and 'ingreso' in request.form:
        nombre = upperFirst(request.form['nombre'].lower())
        apellido = upperFirst(request.form['apellido'].lower())
        rut = request.form['rut']
        sexo = request.form['sexo']
        edad = request.form['edad']
        nacionalidad = request.form['nacionalidad']
        ecivil = request.form['ecivil']
        correo = request.form['email']
        telefono = request.form['telefono']
        profesion = request.form['profesion']
        nestudios = request.form['nestudios']
        slaboral = request.form['slaboral']
        direccion = request.form['direccion']
        region = request.form['region']
        curso = request.form['curso']
        ingreso = request.form['ingreso']
        hostname = request.remote_addr
        IPAddr = request.environ['REMOTE_ADDR']
        hostnameAddr = hostname + " / "+IPAddr
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno (nombre, apellido, rut, sexo, edad, nacionalidad, estado_civil, email, telefono, profesion, nivel_estudios, situacion_laboral, direccion, region, fecha, id_curso, id_subsidio, ingreso) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, now(), %s, 1, %s)', (nombre,apellido,rut,sexo,edad,nacionalidad,ecivil,correo,telefono,profesion,nestudios,slaboral,direccion,region,curso, ingreso))
            id = cursor.lastrowid
            cursor.execute('INSERT INTO Alumno_Estado(id_alumno, id_estado, fecha,id_usuario) VALUES (%s, 6, now(),1)', (id))
            cursor.execute('INSERT INTO LogUsuario (estado, fecha, ip, curso, idAlumno) VALUES ("postulación de curso",now(), %s, %s, %s)', (hostnameAddr,curso, id))
        conexion.commit()
        conexion.close()
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT c.id, c.nombre, c.codigo_curso, c.fecha_inicio, c.fecha_fin, h.rango, d.rango FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id WHERE c.id = %s', (curso))
            curso_ = cursor.fetchall()
        conexion.close()
        nombre = nombre + ' ' + apellido
        curso = curso_[0][1]
        mes = curso_[0][3].month
        nombreMes = obtenerMes(mes)
        mesFin = curso_[0][4].month
        nombreMesFin = obtenerMes(mesFin)
        enviarEmail(nombre, telefono, curso, correo, curso_[0][3].strftime("%d de "+nombreMes+" del %Y") , curso_[0][4].strftime("%d de "+nombreMesFin+" del %Y"), curso_[0][2], curso_[0][5], curso_[0][6])
        flash('Postulación enviada correctamente!', category='success')
    else:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT c.id, c.nombre, c.codigo_curso, h.rango, d.rango, c.fecha_inicio, c.fecha_fin FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id WHERE c.activo = 1 ORDER BY c.id DESC')
            cursos = cursor.fetchall()
        conexion.close()
        return render_template('cursos/rrhh.html',
                            cursos=cursos,
                            )
    return redirect(url_for('index'))

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/contactanos', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST' and 'nombre' in request.form and 'correo' in request.form and 'telefono' in request.form and 'motivo' in request.form and 'mensaje' in request.form:
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']
        motivo = request.form['motivo']
        mensaje = request.form['mensaje']
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Contacto(nombre, correo, telefono, motivo, mensaje, fecha) VALUES (%s, %s, %s, %s, %s,now())', (nombre, correo,telefono,motivo,mensaje,))
        conexion.commit()
        conexion.close()
        flash('Mensaje enviado correctamente!', category='success')
        return redirect(url_for('index'))
    return render_template('contactanos.html')

@app.route('/aspirantes', methods=['GET', 'POST'])
def aspirantes():
    datosCurso = ''
    global cursoActivo
    if 'loggedin' in session:
        if request.method == 'POST' and 'curso' in request.form :
            curso = request.form['curso']
            selected=curso
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute('SELECT DISTINCT a.id, a.nombre, a.apellido, a.rut, a.sexo, a.edad, a.nacionalidad, a.estado_civil, a.email, a.telefono, a.profesion, a.nivel_estudios, a.situacion_laboral, a.direccion, a.region, a.fecha, c.nombre AS nombreCurso, c.codigo_curso, ea.estado, u.nick, ea.id ,c.costo, a.ingreso FROM Alumno_Estado ae JOIN Alumno a ON a.id = ae.id_alumno JOIN Curso c ON a.id_curso = c.id JOIN Estado_Alumno ea ON ae.id_estado = ea.id JOIN Usuario u ON ae.id_usuario = u.id WHERE ae.id_estado = (select de.id_estado AS Id FROM Alumno_Estado de WHERE id_alumno = ae.id_alumno order by de.fecha desc limit 1) AND c.id = %s order by a.id desc;', (curso))# WHERE id = %s', (session['id'],))
                aspirantes = cursor.fetchall()
                cursor.execute('SELECT id, nombre, codigo_curso FROM Curso order by id desc')# WHERE id = %s', (session['id'],))
                cursos = cursor.fetchall()
                cursor.execute('SELECT nombre, codigo_curso, id FROM Curso where id = %s', (curso))# WHERE id = %s', (session['id'],))
                datosCurso = cursor.fetchall()
                cursor.execute('SELECT id, estado FROM Estado_Alumno')# WHERE id = %s', (session['id'],))
                estados = cursor.fetchall()
                conexion.close()
                total = len(aspirantes)
                cursoActivo = curso
                return render_template('administracion/aspirantes.html',
                                aspirantes=aspirantes,
                                cursos=cursos,
                                datosCurso=datosCurso,
                                estados = estados,
                                selected = int(selected),
                                total = total,
                                )
        else:
            if cursoActivo != 0:
                selected=cursoActivo
                conexion = obtener_conexion()
                with conexion.cursor() as cursor:
                    cursor.execute('SELECT DISTINCT a.id, a.nombre, a.apellido, a.rut, a.sexo, a.edad, a.nacionalidad, a.estado_civil, a.email, a.telefono, a.profesion, a.nivel_estudios, a.situacion_laboral, a.direccion, a.region, a.fecha, c.nombre AS nombreCurso, c.codigo_curso, ea.estado, u.nick, ea.id ,c.costo FROM Alumno_Estado ae JOIN Alumno a ON a.id = ae.id_alumno JOIN Curso c ON a.id_curso = c.id JOIN Estado_Alumno ea ON ae.id_estado = ea.id JOIN Usuario u ON ae.id_usuario = u.id WHERE ae.id_estado = (select de.id_estado AS Id FROM Alumno_Estado de WHERE id_alumno = ae.id_alumno order by de.fecha desc limit 1) AND c.id = %s order by a.id desc;', (cursoActivo))# WHERE id = %s', (session['id'],))
                    aspirantes = cursor.fetchall()
                    cursor.execute('SELECT id, nombre, codigo_curso FROM Curso order by id desc')# WHERE id = %s', (session['id'],))
                    cursos = cursor.fetchall()
                    cursor.execute('SELECT nombre, codigo_curso, id FROM Curso where id = %s', (cursoActivo))# WHERE id = %s', (session['id'],))
                    datosCurso = cursor.fetchall()
                    cursor.execute('SELECT id, estado FROM Estado_Alumno')# WHERE id = %s', (session['id'],))
                    estados = cursor.fetchall()
                    conexion.close()
                    total = len(aspirantes)
                return render_template('administracion/aspirantes.html',
                                aspirantes=aspirantes,
                                cursos=cursos,
                                datosCurso=datosCurso,
                                estados = estados,
                                selected = int(selected),
                                total = total,
                                )
            else:
                aspirantes = []
                conexion = obtener_conexion()
                with conexion.cursor() as cursor:
                    cursor.execute('SELECT id, nombre, codigo_curso FROM Curso order by id desc')# WHERE id = %s', (session['id'],))
                    cursos = cursor.fetchall()
                    cursor.execute('SELECT id, estado FROM Estado_Alumno')# WHERE id = %s', (session['id'],))
                    estados = cursor.fetchall()
                    conexion.close()
                    total = len(aspirantes)
                return render_template('administracion/aspirantes.html',
                                aspirantes=aspirantes,
                                cursos=cursos,
                                datosCurso=datosCurso,
                                estados = estados,
                                selected = 0,
                                total = total,
                                )
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/busqueda', methods=['GET', 'POST'])
def busqueda():
    datosCurso = ''
    global idAlumnoSearch
    if 'loggedin' in session:
        if request.method == 'POST' and 'ide' in request.form :
            idalumno = request.form['ide']
            nombreAlumno = request.form['nombreSearch']
            rutAlumno = request.form['rutSearch']
            session['idAlSearch'] = idalumno
            if (idalumno is None or idalumno.strip() == '') and (nombreAlumno is None or nombreAlumno.strip() == '') and (rutAlumno is None or rutAlumno.strip() == ''):
                flash('Debe ingresar un parámetro de busqueda!', category='error')
                return redirect(url_for('busqueda'))
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                if idalumno is not None and idalumno.strip() != '':
                    cursor.execute('SELECT DISTINCT a.id, a.nombre, a.apellido, a.rut, a.sexo, a.edad, a.nacionalidad, a.estado_civil, a.email, a.telefono, a.profesion, a.nivel_estudios, a.situacion_laboral, a.direccion, a.region, a.fecha, c.nombre AS nombreCurso, c.codigo_curso, ea.estado, u.nick, ea.id ,c.costo, a.ingreso, c.id FROM Alumno_Estado ae JOIN Alumno a ON a.id = ae.id_alumno JOIN Curso c ON a.id_curso = c.id JOIN Estado_Alumno ea ON ae.id_estado = ea.id JOIN Usuario u ON ae.id_usuario = u.id WHERE ae.id_estado = (select de.id_estado AS Id FROM Alumno_Estado de WHERE id_alumno = ae.id_alumno order by de.fecha desc limit 1) AND a.id = %s order by a.id desc;', (idalumno))# WHERE id = %s', (session['id'],))
                if nombreAlumno is not None and nombreAlumno.strip() != '':
                    cursor.execute('SELECT DISTINCT a.id, a.nombre, a.apellido, a.rut, a.sexo, a.edad, a.nacionalidad, a.estado_civil, a.email, a.telefono, a.profesion, a.nivel_estudios, a.situacion_laboral, a.direccion, a.region, a.fecha, c.nombre AS nombreCurso, c.codigo_curso, ea.estado, u.nick, ea.id ,c.costo, a.ingreso, c.id FROM Alumno_Estado ae JOIN Alumno a ON a.id = ae.id_alumno JOIN Curso c ON a.id_curso = c.id JOIN Estado_Alumno ea ON ae.id_estado = ea.id JOIN Usuario u ON ae.id_usuario = u.id WHERE ae.id_estado = (select de.id_estado AS Id FROM Alumno_Estado de WHERE id_alumno = ae.id_alumno order by de.fecha desc limit 1) AND a.nombre LIKE %s OR a.apellido Like %s order by a.id desc;', ('%'+nombreAlumno+'%', '%'+nombreAlumno+'%'))# WHERE id = %s', (session['id'],))
                if rutAlumno is not None and rutAlumno.strip() != '':
                    cursor.execute('SELECT DISTINCT a.id, a.nombre, a.apellido, a.rut, a.sexo, a.edad, a.nacionalidad, a.estado_civil, a.email, a.telefono, a.profesion, a.nivel_estudios, a.situacion_laboral, a.direccion, a.region, a.fecha, c.nombre AS nombreCurso, c.codigo_curso, ea.estado, u.nick, ea.id ,c.costo, a.ingreso, c.id FROM Alumno_Estado ae JOIN Alumno a ON a.id = ae.id_alumno JOIN Curso c ON a.id_curso = c.id JOIN Estado_Alumno ea ON ae.id_estado = ea.id JOIN Usuario u ON ae.id_usuario = u.id WHERE ae.id_estado = (select de.id_estado AS Id FROM Alumno_Estado de WHERE id_alumno = ae.id_alumno order by de.fecha desc limit 1) AND a.rut LIKE %s order by a.id desc;', ('%'+rutAlumno+'%'))# WHERE id = %s', (session['id'],))
                aspirantes = cursor.fetchall()
                cursor.execute('SELECT id, nombre, codigo_curso FROM Curso order by id desc')# WHERE id = %s', (session['id'],))
                cursos = cursor.fetchall()
                cursor.execute('SELECT nombre, codigo_curso, id FROM Curso where id = %s', (aspirantes[0][23]))# WHERE id = %s', (session['id'],))
                datosCurso = cursor.fetchall()
                cursor.execute('SELECT id, estado FROM Estado_Alumno')# WHERE id = %s', (session['id'],))
                estados = cursor.fetchall()
                conexion.close()
                total = len(aspirantes)
                return render_template('administracion/busqueda.html',
                                aspirantesSearch=aspirantes,
                                cursos=cursos,
                                datosCurso=datosCurso,
                                estados = estados,
                                total = total,
                                )
        else:
            aspirantes = [] 
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute('SELECT DISTINCT a.id, a.nombre, a.apellido, a.rut, a.sexo, a.edad, a.nacionalidad, a.estado_civil, a.email, a.telefono, a.profesion, a.nivel_estudios, a.situacion_laboral, a.direccion, a.region, a.fecha, c.nombre AS nombreCurso, c.codigo_curso, ea.estado, u.nick, ea.id ,c.costo, a.ingreso, c.id FROM Alumno_Estado ae JOIN Alumno a ON a.id = ae.id_alumno JOIN Curso c ON a.id_curso = c.id JOIN Estado_Alumno ea ON ae.id_estado = ea.id JOIN Usuario u ON ae.id_usuario = u.id WHERE ae.id_estado = (select de.id_estado AS Id FROM Alumno_Estado de WHERE id_alumno = ae.id_alumno order by de.fecha desc limit 1) AND a.id = %s order by a.id desc;', (idAlumnoSearch))# WHERE id = %s', (session['id'],))
                aspirantes = cursor.fetchall()
                print('aspitantes')
                print(aspirantes)
                cursor.execute('SELECT id, nombre, codigo_curso FROM Curso order by id desc')# WHERE id = %s', (session['id'],))
                cursos = cursor.fetchall()
                cursor.execute('SELECT id, estado FROM Estado_Alumno')# WHERE id = %s', (session['id'],))
                estados = cursor.fetchall()
                conexion.close()
                total = len(aspirantes)
            return render_template('administracion/busqueda.html',
                            aspirantesSearch=aspirantes,
                            cursos=cursos,
                            datosCurso=datosCurso,
                            estados = estados,
                            total = total,
                            )
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/descargaCsv', methods=['GET', 'POST'])
def descargaCsv():
    global idAlumnoSearch
    global cursoActivo
    if 'loggedin' in session:
        if request.method == 'POST':
             # Lógica para obtener datos de MySQL
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute('SELECT DISTINCT a.id, a.nombre, a.apellido, a.rut, a.sexo, a.edad, a.nacionalidad, a.estado_civil, a.email, a.telefono, a.profesion, a.nivel_estudios, a.situacion_laboral, a.direccion, a.region, a.fecha, c.nombre AS nombreCurso, c.codigo_curso, ea.estado, u.nick, ea.id ,c.costo, a.ingreso, c.id FROM Alumno_Estado ae JOIN Alumno a ON a.id = ae.id_alumno JOIN Curso c ON a.id_curso = c.id JOIN Estado_Alumno ea ON ae.id_estado = ea.id JOIN Usuario u ON ae.id_usuario = u.id WHERE ae.id_estado = (select de.id_estado AS Id FROM Alumno_Estado de WHERE id_alumno = ae.id_alumno order by de.fecha desc limit 1) AND c.id = %s order by a.id desc;', (cursoActivo,))# WHERE id = %s', (session['id'],))
                aspirantes = cursor.fetchall()

            # Generar el archivo CSV
            csv_data = generar_csv(aspirantes)

            nombre_archivo = 'curso '+aspirantes[0][17]+'.csv'
            # Crear una respuesta con el contenido del CSV y encabezados adecuados
            response = Response(csv_data, content_type='text/csv')
            response.headers["Content-Disposition"] = "attachment; filename="+nombre_archivo

            return response
    return redirect(url_for('index'))

@app.route('/descargaCsvPagados', methods=['GET', 'POST'])
def descargaCsvPagados():
    global idAlumnoSearch
    global cursoActivo
    if 'loggedin' in session:
        if request.method == 'POST':
             # Lógica para obtener datos de MySQL
            nueva_lista_aspirantes = []
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute('SELECT DISTINCT a.rut, a.nombre, a.apellido, a.email, c.codigo_curso, a.id FROM Alumno_Estado ae JOIN Alumno a ON a.id = ae.id_alumno JOIN Curso c ON a.id_curso = c.id JOIN Estado_Alumno ea ON ae.id_estado = ea.id JOIN Usuario u ON ae.id_usuario = u.id WHERE ae.id_estado = (select de.id_estado AS Id FROM Alumno_Estado de WHERE id_alumno = ae.id_alumno order by de.fecha desc limit 1) AND c.id = %s AND ae.id_estado = %s order by a.id desc;', (cursoActivo, 18))# WHERE id = %s', (session['id'],))
                aspirantes = cursor.fetchall()
            
            # Generar el archivo CSV
            for aspirante in aspirantes:
                rut, nombre, apellido, email, codigo_curso, id = aspirante
                rut = limpiar_rut(rut.replace('.', '').replace('-', ''))
                passGen = rut[:4]+"#icL"
                nueva_fila = (rut, passGen, nombre, apellido, email, codigo_curso, 'CL','es_mx','América/Santiago',id)
                nueva_lista_aspirantes.append(nueva_fila)
            csv_data = generar_csv_pagados(nueva_lista_aspirantes)
            nombre_archivo = 'curso '+aspirantes[0][4]+'.csv'
            # Crear una respuesta con el contenido del CSV y encabezados adecuados
            response = Response(csv_data, content_type='text/csv')
            response.headers["Content-Disposition"] = "attachment; filename="+nombre_archivo

            return response
    return redirect(url_for('index'))

def generar_csv(data):
    # Usar el módulo csv de Python para convertir los datos a formato CSV
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Nombre', 'Apellido', 'Rut', 'Sexo', 'Edad', 'Nacionalidad', 'Estado Civil', 'Email', 'Telefono', 'Profesion', 'Nivel de Estudios', 'Situacion Laboral', 'Direccion', 'Region', 'Fecha', 'Nombre del Curso', 'Codigo del Curso', 'Estado del Alumno', 'Nick del Usuario', 'ID de Estado', 'Costo', 'Ingreso', 'ID de Curso'])
    writer.writerows(data)
    return output.getvalue()

def generar_csv_pagados(data):
    # Usar el módulo csv de Python para convertir los datos a formato CSV
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['username', 'password', 'firstname', 'lastname', 'email', 'course1', 'country', 'lang', 'timezone', 'idnumber'])
    writer.writerows(data)
    return output.getvalue()

def limpiar_rut(rut):
    # Eliminar puntos, guiones y el último carácter del RUT
    rut_limpio = rut[:-1]
    return rut_limpio

@app.route('/guardarEstado/<int:id>/<int:curso>', methods=['GET', 'POST'])
def guardarEstado(id, curso):
    if request.method == 'POST' and 'estado' in request.form and 'correoAlumno' in request.form and 'celularAlumno' in request.form and 'nombresAlumno' in request.form and 'apellidosAlumno' in request.form:
        idEstado = request.form['estado']
        correoAlumno = request.form['correoAlumno']
        celularAlumno = request.form['celularAlumno']
        nombresAlumno = request.form['nombresAlumno']
        apellidosAlumno = request.form['apellidosAlumno']
        idUser = session['id']
        selected=curso
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno_Estado(id_estado, id_alumno, fecha, id_usuario) VALUES (%s, %s, now(), %s)', (idEstado, id, idUser,))
            cursor.execute('UPDATE Alumno SET nombre = %s, apellido = %s, email = %s, telefono = %s WHERE id = %s', (nombresAlumno, apellidosAlumno, correoAlumno, celularAlumno,id,))
        conexion.commit()
        conexion.close()
        flash('Estado guardado correctamente!', category='success')
        global cursoActivo
        cursoActivo = curso
        return redirect(url_for('aspirantes'))
    return redirect(url_for('index'))



@app.route('/envioCorreoAceptacion/<int:id>/<int:curso>', methods=['GET', 'POST'])
def envioCorreoAceptacion(id, curso):
    locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')
    if request.method == 'POST':
        urlPago = request.form['urlPago']
        print(urlPago)
        idUser = session['id']
        selected=curso
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT DISTINCT a.nombre, a.apellido, a.email FROM Alumno a WHERE a.id = %s;', (id))# WHERE id = %s', (session['id'],))
            alumno = cursor.fetchall()
            cursor.execute('SELECT c.nombre, c.fecha_inicio, c.fecha_fin, c.modalidad, h.rango, d.rango, c.costo FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id where c.id = %s', (curso))# WHERE id = %s', (session['id'],))
            datosCurso = cursor.fetchall()
            cursor.execute('SELECT nombre, nick, correo, numero FROM Usuario WHERE id = %s', (idUser))# WHERE id = %s', (session['id'],))
            datosUsuario = cursor.fetchall()
        conexion.close()
        nombre = alumno[0][0] + ' ' + alumno[0][1]
        mes = datosCurso[0][1].month
        nombreMes = obtenerMes(mes)
        mesFin = datosCurso[0][2].month
        nombreMesFin = obtenerMes(mesFin)
        valorCurso = locale.format_string('%d', datosCurso[0][6], grouping=True)
        enviarEmailAceptacion(nombre, alumno[0][2], datosCurso[0][0], datosCurso[0][1].strftime("%d de "+nombreMes+" del %Y"), datosCurso[0][2].strftime("%d de "+nombreMesFin+" del %Y"), datosCurso[0][5], datosCurso[0][4], datosCurso[0][3], urlPago, datosUsuario[0][0], datosUsuario[0][2], datosUsuario[0][3], valorCurso)
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno_Estado(id_estado, id_alumno, fecha, id_usuario) VALUES (13, %s, now(), %s)', (id, idUser,))
        conexion.commit()
        conexion.close()
        flash('Correo enviado correctamente!', category='success')
        global cursoActivo
        cursoActivo = curso
        return redirect(url_for('aspirantes'))
    return redirect(url_for('index'))

@app.route('/envioCorreoBienvenidaIEMCE/<int:id>/<int:curso>', methods=['GET', 'POST'])
def envioCorreoBienvenidaIEMCE(id, curso):
    locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')
    if request.method == 'POST':
        linkSense = request.form['linkSense']
        print(linkSense)
        idUser = session['id']
        selected=curso
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT DISTINCT a.nombre, a.apellido, a.email FROM Alumno a WHERE a.id = %s;', (id))# WHERE id = %s', (session['id'],))
            alumno = cursor.fetchall()
            cursor.execute('SELECT c.nombre, c.fecha_inicio, c.fecha_fin, c.modalidad, h.rango, d.rango, c.costo FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id where c.id = %s', (curso))# WHERE id = %s', (session['id'],))
            datosCurso = cursor.fetchall()
            cursor.execute('SELECT nombre, nick, correo, numero FROM Usuario WHERE id = %s', (idUser))# WHERE id = %s', (session['id'],))
            datosUsuario = cursor.fetchall()
        conexion.close()
        nombre = alumno[0][0] + ' ' + alumno[0][1]
        mes = datosCurso[0][1].month
        nombreMes = obtenerMes(mes)
        mesFin = datosCurso[0][2].month
        valorCurso = locale.format_string('%d', datosCurso[0][6], grouping=True)
        nombreMesFin = obtenerMes(mesFin)
        enviarEmailBienvenidaIEMCE(nombre, alumno[0][2], datosCurso[0][0], datosCurso[0][1].strftime("%d de "+nombreMes+" del %Y"), datosCurso[0][2].strftime("%d de "+nombreMesFin+" del %Y"), datosCurso[0][5], datosCurso[0][4], datosCurso[0][3], linkSense, datosUsuario[0][0], datosUsuario[0][2], datosUsuario[0][3], valorCurso)
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno_Estado(id_estado, id_alumno, fecha, id_usuario) VALUES (14, %s, now(), %s)', (id, idUser,))
        conexion.commit()
        conexion.close()
        flash('Correo enviado correctamente!', category='success')
        global cursoActivo
        cursoActivo = curso
        return redirect(url_for('aspirantes'))
    return redirect(url_for('index'))

@app.route('/envioCorreoPago/<int:id>/<int:curso>', methods=['GET', 'POST'])
def envioCorreoPago(id, curso):
    if request.method == 'POST':
        medioPago = request.form['medioPago']
        idUser = session['id']
        selected=curso
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT DISTINCT a.nombre, a.apellido, a.email FROM Alumno a WHERE a.id = %s;', (id))# WHERE id = %s', (session['id'],))
            alumno = cursor.fetchall()
            cursor.execute('SELECT c.nombre, c.codigo_curso, c.costo FROM Curso c where c.id = %s', (curso))# WHERE id = %s', (session['id'],))
            datosCurso = cursor.fetchall()
            cursor.execute('SELECT nombre, nick, correo, numero FROM Usuario WHERE id = %s', (idUser))# WHERE id = %s', (session['id'],))
            datosUsuario = cursor.fetchall()
        conexion.close()
        nombre = alumno[0][0] + ' ' + alumno[0][1]
        enviarEmailPago(nombre, alumno[0][2], datosCurso[0][0], datosCurso[0][1], str(datosCurso[0][2]), medioPago, datosUsuario[0][0], datosUsuario[0][2], datosUsuario[0][3])
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno_Estado(id_estado, id_alumno, fecha, id_usuario) VALUES (18, %s, now(), %s)', (id, idUser,))
        conexion.commit()
        conexion.close()
        flash('Correo enviado correctamente!', category='success')
        global cursoActivo
        cursoActivo = curso
        return redirect(url_for('aspirantes'))
    return redirect(url_for('index'))

@app.route('/guardarEstadoSearch/<int:id>', methods=['GET', 'POST'])
def guardarEstadoSearch(id):
    if request.method == 'POST' and 'estado' in request.form and 'correoAlumno' in request.form and 'celularAlumno' in request.form and 'nombresAlumno' in request.form and 'apellidosAlumno' in request.form:
        idEstado = request.form['estado']
        correoAlumno = request.form['correoAlumno']
        celularAlumno = request.form['celularAlumno']
        nombresAlumno = request.form['nombresAlumno']
        apellidosAlumno = request.form['apellidosAlumno']
        idUser = session['id']
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno_Estado(id_estado, id_alumno, fecha, id_usuario) VALUES (%s, %s, now(), %s)', (idEstado, id, idUser,))
            cursor.execute('UPDATE Alumno SET nombre = %s, apellido = %s, email = %s, telefono = %s WHERE id = %s', (nombresAlumno, apellidosAlumno, correoAlumno, celularAlumno,id,))
        conexion.commit()
        conexion.close()
        flash('Estado guardado correctamente!', category='success')
        global idAlumnoSearch
        idAlumnoSearch = id
        return redirect(url_for('busqueda'))
    return redirect(url_for('index'))



@app.route('/envioCorreoAceptacionSearch/<int:id>/<int:curso>', methods=['GET', 'POST'])
def envioCorreoAceptacionSearch(id, curso):
    locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')
    if request.method == 'POST':
        urlPago = request.form['urlPago']
        print(urlPago)
        idUser = session['id']
        selected=curso
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT DISTINCT a.nombre, a.apellido, a.email FROM Alumno a WHERE a.id = %s;', (id))# WHERE id = %s', (session['id'],))
            alumno = cursor.fetchall()
            cursor.execute('SELECT c.nombre, c.fecha_inicio, c.fecha_fin, c.modalidad, h.rango, d.rango, c.costo FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id where c.id = %s', (curso))# WHERE id = %s', (session['id'],))
            datosCurso = cursor.fetchall()
            cursor.execute('SELECT nombre, nick, correo, numero FROM Usuario WHERE id = %s', (idUser))# WHERE id = %s', (session['id'],))
            datosUsuario = cursor.fetchall()
        conexion.close()
        nombre = alumno[0][0] + ' ' + alumno[0][1]
        mes = datosCurso[0][1].month
        nombreMes = obtenerMes(mes)
        mesFin = datosCurso[0][2].month
        nombreMesFin = obtenerMes(mesFin)
        valorCurso = locale.format_string('%d', datosCurso[0][6], grouping=True)
        enviarEmailAceptacion(nombre, alumno[0][2], datosCurso[0][0], datosCurso[0][1].strftime("%d de "+nombreMes+" del %Y"), datosCurso[0][2].strftime("%d de "+nombreMesFin+" del %Y"), datosCurso[0][5], datosCurso[0][4], datosCurso[0][3], urlPago, datosUsuario[0][0], datosUsuario[0][2], datosUsuario[0][3], valorCurso)
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno_Estado(id_estado, id_alumno, fecha, id_usuario) VALUES (13, %s, now(), %s)', (id, idUser,))
        conexion.commit()
        conexion.close()
        flash('Correo enviado correctamente!', category='success')
        global cursoActivo
        cursoActivo = curso
        global idAlumnoSearch
        idAlumnoSearch = id
        return redirect(url_for('busqueda'))
    return redirect(url_for('index'))

@app.route('/envioCorreoBienvenidaIEMCESearch/<int:id>/<int:curso>', methods=['GET', 'POST'])
def envioCorreoBienvenidaIEMCESearch(id, curso):
    locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')
    if request.method == 'POST':
        linkSense = request.form['linkSense']
        print(linkSense)
        idUser = session['id']
        selected=curso
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT DISTINCT a.nombre, a.apellido, a.email FROM Alumno a WHERE a.id = %s;', (id))# WHERE id = %s', (session['id'],))
            alumno = cursor.fetchall()
            cursor.execute('SELECT c.nombre, c.fecha_inicio, c.fecha_fin, c.modalidad, h.rango, d.rango, c.costo FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id where c.id = %s', (curso))# WHERE id = %s', (session['id'],))
            datosCurso = cursor.fetchall()
            cursor.execute('SELECT nombre, nick, correo, numero FROM Usuario WHERE id = %s', (idUser))# WHERE id = %s', (session['id'],))
            datosUsuario = cursor.fetchall()
        conexion.close()
        nombre = alumno[0][0] + ' ' + alumno[0][1]
        mes = datosCurso[0][1].month
        nombreMes = obtenerMes(mes)
        mesFin = datosCurso[0][2].month
        valorCurso = locale.format_string('%d', datosCurso[0][6], grouping=True)
        nombreMesFin = obtenerMes(mesFin)
        enviarEmailBienvenidaIEMCE(nombre, alumno[0][2], datosCurso[0][0], datosCurso[0][1].strftime("%d de "+nombreMes+" del %Y"), datosCurso[0][2].strftime("%d de "+nombreMesFin+" del %Y"), datosCurso[0][5], datosCurso[0][4], datosCurso[0][3], linkSense, datosUsuario[0][0], datosUsuario[0][2], datosUsuario[0][3], valorCurso)
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno_Estado(id_estado, id_alumno, fecha, id_usuario) VALUES (14, %s, now(), %s)', (id, idUser,))
        conexion.commit()
        conexion.close()
        flash('Correo enviado correctamente!', category='success')
        global cursoActivo
        cursoActivo = curso
        global idAlumnoSearch
        idAlumnoSearch = id
        return redirect(url_for('busqueda'))
    return redirect(url_for('index'))

@app.route('/envioCorreoPagoSearch/<int:id>/<int:curso>', methods=['GET', 'POST'])
def envioCorreoPagoSearch(id, curso):
    if request.method == 'POST':
        medioPago = request.form['medioPago']
        idUser = session['id']
        selected=curso
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT DISTINCT a.nombre, a.apellido, a.email FROM Alumno a WHERE a.id = %s;', (id))# WHERE id = %s', (session['id'],))
            alumno = cursor.fetchall()
            cursor.execute('SELECT c.nombre, c.codigo_curso, c.costo FROM Curso c where c.id = %s', (curso))# WHERE id = %s', (session['id'],))
            datosCurso = cursor.fetchall()
            cursor.execute('SELECT nombre, nick, correo, numero FROM Usuario WHERE id = %s', (idUser))# WHERE id = %s', (session['id'],))
            datosUsuario = cursor.fetchall()
        conexion.close()
        nombre = alumno[0][0] + ' ' + alumno[0][1]
        enviarEmailPago(nombre, alumno[0][2], datosCurso[0][0], datosCurso[0][1], str(datosCurso[0][2]), medioPago, datosUsuario[0][0], datosUsuario[0][2], datosUsuario[0][3])
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno_Estado(id_estado, id_alumno, fecha, id_usuario) VALUES (18, %s, now(), %s)', (id, idUser,))
        conexion.commit()
        conexion.close()
        flash('Correo enviado correctamente!', category='success')
        global cursoActivo
        cursoActivo = curso
        global idAlumnoSearch
        idAlumnoSearch = id
        return redirect(url_for('busqueda'))
    return redirect(url_for('index'))

@app.route('/cursos', methods=['GET', 'POST'])
def cursos():
    if 'loggedin' in session:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT *, h.rango, d.rango, DATEDIFF(c.fecha_inicio, now()) AS Diferencia, date_format(c.fecha_inicio, "%d-%m-%Y") AS fechaInicio, date_format(c.fecha_fin, "%d-%m-%Y") AS fechaFin FROM Curso c JOIN Horario h ON h.id = c.id_horario JOIN Dias d ON d.id = c.id_dias order by c.id desc')# WHERE id = %s', (session['id'],))
            cursos = cursor.fetchall()
            cursor.execute('SELECT * FROM Horario order by id desc')# WHERE id = %s', (session['id'],))
            horario = cursor.fetchall()
            cursor.execute('SELECT * FROM Dias order by id desc')# WHERE id = %s', (session['id'],))
            dias = cursor.fetchall()
        conexion.close()
        return render_template('administracion/cursos.html',
                            cursos=cursos,
                            horario=horario,
                            dias=dias,
                            )
    return redirect(url_for('index'))

@app.route('/actualizarEstadoCurso/<int:id>', methods=['GET', 'POST'])
def actualizarEstadoCurso(id):
    if request.method == 'POST' and 'idValor' in request.form:
        idValor = request.form['idValor']
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('UPDATE Curso SET activo = %s WHERE id = %s', (idValor, id,))
        conexion.commit()
        conexion.close()
        flash('Actualizado correctamente!', category='success')
        return redirect(url_for('cursos'))
    return redirect(url_for('index'))

@app.route('/enviarCorreoBienvenida', methods=['GET', 'POST'])
def enviarCorreoBienvenida():
    if request.method == 'POST' and 'idCurso' in request.form and 'nombreCurso' in request.form and 'inicioCurso' in request.form and 'horarioCurso' in request.form and 'urlZoom' in request.form and 'idReunionZoom' in request.form and 'codigoAccesoZoom' in request.form and 'nombreProfesor' in request.form:
        idCurso = request.form['idCurso']
        urlZoom = request.form['urlZoom']
        nombreCurso = request.form['nombreCurso']
        inicioCurso = request.form['inicioCurso']
        horarioCurso = request.form['horarioCurso']
        idReunionZoom = request.form['idReunionZoom']
        codigoAccesoZoom = request.form['codigoAccesoZoom']
        nombreProfesor = request.form['nombreProfesor']
        idUser = session['id']
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT DISTINCT a.id, a.nombre, a.apellido, a.email FROM Alumno_Estado ae JOIN Alumno a ON a.id = ae.id_alumno JOIN Curso c ON a.id_curso = c.id WHERE ae.id_estado = (select de.id_estado AS Id FROM Alumno_Estado de WHERE id_alumno = ae.id_alumno order by de.fecha desc limit 1) AND c.id = %s AND ae.id_estado = 18 order by a.id desc', (idCurso))# WHERE id = %s', (session['id'],))
            alumnosPagados = cursor.fetchall()
            cursor.execute('SELECT nombre, nick, correo, numero FROM Usuario WHERE id = %s', (idUser))# WHERE id = %s', (session['id'],))
            datosUsuario = cursor.fetchall()
        conexion.close()
        for x in alumnosPagados:
            nombreAlumno = x[1] + ' ' + x[2]
            enviarEmailBienvenida(nombreAlumno, x[3], nombreCurso, urlZoom, idReunionZoom, codigoAccesoZoom, inicioCurso, nombreProfesor, horarioCurso, datosUsuario[0][0], datosUsuario[0][2], datosUsuario[0][3])
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute('INSERT INTO Alumno_Estado(id_alumno, id_estado, fecha,id_usuario) VALUES (%s, 19, now(), 1)', (x[0]))
            conexion.commit()   
            conexion.close()
        flash('Actualizado correctamente!', category='success')
        return redirect(url_for('cursos'))
    return redirect(url_for('index'))

@app.route('/agregarCurso', methods=['GET', 'POST'])
def agregarCurso():
    if request.method == 'POST' and 'nombre' in request.form and 'codigo' in request.form and 'fechaInicio' in request.form and 'fechaFin' in request.form and 'dias' in request.form  and 'horario' in request.form and 'costo' in request.form and 'modalidad' in request.form :
        nombre = request.form['nombre']
        codigo = request.form['codigo']
        fechaInicio = request.form['fechaInicio']
        fechaFin = request.form['fechaFin']
        dias = request.form['dias']
        horario = request.form['horario']
        costo = request.form['costo']
        modalidad = request.form['modalidad']
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Curso(nombre, codigo_curso, fecha_inicio, fecha_fin, id_dias, id_horario, costo, activo, modalidad) VALUES (%s, %s, %s, %s, %s, %s, %s, 1, %s)', (nombre, codigo, fechaInicio, fechaFin, dias, horario, costo, modalidad,))
        conexion.commit()
        conexion.close()
        flash('Agregado correctamente!', category='success')
        return redirect(url_for('cursos'))
    return redirect(url_for('index'))

@app.route('/aspirantes-asistente-aula', methods=['GET', 'POST'])
def aspirantesAula():
    if 'loggedin' in session:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT * FROM Alumno where id_curso = 1 order by id desc')# WHERE id = %s', (session['id'],))
            aspirantes = cursor.fetchall()
        conexion.close()
        page, per_page, offset = get_page_args(page_parameter='page',
                                        per_page_parameter='per_page')
        total = len(aspirantes)
        pagination_aspirantes = get_aspirantes(offset=offset, per_page=per_page, aspirantes=aspirantes)
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap4')
        return render_template('administracion/aspirantes-asistente-aula.html',
                            aspirantes=pagination_aspirantes,
                            page=page,
                            per_page=10,
                            pagination=pagination,
                            )
    return redirect(url_for('index'))

@app.route('/aspirantes-inspector-educacional')
def aspirantesInspector():
    if 'loggedin' in session:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT * FROM curso_inspector_educacional order by id desc')
            aspirantes = cursor.fetchall()
        conexion.close()
        page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
        total = len(aspirantes)
        pagination_aspirantes = get_aspirantes(offset=offset, per_page=per_page, aspirantes=aspirantes)
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap4')
        return render_template('administracion/aspirantes-inspector-educacional.html',
                            aspirantes=pagination_aspirantes,
                            page=page,
                            per_page=10,
                            pagination=pagination,
                            )
    return redirect(url_for('index'))

@app.route('/aspirantes-cajero-bancario')
def aspirantesCajeroBancario():
    # Check if user is loggedin
    if 'loggedin' in session:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT * FROM curso_cajero_bancario order by id desc')
            aspirantes = cursor.fetchall()
        conexion.close()
        page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
        total = len(aspirantes)
        pagination_aspirantes = get_aspirantes(offset=offset, per_page=per_page, aspirantes=aspirantes)
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap4')
        return render_template('administracion/aspirantes-cajero-bancario.html',
                            aspirantes=pagination_aspirantes,
                            page=page,
                            per_page=10,
                            pagination=pagination,
                            )
    return redirect(url_for('index'))

@app.route('/aspirantes-asistente-contable')
def aspirantesAsistenteContable():
    if 'loggedin' in session:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT * FROM curso_asistente_contable order by id desc')
            aspirantes = cursor.fetchall()
        conexion.close()
        page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
        total = len(aspirantes)
        pagination_aspirantes = get_aspirantes(offset=offset, per_page=per_page, aspirantes=aspirantes)
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap4')
        return render_template('administracion/aspirantes-asistente-contable.html',
                            aspirantes=pagination_aspirantes,
                            page=page,
                            per_page=10,
                            pagination=pagination,
                            )
    return redirect(url_for('index'))

@app.route('/mensajes-contacto')
def mensajesContacto():
    # Check if user is loggedin
    if 'loggedin' in session:
        mensajes = []
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM Contacto order by id desc")# WHERE id = %s', (session['id'],))
            mensajes = cursor.fetchall()
        conexion.close()
        page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
        total = len(mensajes)
        pagination_mensajes = get_mensajes(offset=offset, per_page=per_page, mensajes=mensajes)
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap4')
        return render_template('administracion/mensajes-contacto.html',
                            mensajes=pagination_mensajes,
                            page=page,
                            per_page=10,
                            pagination=pagination,
                            )
    return redirect(url_for('index'))

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:

        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT * FROM Usuario WHERE id = %s', (session['id'],))
            account = cursor.fetchone()
        conexion.close()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

def get_aspirantes(offset=0, per_page=100, aspirantes=[]):
    return aspirantes[offset: offset + per_page]

def get_mensajes(offset=0, per_page=100, mensajes=[]):
    return mensajes[offset: offset + per_page]

if __name__ == '__main__':
    app.run(port = 3000, debug = True) 