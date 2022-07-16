from flask import Flask, render_template, request, redirect, flash,url_for, session,jsonify, json
from flask_paginate import Pagination, get_page_args ,get_page_parameter  
from flask import Flask, request, render_template, jsonify, json
from bd import obtener_conexion
from correo import enviarEmail, upperFirst



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
#mydb = mysql.connector.connect(host="iccapacitacionlaboral.cl", user="iccapaci1_admin", passwd="gQ9Pb$$PKh", database="iccapaci1_iccaplab")

ROWS_PER_PAGE = 5
cursoActivo = 0
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
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nick, nombre FROM usuario WHERE nick = %s AND clave = %s", (usuario, clave,))
            account = cursor.fetchone()
        conexion.close()
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]
            session['usuario'] = account[1]
            session['nombre'] = account[2]
            # Redirect to home page
            flash('Login correcto!', category='success')
            return redirect(url_for('index'))
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
    if request.method == 'POST' and 'nombre' in request.form and 'apellido' in request.form and 'rut' in request.form and 'sexo' in request.form and 'edad' in request.form and 'nacionalidad' in request.form and 'ecivil' in request.form and 'email' in request.form and 'telefono' in request.form and 'profesion' in request.form and 'nestudios' in request.form and 'slaboral' in request.form and 'direccion' in request.form and 'region' in request.form and 'curso' in request.form:
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
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno (nombre, apellido, rut, sexo, edad, nacionalidad, estado_civil, email, telefono, profesion, nivel_estudios, situacion_laboral, direccion, region, fecha, id_curso, id_subsidio) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, now(), %s, 1)', (nombre,apellido,rut,sexo,edad,nacionalidad,ecivil,correo,telefono,profesion,nestudios,slaboral,direccion,region,curso))
            id = cursor.lastrowid
            cursor.execute('INSERT INTO alumno_estado(id_alumno, id_estado, fecha,id_usuario) VALUES (%s, 1, now(),1)', (id))
        conexion.commit()
        conexion.close()
        nombre = nombre + ' ' + apellido
        enviarEmail(nombre, telefono, curso, correo)
        flash('Postulación enviada correctamente!', category='success')
    else:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT id, nombre, codigo_curso FROM curso WHERE activo = 1')# WHERE id = %s', (session['id'],))
            cursos = cursor.fetchall()
        conexion.close()
        return render_template('cursos/asistente-aula.html',
                            cursos=cursos,
                            )
    return redirect(url_for('home'))

@app.route('/inspector-educacional', methods=['GET', 'POST'])
def inspectorEducacional():
    if request.method == 'POST' and 'nombre' in request.form and 'apellido' in request.form and 'rut' in request.form and 'sexo' in request.form and 'edad' in request.form and 'nacionalidad' in request.form and 'ecivil' in request.form and 'email' in request.form and 'telefono' in request.form and 'profesion' in request.form and 'nestudios' in request.form and 'slaboral' in request.form and 'direccion' in request.form and 'region' in request.form and 'curso' in request.form:
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
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno (nombre, apellido, rut, sexo, edad, nacionalidad, estado_civil, email, telefono, profesion, nivel_estudios, situacion_laboral, direccion, region, fecha, id_curso, id_subsidio) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, now(), %s, 1)', (nombre,apellido,rut,sexo,edad,nacionalidad,ecivil,correo,telefono,profesion,nestudios,slaboral,direccion,region,curso))
            id = cursor.lastrowid
            cursor.execute('INSERT INTO alumno_estado(id_alumno, id_estado, fecha,id_usuario) VALUES (%s, 1, now(),1)', (id))
        conexion.commit()
        conexion.close()
        nombre = nombre + ' ' + apellido
        enviarEmail(nombre, telefono, curso, correo)
        flash('Postulación enviada correctamente!', category='success')
    else:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT id, nombre, codigo_curso FROM curso WHERE activo = 1')# WHERE id = %s', (session['id'],))
            cursos = cursor.fetchall()
        conexion.close()
        return render_template('cursos/inspector-educacional.html',
                            cursos=cursos,
                            )
    return redirect(url_for('home'))

