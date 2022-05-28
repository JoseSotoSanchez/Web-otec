from asyncio.windows_events import NULL
from flask import Flask, render_template, request, redirect, flash,url_for, session
from flask_paginate import Pagination, get_page_args ,get_page_parameter  
from flask_mysqldb import MySQL
from flask import Flask, request, render_template, jsonify, json
import pymysql
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
#local
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'otec'

#web
app.config['MYSQL_HOST'] = 'iccapacitacionlaboral.cl'
app.config['MYSQL_USER'] = 'iccapaci1_admin'
app.config['MYSQL_PASSWORD'] = 'gQ9Pb$$PKh'
app.config['MYSQL_DB'] = 'iccapaci1_iccaplab'

# Intialize MySQL
mysql = MySQL(app)
ROWS_PER_PAGE = 5
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
          # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE usuario = %s AND clave = %s', (usuario, clave,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['usuario'] = account['usuario']
            # Redirect to home page
            flash('Login correcto!', category='success')
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Usuario y/o contraseña incorrectas'
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
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
# @app.route('/home')
# def home():
#     # Check if user is loggedin
#     if 'loggedin' in session:
#         # User is loggedin show them the home page
#         return render_template('home.html', username=session['usuario'])
#     # User is not loggedin redirect to login page
#     return redirect(url_for('login'))
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/asistente-aula', methods=['GET', 'POST'])
def asistenteAula():
     # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'nombre' in request.form and 'apellido' in request.form and 'rut' in request.form and 'sexo' in request.form and 'edad' in request.form and 'nacionalidad' in request.form and 'ecivil' in request.form and 'email' in request.form and 'telefono' in request.form and 'profesion' in request.form and 'nestudios' in request.form and 'slaboral' in request.form and 'direccion' in request.form and 'region' in request.form and 'curso' in request.form:
    # Create variables for easy access
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        rut = request.form['rut']
        sexo = request.form['sexo']
        edad = request.form['edad']
        nacionalidad = request.form['nacionalidad']
        ecivil = request.form['ecivil']
        email = request.form['email']
        telefono = request.form['telefono']
        profesion = request.form['profesion']
        nestudios = request.form['nestudios']
        slaboral = request.form['slaboral']
        direccion = request.form['direccion']
        region = request.form['region']
        curso = request.form['curso']
          # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO curso_asistente_aula (nombre, apellido, rut, sexo, edad, nacionalidad, estado_civil, email, telefono, profesion, nivel_estudios, situacion_laboral, direccion, region, curso, fecha) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, now())', (nombre,apellido,rut,sexo,edad,nacionalidad,ecivil,email,telefono,profesion,nestudios,slaboral,direccion,region,curso,))
        # Fetch one record and return result
        curso = NULL
        mysql.connection.commit()
        msg = 'postulación exitosa!'
        #return render_template('contactanos.html', msg)
    return render_template('cursos/asistente-aula.html')

@app.route('/inspector-educacional', methods=['GET', 'POST'])
def inspectorEducacional():
     # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'nombre' in request.form and 'apellido' in request.form and 'rut' in request.form and 'sexo' in request.form and 'edad' in request.form and 'nacionalidad' in request.form and 'ecivil' in request.form and 'email' in request.form and 'telefono' in request.form and 'profesion' in request.form and 'nestudios' in request.form and 'slaboral' in request.form and 'direccion' in request.form and 'region' in request.form and 'curso' in request.form:
    # Create variables for easy access
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        rut = request.form['rut']
        sexo = request.form['sexo']
        edad = request.form['edad']
        nacionalidad = request.form['nacionalidad']
        ecivil = request.form['ecivil']
        email = request.form['email']
        telefono = request.form['telefono']
        profesion = request.form['profesion']
        nestudios = request.form['nestudios']
        slaboral = request.form['slaboral']
        direccion = request.form['direccion']
        region = request.form['region']
        curso = request.form['curso']
          # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO curso_inspector_educacional (nombre, apellido, rut, sexo, edad, nacionalidad, estado_civil, email, telefono, profesion, nivel_estudios, situacion_laboral, direccion, region, curso, fecha) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, now())', (nombre,apellido,rut,sexo,edad,nacionalidad,ecivil,email,telefono,profesion,nestudios,slaboral,direccion,region,curso,))
        # Fetch one record and return result
        mysql.connection.commit()
        msg = 'postulación exitosa!'
        #return render_template('contactanos.html', msg)
    return render_template('cursos/inspector-educacional.html')

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/contactanos', methods=['GET', 'POST'])
def contactanos():
     # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'nombre' in request.form and 'correo' in request.form and 'telefono' in request.form and 'motivo' in request.form and 'mensaje' in request.form:
    # Create variables for easy access
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']
        motivo = request.form['motivo']
        mensaje = request.form['mensaje']
          # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO contacto (nombre, correo, telefono, motivo, mensaje, fecha) VALUES (%s, %s, %s, %s, %s,now())', (nombre, correo,telefono,motivo,mensaje,))
        # Fetch one record and return result
        mysql.connection.commit()
        nombre = NULL
        msg = 'Mensaje enviado'
        #return render_template('contactanos.html', msg)
    return render_template('contactanos.html')

@app.route('/aspirantes-asistente-aula')
def aspirantesAula():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        page = int(request.args.get('page', 1))
        per_page = 5
        page = request.args.get(get_page_parameter(), type=int, default=1)
        offset = (page - 1) * per_page
        cursor.execute('SELECT * FROM curso_asistente_aula order by id desc')# WHERE id = %s', (session['id'],))
        aspirantes = cursor.fetchall() 
        pagination = Pagination(page=page, per_page=per_page, offset=offset, total=len(aspirantes), 
                    record_name='aspirantes')
        return render_template('administracion/aspirantes-asistente-aula.html', aspirantes = aspirantes, pagination = pagination) 
        # Show the profile page with account info
        return render_template('administracion/aspirantes-asistente-aula.html', username=session['usuario'])
    # User is not loggedin redirect to login page
    return redirect(url_for('home'))

@app.route('/aspirantes-inspector-educacional')
def aspirantesInspector():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        page = request.args.get('page', 1, type=int)
        cursor.execute('SELECT * FROM curso_inspector_educacional order by id desc')# WHERE id = %s', (session['id'],))
        aspirantes = cursor.fetchall() 
        return render_template('administracion/aspirantes-inspector-educacional.html', aspirantes = aspirantes)
    # User is not loggedin redirect to login page
    return redirect(url_for('home'))

@app.route('/mensajes-contacto')
def mensajesContacto():
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        page = int(request.args.get('page', 1))
        per_page = 5
        page = request.args.get(get_page_parameter(), type=int, default=1)
        offset = (page - 1) * per_page
        cursor.execute('SELECT * FROM contacto order by id desc')# WHERE id = %s', (session['id'],))
        mensajes = cursor.fetchall() 
        pagination = Pagination(page=page, per_page=per_page, offset=offset, total=len(mensajes), 
                    record_name='mensajes')
        return render_template('administracion/mensajes-contacto.html', mensajes = mensajes, pagination = pagination) 
    # User is not loggedin redirect to login page
    return redirect(url_for('home'))


# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuario WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(port = 3000, debug = True) 