@app.route('/asistente-administrativo-contable', methods=['GET', 'POST'])
def asistenteContable():
    if request.method == 'POST' and 'nombre' in request.form and 'apellido' in request.form and 'rut' in request.form and 'sexo' in request.form and 'edad' in request.form and 'nacionalidad' in request.form and 'ecivil' in request.form and 'email' in request.form and 'telefono' in request.form and 'profesion' in request.form and 'nestudios' in request.form and 'slaboral' in request.form and 'direccion' in request.form and 'region' in request.form and 'curso' in request.form:
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
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno (nombre, apellido, rut, sexo, edad, nacionalidad, estado_civil, email, telefono, profesion, nivel_estudios, situacion_laboral, direccion, region, fecha, id_curso, id_subsidio) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, now(), %s, 1)', (nombre,apellido,rut,sexo,edad,nacionalidad,ecivil,correo,telefono,profesion,nestudios,slaboral,direccion,region,curso))
            id = cursor.lastrowid
            cursor.execute('INSERT INTO alumno_estado(id_alumno, id_estado, fecha,id_usuario) VALUES (%s, 1, now(),1)', (id))
        conexion.commit()
        conexion.close()
        nombre = nombre + ' ' + apellido
        enviarEmail(nombre, telefono, curso, correo)
        flash('Postulación enviada correctamente!', category='success')
    else:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT id, nombre, codigo_curso FROM curso WHERE activo = 1')# WHERE id = %s', (session['id'],))
            cursos = cursor.fetchall()
        conexion.close()
        return render_template('cursos/asistente-administrativo-contable.html',
                            cursos=cursos,
                            )
    return redirect(url_for('home'))

@app.route('/cajero-bancario', methods=['GET', 'POST'])
def cajeroBancario():
    if request.method == 'POST' and 'nombre' in request.form and 'apellido' in request.form and 'rut' in request.form and 'sexo' in request.form and 'edad' in request.form and 'nacionalidad' in request.form and 'ecivil' in request.form and 'email' in request.form and 'telefono' in request.form and 'profesion' in request.form and 'nestudios' in request.form and 'slaboral' in request.form and 'direccion' in request.form and 'region' in request.form and 'curso' in request.form:
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
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno (nombre, apellido, rut, sexo, edad, nacionalidad, estado_civil, email, telefono, profesion, nivel_estudios, situacion_laboral, direccion, region, fecha, id_curso, id_subsidio) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, now(), %s, 1)', (nombre,apellido,rut,sexo,edad,nacionalidad,ecivil,correo,telefono,profesion,nestudios,slaboral,direccion,region,curso))
            id = cursor.lastrowid
            cursor.execute('INSERT INTO alumno_estado(id_alumno, id_estado, fecha,id_usuario) VALUES (%s, 1, now(),1)', (id))
        conexion.commit()
        conexion.close()
        nombre = nombre + ' ' + apellido
        enviarEmail(nombre, telefono, curso, correo)
        flash('Postulación enviada correctamente!', category='success')
    else:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT id, nombre, codigo_curso FROM curso WHERE activo = 1')# WHERE id = %s', (session['id'],))
            cursos = cursor.fetchall()
        conexion.close()
        return render_template('cursos/cajero-bancario.html',
                            cursos=cursos,
                            )
    return redirect(url_for('home'))

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
            cursor.execute('INSERT INTO contacto (nombre, correo, telefono, motivo, mensaje, fecha) VALUES (%s, %s, %s, %s, %s,now())', (nombre, correo,telefono,motivo,mensaje,))
        conexion.commit()
        conexion.close()
        flash('Mensaje enviado correctamente!', category='success')
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
                cursor.execute('SELECT DISTINCT a.id, a.nombre, a.apellido, a.rut, a.sexo, a.edad, a.nacionalidad, a.estado_civil, a.email, a.telefono, a.profesion, a.nivel_estudios, a.situacion_laboral, a.direccion, a.region, a.fecha, c.nombre AS nombreCurso, c.codigo_curso, ea.estado, u.nick FROM alumno_estado ae JOIN alumno a ON a.id = ae.id_alumno JOIN curso c ON a.id_curso = c.id JOIN estado_alumno ea ON ae.id_estado = ea.id JOIN usuario u ON ae.id_usuario = u.id WHERE ae.id_estado = (select de.id_estado AS Id FROM alumno_estado de WHERE id_alumno = ae.id_alumno order by de.fecha desc limit 1) AND c.id = %s order by a.id desc;', (curso))# WHERE id = %s', (session['id'],))
                aspirantes = cursor.fetchall()
                cursor.execute('SELECT id, nombre, codigo_curso FROM curso')# WHERE id = %s', (session['id'],))
                cursos = cursor.fetchall()
                cursor.execute('SELECT nombre, codigo_curso, id FROM curso where id = %s', (curso))# WHERE id = %s', (session['id'],))
                datosCurso = cursor.fetchall()
                cursor.execute('SELECT id, estado FROM Estado_Alumno')# WHERE id = %s', (session['id'],))
                estados = cursor.fetchall()
                conexion.close()
            return render_template('administracion/aspirantes.html',
                                aspirantes=aspirantes,
                                cursos=cursos,
                                datosCurso=datosCurso,
                                estados = estados,
                                selected = int(selected),
                                )
        else:
            if cursoActivo != 0:
                selected=cursoActivo
                conexion = obtener_conexion()
                with conexion.cursor() as cursor:
                    cursor.execute('SELECT DISTINCT a.id, a.nombre, a.apellido, a.rut, a.sexo, a.edad, a.nacionalidad, a.estado_civil, a.email, a.telefono, a.profesion, a.nivel_estudios, a.situacion_laboral, a.direccion, a.region, a.fecha, c.nombre AS nombreCurso, c.codigo_curso, ea.estado, u.nick FROM alumno_estado ae JOIN alumno a ON a.id = ae.id_alumno JOIN curso c ON a.id_curso = c.id JOIN estado_alumno ea ON ae.id_estado = ea.id JOIN usuario u ON ae.id_usuario = u.id WHERE ae.id_estado = (select de.id_estado AS Id FROM alumno_estado de WHERE id_alumno = ae.id_alumno order by de.fecha desc limit 1) AND c.id = %s order by a.id desc;', (cursoActivo))# WHERE id = %s', (session['id'],))
                    aspirantes = cursor.fetchall()
                    cursor.execute('SELECT id, nombre, codigo_curso FROM curso')# WHERE id = %s', (session['id'],))
                    cursos = cursor.fetchall()
                    cursor.execute('SELECT nombre, codigo_curso, id FROM curso where id = %s', (cursoActivo))# WHERE id = %s', (session['id'],))
                    datosCurso = cursor.fetchall()
                    cursor.execute('SELECT id, estado FROM Estado_Alumno')# WHERE id = %s', (session['id'],))
                    estados = cursor.fetchall()
                    conexion.close()
                return render_template('administracion/aspirantes.html',
                                aspirantes=aspirantes,
                                cursos=cursos,
                                datosCurso=datosCurso,
                                estados = estados,
                                selected = int(selected),
                                )
            else:
                aspirantes = []
                conexion = obtener_conexion()
                with conexion.cursor() as cursor:
                    cursor.execute('SELECT id, nombre, codigo_curso FROM curso')# WHERE id = %s', (session['id'],))
                    cursos = cursor.fetchall()
                    cursor.execute('SELECT id, estado FROM Estado_Alumno')# WHERE id = %s', (session['id'],))
                    estados = cursor.fetchall()
                conexion.close()
                return render_template('administracion/aspirantes.html',
                                    cursos=cursos,
                                    aspirantes=aspirantes,
                                    datosCurso=datosCurso,
                                    estados = estados,
                                    selected = 0,
                                    )
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/guardarEstado/<int:id>/<int:curso>', methods=['GET', 'POST'])
def guardarEstado(id, curso):
    if request.method == 'POST' and 'estado' in request.form:
        idEstado = request.form['estado']
        idUser = session['id']
        selected=curso
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO alumno_estado(id_estado, id_alumno, fecha, id_usuario) VALUES (%s, %s, now(), %s)', (idEstado, id, idUser,))
        conexion.commit()
        conexion.close()
        flash('Estado guardado correctamente!', category='success')
        global cursoActivo
        cursoActivo = curso
        return redirect(url_for('aspirantes'))
    return redirect(url_for('home'))

@app.route('/aspirantes-asistente-aula', methods=['GET', 'POST'])
def aspirantesAula():
    if 'loggedin' in session:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT * FROM alumno where id_curso = 1 order by id desc')# WHERE id = %s', (session['id'],))
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
    return redirect(url_for('home'))

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
    return redirect(url_for('home'))

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
    return redirect(url_for('home'))

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
    return redirect(url_for('home'))

@app.route('/mensajes-contacto')
def mensajesContacto():
    # Check if user is loggedin
    if 'loggedin' in session:
        mensajes = []
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM contacto order by id desc")# WHERE id = %s', (session['id'],))
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
    return redirect(url_for('home'))

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:

        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT * FROM usuario WHERE id = %s', (session['id'],))
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