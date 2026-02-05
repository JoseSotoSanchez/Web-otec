from flask import Flask, render_template, request, redirect, flash,url_for, session,jsonify, json, Response, send_file
from flask_paginate import Pagination, get_page_args ,get_page_parameter  
from flask import Flask, request, render_template, jsonify, json
from bd import obtener_conexion
from correo import enviarEmail, upperFirst, enviarEmailAceptacion, obtenerMes, enviarEmailPago, enviarEmailBienvenida, enviarEmailBienvenidaIEMCE, enviarEmailBienvenidaAAMCE, enviarEmailBienvenidaCBC, enviarEmailBienvenidaAAC
from datetime import datetime
from openpyxl import Workbook
from io import BytesIO
import csv
from io import StringIO
import os
from tempfile import NamedTemporaryFile
import locale
import sys
import socket
from itertools import cycle
from models.aspirante import Aspirante, AspiranteJSON
from models.curso import Curso
from db_operations import verificar_postulacion_existente, obtener_cursos_activos, registrar_aspirante, obtener_info_curso, insertar_log_usuario, obtener_aspirantes_por_curso, obtener_cursos, obtener_datos_curso_por_id, obtener_estados_alumno,guardar_contacto, obtener_info_alumno_por_id, buscar_alumnos_por_nombre, buscar_alumno_por_rut, buscar_alumno_por_correo, obtener_aspirante_por_id, registrar_pago, actualizar_datos_alumno, registrar_estado_alumno
import bcrypt
# from flask import Flask, request, session, redirect, url_for, flash, render_template, render_template_string


# === APP FLASK ===
app = Flask(__name__)
# app.secret_key = SECRET_KEY
# app.config.update(
#     SESSION_COOKIE_HTTPONLY=True,
#     SESSION_COOKIE_SAMESITE="Lax",
# )

locale.setlocale(locale.LC_TIME, 'es_ES.utf-8')
app.secret_key = 'b93f9e42086d47df8c36f5121b6a8a22'
API_SECRET_KEY = 'b93f9e42086d47df8c36f5121b6a8a22'

cursoActivo = 0
aspirantesSave = []
cursos = []

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'usuario' in request.form and 'clave' in request.form:
        usuario = request.form['usuario']
        clave = request.form['clave']
        hostname = request.remote_addr
        IPAddr = request.environ['REMOTE_ADDR']
        hostnameAddr = hostname + " / " + IPAddr
        clave_hashed = bcrypt.hashpw(clave.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nick, nombre, clave FROM Usuario WHERE nick = %s", (usuario,))
            account = cursor.fetchone()
        conexion.close()

        if account and bcrypt.checkpw(clave.encode('utf-8'), account[3].encode('utf-8')):
            estado = "OK"
            insertar_log_usuario(usuario, clave_hashed, estado, hostnameAddr)
            session['loggedin'] = True
            session['id'] = account[0]
            session['usuario'] = account[1]
            session['nombre'] = account[2]
            flash('Login correcto!', category='success')
            return redirect(url_for('index'))
        else:
            estado = "fallido"
            insertar_log_usuario(usuario, clave_hashed, estado, hostnameAddr)
            flash('Usuario y/o contraseña incorrectas!', category='error')
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('usuario', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/')
def index():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursos = obtener_cursos_activos()
        return render_template('home.html',
                            cursos=cursos,
                            )
    return render_template('home.html')

@app.route('/home')
def home():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursos = obtener_cursos_activos()
        return render_template('home.html',
                            cursos=cursos,
                            )

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/privacidad')
def privacidad():
    return render_template('privacidad.html')

@app.route('/postulacion-curso', methods=['GET', 'POST'])
def postulacionCurso():
    if request.method == 'POST':
        hostname = request.remote_addr
        ip = request.environ.get('REMOTE_ADDR', '0.0.0.0')
        aspiranteNew = Aspirante(request.form, hostname, ip, request.environ)
        conexion = obtener_conexion()
        rut = aspiranteNew.rut.upper()
        rut = rut.replace("-","")
        rut = rut.replace(".","")
        cursos = obtener_cursos_activos()
        aspirante = verificar_postulacion_existente(rut, aspiranteNew.curso)
        if aspirante:
            flash('Usted ya ha postulado al curso!, en breve nos comunicaremos con usted.', category='error')
            return render_template('cursos/curso-asistente-de-aula.html', cursos=cursos)
        if not validar_rut(rut):
            flash('Rut no válido! Favor vuelva a intentarlo', category='error')
            return render_template('cursos/curso-asistente-de-aula.html', cursos=cursos)
        if len(rut) < 6:
            flash('Rut no válido! Favor vuelva a intentarlo', category='error')
            return render_template('cursos/curso-asistente-de-aula.html', cursos=cursos)
        registrar_aspirante(aspiranteNew, rut)
        curso_ = obtener_info_curso(aspiranteNew.curso)
        nombre = aspiranteNew.nombre + ' ' + aspiranteNew.apellido
        curso = curso_[0][1]
        mes = curso_[0][3].month
        nombreMes = obtenerMes(mes)
        mesFin = curso_[0][4].month
        nombreMesFin = obtenerMes(mesFin)
        enviarEmail(nombre, aspiranteNew.telefono, curso, aspiranteNew.correo, curso_[0][3].strftime("%d de "+nombreMes+" del %Y") , curso_[0][4].strftime("%d de "+nombreMesFin+" del %Y"), curso_[0][2], curso_[0][5], curso_[0][6])
        flash('Postulación enviada correctamente!', category='success')
    else:
        cursos = obtener_cursos_activos()
        return render_template('index.html',
                            cursos=cursos,
                            )
    return redirect(url_for('index'))

@app.route('/curso-asistente-de-aula', methods=['GET', 'POST'])
def asistenteAula():
    cursos = obtener_cursos_activos()
    return render_template('cursos/curso-asistente-de-aula.html',
                            cursos=cursos,
                            )

@app.route('/curso-inspector-educacional', methods=['GET', 'POST'])
def inspectorEducacional():
    cursos = obtener_cursos_activos()
    return render_template('cursos/curso-inspector-educacional.html',
                        cursos=cursos,
                        )

@app.route('/curso-asistente-administrativo-contable', methods=['GET', 'POST'])
def asistenteContable():
    cursos = obtener_cursos_activos()
    return render_template('cursos/curso-asistente-administrativo-contable.html',
                            cursos=cursos,
                            )

@app.route('/curso-cajero-bancario-y-comercial', methods=['GET', 'POST'])
def cajeroBancario():
    cursos = obtener_cursos_activos()
    return render_template('cursos/curso-cajero-bancario-y-comercial.html',
                            cursos=cursos,
                            )
    
@app.route('/curso-convivencia-escolar', methods=['GET', 'POST'])
def convivenciaEscolar():
    cursos = obtener_cursos_activos()
    return render_template('cursos/curso-convivencia-escolar.html',
                        cursos=cursos,
                        )
    
@app.route('/curso-tutor-sombra-y-trastorno-del-espectro-autista', methods=['GET', 'POST'])
def tea():
    cursos = obtener_cursos_activos()
    return render_template('cursos/curso-tutor-sombra-y-trastorno-del-espectro-autista.html',
                        cursos=cursos,
                        )

@app.route('/curso-corredor-de-propiedades-y-estudio-de-titulo', methods=['GET', 'POST'])
def corretaje():
    cursos = obtener_cursos_activos()
    return render_template('cursos/curso-corredor-de-propiedades-y-estudio-de-titulo.html',
                        cursos=cursos,
                        )

@app.route('/curso-perfeccionamiento-rrhh', methods=['GET', 'POST'])
def rrhh():
    cursos = obtener_cursos_activos()    
    return render_template('cursos/curso-perfeccionamiento-rrhh.html',
                        cursos=cursos,
                        )
    
@app.route('/curso-asistente-en-educadora-de-parvulos', methods=['GET', 'POST'])
def asistenteParvulos():
    cursos = obtener_cursos_activos()    
    return render_template('cursos/curso-asistente-en-educadora-de-parvulos.html',
                        cursos=cursos,
                        )
    
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
        guardar_contacto(nombre, correo, telefono, motivo, mensaje)
        flash('Mensaje enviado correctamente!', category='success')
        return redirect(url_for('index'))
    return render_template('contactanos.html')

@app.route('/aspirantes', methods=['GET', 'POST'])
def aspirantes():
    datosCurso = ''
    global cursoActivo
    global aspirantesSave
    if 'loggedin' in session:
        if request.method == 'POST' and 'curso' in request.form :
            curso = request.form['curso']
            selected=curso
            aspirantes = obtener_aspirantes_por_curso(curso)
            cursos = obtener_cursos()
            datosCurso = obtener_datos_curso_por_id(curso)
            estados = obtener_estados_alumno()
            total = len(aspirantes)
            aspirantesSave = aspirantes
            session['cursoActivo'] = curso
            page, per_page, offset = get_page_args(page_parameter='page',
                                        per_page_parameter='per_page')
            total = len(aspirantes)
            pagination_aspirantes = get_aspirantes(offset=offset, per_page=per_page, aspirantes=aspirantes)
            pagination = Pagination(page=page, per_page=per_page, total=total,
                                    css_framework='bootstrap4')
            
            page_ = request.args.get('page_', 1,type=int)
            per_page_ = 50
            start = (page_ - 1) * per_page_
            end = start + per_page_
            total_pages = (len(aspirantes) + per_page_ - 1) // per_page_
            pages = range(1, total_pages + 1)

            items_on_page = aspirantes[start:end]
            return render_template('administracion/aspirantes.html',
                            aspirantes=pagination_aspirantes,
                            page=page,
                            per_page=100,
                            pagination=pagination,
                            aspirantesSave = aspirantes,
                            cursos=cursos,
                            datosCurso=datosCurso,
                            estados = estados,
                            selected = int(selected),
                            total = total,
                            items_on_page = items_on_page,
                            total_pages = total_pages,
                            page_=page_,
                            pages=pages,
                            )
        else:
            cursoAct = session.get('cursoActivo', 0)
            if cursoAct == 0:
                curso = request.args.get('curso', 0,type=int)
                cursoAct = curso
            if cursoAct != 0:
                selected=cursoAct
                aspirantes = obtener_aspirantes_por_curso(cursoAct)
                cursos = obtener_cursos()
                datosCurso = obtener_datos_curso_por_id(cursoAct)
                estados = obtener_estados_alumno()
                page, per_page, offset = get_page_args(page_parameter='page',
                                        per_page_parameter='per_page')
                total = len(aspirantes)
                pagination_aspirantes = get_aspirantes(offset=offset, per_page=per_page, aspirantes=aspirantes)
                pagination = Pagination(page=page, per_page=per_page, total=total,
                                        css_framework='bootstrap4')
                aspirantesSave = aspirantes
                total = len(aspirantes)
                page_ = request.args.get('page_', 1,type=int)
                per_page_ = 50
                start = (page_ - 1) * per_page_
                end = start + per_page_
                total_pages = (len(aspirantes) + per_page_ - 1) // per_page_
                pages = range(1, total_pages + 1)

                items_on_page = aspirantes[start:end]
                return render_template('administracion/aspirantes.html',
                                aspirantes=pagination_aspirantes,
                                page=page,
                                per_page=100,
                                pagination=pagination,
                                aspirantesSave = aspirantes,
                                cursos=cursos,
                                datosCurso=datosCurso,
                                estados = estados,
                                selected = int(selected),
                                total = total,
                                items_on_page = items_on_page,
                                total_pages = total_pages,
                                page_ =page_,
                                pages= pages,
                                )
            else:
                aspirantes = []
                items_on_page = []
                cursos = obtener_cursos()
                estados = obtener_estados_alumno()
                page, per_page, offset = get_page_args(page_parameter='page',
                                        per_page_parameter='per_page')
                total = len(aspirantes)
                pagination_aspirantes = get_aspirantes(offset=offset, per_page=per_page, aspirantes=aspirantes)
                pagination = Pagination(page=page, per_page=per_page, total=total,
                                        css_framework='bootstrap4')
                aspirantesSave = aspirantes
                total = len(aspirantes)
                return render_template('administracion/aspirantes.html',
                                aspirantes=pagination_aspirantes,
                                page=page,
                                per_page=100,
                                pagination=pagination,
                                aspirantesSave = aspirantes,
                                cursos=cursos,
                                datosCurso=datosCurso,
                                estados = estados,
                                selected = 0,
                                total = total,
                                items_on_page = items_on_page,
                                page_ = 0,
                                total_pages = 0,
                                )
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/busqueda', methods=['GET', 'POST'])
def busqueda():
    datosCurso = ''
    aspirantes = []
    idAlumnoSearch = curso = session.get('idAlumnoSearch', 0)
    if 'loggedin' in session:
        if request.method == 'POST' and 'ide' in request.form :
            idalumno = request.form['ide']
            nombreAlumno = request.form['nombreSearch']
            rutAlumno = request.form['rutSearch']
            correoAlumno = request.form['correoSearch']
            session['idAlSearch'] = idalumno
            if (idalumno is None or idalumno.strip() == '') and (nombreAlumno is None or nombreAlumno.strip() == '') and (rutAlumno is None or rutAlumno.strip() == '') and (correoAlumno is None or correoAlumno.strip() == ''):
                flash('Debe ingresar un parámetro de busqueda!', category='error')
                return redirect(url_for('busqueda'))
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                if idalumno is not None and idalumno.strip() != '':
                    aspirantes = obtener_info_alumno_por_id(idalumno) 
                if nombreAlumno is not None and nombreAlumno.strip() != '':
                    aspirantes = buscar_alumnos_por_nombre(nombreAlumno)
                if rutAlumno is not None and rutAlumno.strip() != '':
                    aspirantes = buscar_alumno_por_rut(rutAlumno)
                if correoAlumno is not None and correoAlumno.strip() != '':
                    aspirantes = buscar_alumno_por_correo(correoAlumno)
                if aspirantes is None or not aspirantes:
                    flash('No se ha encontrado resultados!', category='error')
                    return redirect(url_for('busqueda'))
                cursos = obtener_cursos()
                datosCurso = obtener_datos_curso_por_id(aspirantes[0][23])
                estados = obtener_estados_alumno()
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
                aspirantes = obtener_aspirante_por_id(idAlumnoSearch)
                cursos = obtener_cursos()
                estados = obtener_estados_alumno()
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

@app.route('/descargaCsv/<int:curso>', methods=['GET', 'POST'])
def descargaCsv(curso):
    if 'loggedin' in session:
        if request.method == 'POST':
            wb = Workbook()
            ws = wb.active
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                # cursor.execute('SELECT DISTINCT a.id, a.nombre, a.apellido, a.rut, a.sexo, a.edad, a.nacionalidad, a.estado_civil, a.email, a.telefono, a.profesion, a.nivel_estudios, a.situacion_laboral, a.direccion, a.region, a.fecha, c.nombre AS nombreCurso, c.codigo_curso, ea.estado, u.nick, ea.id ,c.costo, a.ingreso, (SELECT SUM(p.monto) FROM Pagos p WHERE p.id_alumno = a.id AND p.id_curso = a.id_curso) AS total_pagos FROM Alumno_Estado ae JOIN Alumno a ON a.id = ae.id_alumno JOIN Curso c ON a.id_curso = c.id JOIN Estado_Alumno ea ON ae.id_estado = ea.id JOIN Usuario u ON ae.id_usuario = u.id WHERE ae.id_estado = (select de.id_estado AS Id FROM Alumno_Estado de WHERE id_alumno = ae.id_alumno order by de.fecha desc limit 1) AND c.id = %s order by a.id desc;', (curso))
                aspirantes = obtener_aspirantes_por_curso(curso)
                conexion.close()
            nombre_archivo = 'curso ' + aspirantes[0][17] + '.xlsx'
            with NamedTemporaryFile(delete=False) as tmpfile:
                for row in aspirantes:
                    ws.append(row)
                wb.save(tmpfile.name)
            return send_file(
                tmpfile.name,
                attachment_filename=nombre_archivo,
                as_attachment=True
            )
    return redirect(url_for('index'))

@app.route('/descargaCsvPagados/<int:curso>', methods=['GET', 'POST'])
def descargaCsvPagados(curso):
    codigoCurso = ''
    if 'loggedin' in session:
        if request.method == 'POST':
            wb = Workbook()
            ws = wb.active
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                # cursor.execute('SELECT DISTINCT a.id, a.nombre, a.apellido, a.rut, a.sexo, a.edad, a.nacionalidad, a.estado_civil, a.email, a.telefono, a.profesion, a.nivel_estudios, a.situacion_laboral, a.direccion, a.region, a.fecha, c.nombre AS nombreCurso, c.codigo_curso, ea.estado, u.nick, ea.id ,c.costo, a.ingreso, (SELECT SUM(p.monto) FROM Pagos p WHERE p.id_alumno = a.id AND p.id_curso = a.id_curso) AS total_pagos FROM Alumno_Estado ae JOIN Alumno a ON a.id = ae.id_alumno JOIN Curso c ON a.id_curso = c.id JOIN Estado_Alumno ea ON ae.id_estado = ea.id JOIN Usuario u ON ae.id_usuario = u.id WHERE ae.id_estado = (select de.id_estado AS Id FROM Alumno_Estado de WHERE id_alumno = ae.id_alumno order by de.fecha desc limit 1) AND c.id = %s order by a.id desc;', (curso))
                aspirantes = obtener_aspirantes_por_curso(curso)
                conexion.close()

            nueva_lista_aspirantes = []
            for aspirante in aspirantes:
                alumnoid, alumnonombre, alumnoapellido, alumnorut, alumnosexo, alumnoedad, alumnonacionalidad, alumnoestado_civil, alumnoemail, alumnotelefono, alumnoprofesion, alumnonivel_estudios, alumnosituacion_laboral, alumnodireccion, alumnoregion, alumnofecha, cursonombreCurso, cursoCodigo_curso, estadoAlumnoestado, usuarioNick, estadoAlumnoid, cursoCosto, alumnoIngreso, totalPagado = aspirante
                if estadoAlumnoid >= 18:
                    alumnorut = limpiar_rut(alumnorut.replace('.', '').replace('-', ''))
                    passGen = alumnorut[:4] + "#icL"
                    nueva_fila = (alumnorut, passGen, alumnonombre, alumnoapellido, alumnoemail, cursoCodigo_curso, 'CL', 'es_mx', 'América/Santiago', alumnoid)
                    nueva_lista_aspirantes.append(nueva_fila)
                    if codigoCurso == '':
                            codigoCurso = cursoCodigo_curso
            nombre_archivo = 'curso ' + codigoCurso + '.xlsx'

            with NamedTemporaryFile(delete=False) as tmpfile:
                for row in nueva_lista_aspirantes:
                    ws.append(row)
                wb.save(tmpfile.name)

            return send_file(
                tmpfile.name,
                attachment_filename=nombre_archivo,
                as_attachment=True
            )
    return redirect(url_for('index'))

def generar_csv(data):
    # Usar el módulo csv de Python para convertir los datos a formato CSV
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Nombre', 'Apellido', 'Rut', 'Sexo', 'Edad', 'Nacionalidad', 'Estado Civil', 'Email', 'Telefono', 'Profesion', 'Nivel de Estudios', 'Situacion Laboral', 'Direccion', 'Region', 'Fecha', 'Nombre del Curso', 'Codigo del Curso', 'Estado del Alumno', 'Nick del Usuario', 'ID de Estado', 'Costo', 'Ingreso', 'ID de Curso', 'Total pagado'])
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

@app.route('/guardarPago/<int:id>/<int:curso>', methods=['GET', 'POST'])
def guardarPago(id, curso):
    if request.method == 'POST' and 'formaPago' in request.form and 'montoPago' in request.form:
        page_ = request.args.get('page_', 1,type=int)
        formaPago = request.form['formaPago']
        montoPago = request.form['montoPago']
        idUser = session['id']
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            registrar_pago(id, curso, montoPago, formaPago)
            registrar_estado_alumno("18", id, idUser)
            # cursor.execute('INSERT INTO Pagos(id_alumno, id_curso, monto, medio_pago, fecha) VALUES (%s, %s, %s, %s, now())', (id, curso, montoPago,formaPago,))
            # cursor.execute('INSERT INTO Alumno_Estado(id_estado, id_alumno, fecha, id_usuario) VALUES (%s, %s, now(), %s)', ("18", id, idUser,))
        conexion.commit()
        conexion.close()
        flash('Pago guardado correctamente!', category='success')
        session['cursoActivo'] = curso
        return redirect(url_for('aspirantes', page_=page_, curso=curso))
    return redirect(url_for('index'))

@app.route('/guardarEstado/<int:id>/<int:curso>', methods=['GET', 'POST'])
def guardarEstado(id, curso):
    if request.method == 'POST' and 'estado' in request.form and 'correoAlumno' in request.form and 'celularAlumno' in request.form and 'nombresAlumno' in request.form and 'apellidosAlumno' in request.form:
        page_ = request.args.get('page_', 1,type=int)
        idEstado = request.form['estado']
        correoAlumno = request.form['correoAlumno']
        celularAlumno = request.form['celularAlumno']
        nombresAlumno = request.form['nombresAlumno']
        apellidosAlumno = request.form['apellidosAlumno']
        idUser = session['id']
        selected=curso
        registrar_estado_alumno(idEstado, id, idUser)
        actualizar_datos_alumno(id, nombresAlumno, apellidosAlumno, correoAlumno, celularAlumno)
            # cursor.execute('INSERT INTO Alumno_Estado(id_estado, id_alumno, fecha, id_usuario) VALUES (%s, %s, now(), %s)', (idEstado, id, idUser,))
            # cursor.execute('UPDATE Alumno SET nombre = %s, apellido = %s, email = %s, telefono = %s WHERE id = %s', (nombresAlumno, apellidosAlumno, correoAlumno, celularAlumno,id,))x|x|
        flash('Estado guardado correctamente!', category='success')
        session['cursoActivo'] = curso
        return redirect(url_for('aspirantes', page_=page_, curso=curso))
    return redirect(url_for('index'))



@app.route('/envioCorreoAceptacion/<int:id>/<int:curso>', methods=['GET', 'POST'])
def envioCorreoAceptacion(id, curso):
    if request.method == 'POST':
        page_ = request.args.get('page_', 1,type=int)
        urlPago = request.form['urlPago']
        idUser = session['id']
        selected=curso
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT DISTINCT a.nombre, a.apellido, a.email FROM Alumno a WHERE a.id = %s;', (id))
            alumno = cursor.fetchall()
            cursor.execute('SELECT c.nombre, c.fecha_inicio, c.fecha_fin, c.modalidad, h.rango, d.rango, c.costo FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id where c.id = %s', (curso))
            datosCurso = cursor.fetchall()
            cursor.execute('SELECT nombre, nick, correo, numero FROM Usuario WHERE id = %s', (idUser))
            datosUsuario = cursor.fetchall()
        conexion.close()
        nombre = alumno[0][0] + ' ' + alumno[0][1]
        mes = datosCurso[0][1].month
        nombreMes = obtenerMes(mes)
        mesFin = datosCurso[0][2].month
        nombreMesFin = obtenerMes(mesFin)
        valorCurso = locale.format_string('%d', datosCurso[0][6], grouping=True)
        if "Corredor" in datosCurso[0][0]:
            porcentaje = "50"
        else:
            porcentaje = "75"
        enviarEmailAceptacion(nombre, alumno[0][2], datosCurso[0][0], datosCurso[0][1].strftime("%d de "+nombreMes+" del %Y"), datosCurso[0][2].strftime("%d de "+nombreMesFin+" del %Y"), datosCurso[0][5], datosCurso[0][4], datosCurso[0][3], urlPago, datosUsuario[0][0], datosUsuario[0][2], datosUsuario[0][3], valorCurso, porcentaje)
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno_Estado(id_estado, id_alumno, fecha, id_usuario) VALUES (13, %s, now(), %s)', (id, idUser,))
        conexion.commit()
        conexion.close()
        flash('Correo enviado correctamente!', category='success')
        session['cursoActivo'] = curso
        return redirect(url_for('aspirantes', page_=page_, curso=curso))
    return redirect(url_for('index'))

@app.route('/envioCorreoBienvenidaIEMCE/<int:id>/<int:curso>', methods=['GET', 'POST'])
def envioCorreoBienvenidaIEMCE(id, curso):
    page_ = request.args.get('page_', 1,type=int)
    if request.method == 'POST':
        linkSense = request.form['linkSense']
        idUser = session['id']
        selected=curso
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT DISTINCT a.nombre, a.apellido, a.email FROM Alumno a WHERE a.id = %s;', (id))
            alumno = cursor.fetchall()
            cursor.execute('SELECT c.nombre, c.fecha_inicio, c.fecha_fin, c.modalidad, h.rango, d.rango, c.costo FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id where c.id = %s', (curso))
            datosCurso = cursor.fetchall()
            cursor.execute('SELECT nombre, nick, correo, numero FROM Usuario WHERE id = %s', (idUser))
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
        session['cursoActivo'] = curso
        return redirect(url_for('aspirantes', page_=page_, curso=curso))
    return redirect(url_for('index'))

@app.route('/envioCorreoBienvenidaAAMCE/<int:id>/<int:curso>', methods=['GET', 'POST'])
def envioCorreoBienvenidaAAMCE(id, curso):
    page_ = request.args.get('page_', 1,type=int)
    if request.method == 'POST':
        linkSense = request.form['linkSense']
        idUser = session['id']
        selected=curso
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT DISTINCT a.nombre, a.apellido, a.email FROM Alumno a WHERE a.id = %s;', (id))
            alumno = cursor.fetchall()
            cursor.execute('SELECT c.nombre, c.fecha_inicio, c.fecha_fin, c.modalidad, h.rango, d.rango, c.costo FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id where c.id = %s', (curso))
            datosCurso = cursor.fetchall()
            cursor.execute('SELECT nombre, nick, correo, numero FROM Usuario WHERE id = %s', (idUser))
            datosUsuario = cursor.fetchall()
        conexion.close()
        nombre = alumno[0][0] + ' ' + alumno[0][1]
        mes = datosCurso[0][1].month
        nombreMes = obtenerMes(mes)
        mesFin = datosCurso[0][2].month
        valorCurso = locale.format_string('%d', datosCurso[0][6], grouping=True)
        nombreMesFin = obtenerMes(mesFin)
        enviarEmailBienvenidaAAMCE(nombre, alumno[0][2], datosCurso[0][0], datosCurso[0][1].strftime("%d de "+nombreMes+" del %Y"), datosCurso[0][2].strftime("%d de "+nombreMesFin+" del %Y"), datosCurso[0][5], datosCurso[0][4], datosCurso[0][3], linkSense, datosUsuario[0][0], datosUsuario[0][2], datosUsuario[0][3], valorCurso)
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno_Estado(id_estado, id_alumno, fecha, id_usuario) VALUES (14, %s, now(), %s)', (id, idUser,))
        conexion.commit()
        conexion.close()
        flash('Correo enviado correctamente!', category='success')
        session['cursoActivo'] = curso
        return redirect(url_for('aspirantes', page_=page_, curso=curso))
    return redirect(url_for('index'))

@app.route('/envioCorreoBienvenidaCBC/<int:id>/<int:curso>', methods=['GET', 'POST'])
def envioCorreoBienvenidaCBC(id, curso):
    page_ = request.args.get('page_', 1,type=int)
    if request.method == 'POST':
        linkSense = request.form['linkSense']
        idUser = session['id']
        selected=curso
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT DISTINCT a.nombre, a.apellido, a.email FROM Alumno a WHERE a.id = %s;', (id))
            alumno = cursor.fetchall()
            cursor.execute('SELECT c.nombre, c.fecha_inicio, c.fecha_fin, c.modalidad, h.rango, d.rango, c.costo FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id where c.id = %s', (curso))
            datosCurso = cursor.fetchall()
            cursor.execute('SELECT nombre, nick, correo, numero FROM Usuario WHERE id = %s', (idUser))
            datosUsuario = cursor.fetchall()
        conexion.close()
        nombre = alumno[0][0] + ' ' + alumno[0][1]
        mes = datosCurso[0][1].month
        nombreMes = obtenerMes(mes)
        mesFin = datosCurso[0][2].month
        valorCurso = locale.format_string('%d', datosCurso[0][6], grouping=True)
        nombreMesFin = obtenerMes(mesFin)
        enviarEmailBienvenidaCBC(nombre, alumno[0][2], datosCurso[0][0], datosCurso[0][1].strftime("%d de "+nombreMes+" del %Y"), datosCurso[0][2].strftime("%d de "+nombreMesFin+" del %Y"), datosCurso[0][5], datosCurso[0][4], datosCurso[0][3], linkSense, datosUsuario[0][0], datosUsuario[0][2], datosUsuario[0][3], valorCurso)
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno_Estado(id_estado, id_alumno, fecha, id_usuario) VALUES (14, %s, now(), %s)', (id, idUser,))
        conexion.commit()
        conexion.close()
        flash('Correo enviado correctamente!', category='success')
        session['cursoActivo'] = curso
        return redirect(url_for('aspirantes', page_=page_, curso=curso))
    return redirect(url_for('index'))

@app.route('/envioCorreoBienvenidaAAC/<int:id>/<int:curso>', methods=['GET', 'POST'])
def envioCorreoBienvenidaAAC(id, curso):
    page_ = request.args.get('page_', 1,type=int)
    if request.method == 'POST':
        linkSense = request.form['linkSense']
        idUser = session['id']
        selected=curso
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT DISTINCT a.nombre, a.apellido, a.email FROM Alumno a WHERE a.id = %s;', (id))
            alumno = cursor.fetchall()
            cursor.execute('SELECT c.nombre, c.fecha_inicio, c.fecha_fin, c.modalidad, h.rango, d.rango, c.costo FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id where c.id = %s', (curso))
            datosCurso = cursor.fetchall()
            cursor.execute('SELECT nombre, nick, correo, numero FROM Usuario WHERE id = %s', (idUser))
            datosUsuario = cursor.fetchall()
        conexion.close()
        nombre = alumno[0][0] + ' ' + alumno[0][1]
        mes = datosCurso[0][1].month
        nombreMes = obtenerMes(mes)
        mesFin = datosCurso[0][2].month
        valorCurso = locale.format_string('%d', datosCurso[0][6], grouping=True)
        nombreMesFin = obtenerMes(mesFin)
        enviarEmailBienvenidaAAC(nombre, alumno[0][2], datosCurso[0][0], datosCurso[0][1].strftime("%d de "+nombreMes+" del %Y"), datosCurso[0][2].strftime("%d de "+nombreMesFin+" del %Y"), datosCurso[0][5], datosCurso[0][4], datosCurso[0][3], linkSense, datosUsuario[0][0], datosUsuario[0][2], datosUsuario[0][3], valorCurso)
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno_Estado(id_estado, id_alumno, fecha, id_usuario) VALUES (14, %s, now(), %s)', (id, idUser,))
        conexion.commit()
        conexion.close()
        flash('Correo enviado correctamente!', category='success')
        session['cursoActivo'] = curso
        return redirect(url_for('aspirantes', page_=page_, curso=curso))
    return redirect(url_for('index'))

@app.route('/envioCorreoPago/<int:id>/<int:curso>', methods=['GET', 'POST'])
def envioCorreoPago(id, curso):
    if request.method == 'POST':
        page_ = request.args.get('page_', 1,type=int)
        medioPago = request.form['medioPago']
        idUser = session['id']
        selected=curso
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT DISTINCT a.nombre, a.apellido, a.email FROM Alumno a WHERE a.id = %s;', (id))
            alumno = cursor.fetchall()
            cursor.execute('SELECT c.nombre, c.codigo_curso, c.costo FROM Curso c where c.id = %s', (curso))
            datosCurso = cursor.fetchall()
            cursor.execute('SELECT nombre, nick, correo, numero FROM Usuario WHERE id = %s', (idUser))
            datosUsuario = cursor.fetchall()
        conexion.close()
        nombre = alumno[0][0] + ' ' + alumno[0][1]
        enviarEmailPago(nombre, alumno[0][2], datosCurso[0][0], datosCurso[0][1], str(datosCurso[0][2]), medioPago, datosUsuario[0][0], datosUsuario[0][2], datosUsuario[0][3])
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno_Estado(id_estado, id_alumno, fecha, id_usuario) VALUES (19, %s, now(), %s)', (id, idUser,))
        conexion.commit()
        conexion.close()
        flash('Correo enviado correctamente!', category='success')
        session['cursoActivo'] = curso
        return redirect(url_for('aspirantes', page_=page_, curso=curso))
    return redirect(url_for('index'))

@app.route('/guardarPagoSearch/<int:id>/<int:curso>', methods=['GET', 'POST'])
def guardarPagoSearch(id, curso):
    if request.method == 'POST' and 'formaPago' in request.form and 'montoPago' in request.form:
        formaPago = request.form['formaPago']
        montoPago = request.form['montoPago']
        idUser = session['id']
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Pagos(id_alumno, id_curso, monto, medio_pago, fecha) VALUES (%s, %s, %s, %s, now())', (id, curso, montoPago,formaPago,))
            cursor.execute('INSERT INTO Alumno_Estado(id_estado, id_alumno, fecha, id_usuario) VALUES (%s, %s, now(), %s)', ("18", id, idUser,))
        conexion.commit()
        conexion.close()
        flash('Pago guardado correctamente!', category='success')
        session['idAlumnoSearch'] = id
        return redirect(url_for('busqueda'))
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
        session['idAlumnoSearch'] = id
        return redirect(url_for('busqueda'))
    return redirect(url_for('index'))

@app.route('/envioCorreoAceptacionSearch/<int:id>/<int:curso>', methods=['GET', 'POST'])
def envioCorreoAceptacionSearch(id, curso):
    if request.method == 'POST':
        urlPago = request.form['urlPago']
        idUser = session['id']
        selected=curso
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT DISTINCT a.nombre, a.apellido, a.email FROM Alumno a WHERE a.id = %s;', (id))
            alumno = cursor.fetchall()
            cursor.execute('SELECT c.nombre, c.fecha_inicio, c.fecha_fin, c.modalidad, h.rango, d.rango, c.costo FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id where c.id = %s', (curso))
            datosCurso = cursor.fetchall()
            cursor.execute('SELECT nombre, nick, correo, numero FROM Usuario WHERE id = %s', (idUser))
            datosUsuario = cursor.fetchall()
        conexion.close()
        nombre = alumno[0][0] + ' ' + alumno[0][1]
        mes = datosCurso[0][1].month
        nombreMes = obtenerMes(mes)
        mesFin = datosCurso[0][2].month
        nombreMesFin = obtenerMes(mesFin)
        valorCurso = locale.format_string('%d', datosCurso[0][6], grouping=True)
        if "Corredor" in datosCurso[0][0]:
            porcentaje = "50"
        else:
            porcentaje = "75"
        enviarEmailAceptacion(nombre, alumno[0][2], datosCurso[0][0], datosCurso[0][1].strftime("%d de "+nombreMes+" del %Y"), datosCurso[0][2].strftime("%d de "+nombreMesFin+" del %Y"), datosCurso[0][5], datosCurso[0][4], datosCurso[0][3], urlPago, datosUsuario[0][0], datosUsuario[0][2], datosUsuario[0][3], valorCurso, porcentaje)
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno_Estado(id_estado, id_alumno, fecha, id_usuario) VALUES (13, %s, now(), %s)', (id, idUser,))
        conexion.commit()
        conexion.close()
        flash('Correo enviado correctamente!', category='success')
        session['cursoActivo'] = curso
        session['idAlumnoSearch']  = id
        return redirect(url_for('busqueda'))
    return redirect(url_for('index'))

@app.route('/pagos-realizados/<int:id>/<int:curso>', methods=['GET', 'POST'])
def consultaPagos(id, curso):
    # Check if user is loggedin
    if 'loggedin' in session:
        pagos = []
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT * from Pagos WHERE id_alumno = %s AND id_curso = %s order by id desc', (id,curso,))
            pagos = cursor.fetchall()
        conexion.close()
        page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
        total = len(pagos)
        pagination_pagos = get_pagos(offset=offset, per_page=per_page, pagos=pagos)
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap4')
        return render_template('administracion/pagos-realizados.html',
                            pagos=pagination_pagos,
                            page=page,
                            per_page=10,
                            pagination=pagination,
                            )
    return redirect(url_for('index'))

@app.route('/envioCorreoBienvenidaIEMCESearch/<int:id>/<int:curso>', methods=['GET', 'POST'])
def envioCorreoBienvenidaIEMCESearch(id, curso):
    if request.method == 'POST':
        linkSense = request.form['linkSense']
        idUser = session['id']
        selected=curso
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT DISTINCT a.nombre, a.apellido, a.email FROM Alumno a WHERE a.id = %s;', (id))
            alumno = cursor.fetchall()
            cursor.execute('SELECT c.nombre, c.fecha_inicio, c.fecha_fin, c.modalidad, h.rango, d.rango, c.costo FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id where c.id = %s', (curso))
            datosCurso = cursor.fetchall()
            cursor.execute('SELECT nombre, nick, correo, numero FROM Usuario WHERE id = %s', (idUser))
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
        session['cursoActivo'] = curso
        session['idAlumnoSearch'] = id
        return redirect(url_for('busqueda'))
    return redirect(url_for('index'))

@app.route('/envioCorreoBienvenidaAAMCESearch/<int:id>/<int:curso>', methods=['GET', 'POST'])
def envioCorreoBienvenidaAAMCESearch(id, curso):
    if request.method == 'POST':
        linkSense = request.form['linkSense']
        idUser = session['id']
        selected=curso
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT DISTINCT a.nombre, a.apellido, a.email FROM Alumno a WHERE a.id = %s;', (id))
            alumno = cursor.fetchall()
            cursor.execute('SELECT c.nombre, c.fecha_inicio, c.fecha_fin, c.modalidad, h.rango, d.rango, c.costo FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id where c.id = %s', (curso))
            datosCurso = cursor.fetchall()
            cursor.execute('SELECT nombre, nick, correo, numero FROM Usuario WHERE id = %s', (idUser))
            datosUsuario = cursor.fetchall()
        conexion.close()
        nombre = alumno[0][0] + ' ' + alumno[0][1]
        mes = datosCurso[0][1].month
        nombreMes = obtenerMes(mes)
        mesFin = datosCurso[0][2].month
        valorCurso = locale.format_string('%d', datosCurso[0][6], grouping=True)
        nombreMesFin = obtenerMes(mesFin)
        enviarEmailBienvenidaAAMCE(nombre, alumno[0][2], datosCurso[0][0], datosCurso[0][1].strftime("%d de "+nombreMes+" del %Y"), datosCurso[0][2].strftime("%d de "+nombreMesFin+" del %Y"), datosCurso[0][5], datosCurso[0][4], datosCurso[0][3], linkSense, datosUsuario[0][0], datosUsuario[0][2], datosUsuario[0][3], valorCurso)
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno_Estado(id_estado, id_alumno, fecha, id_usuario) VALUES (14, %s, now(), %s)', (id, idUser,))
        conexion.commit()
        conexion.close()
        flash('Correo enviado correctamente!', category='success')
        session['cursoActivo'] = curso
        session['idAlumnoSearch'] = id
        return redirect(url_for('busqueda'))
    return redirect(url_for('index'))

@app.route('/envioCorreoBienvenidaCBCSearch/<int:id>/<int:curso>', methods=['GET', 'POST'])
def envioCorreoBienvenidaCBCSearch(id, curso):
    if request.method == 'POST':
        linkSense = request.form['linkSense']
        idUser = session['id']
        selected=curso
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT DISTINCT a.nombre, a.apellido, a.email FROM Alumno a WHERE a.id = %s;', (id))
            alumno = cursor.fetchall()
            cursor.execute('SELECT c.nombre, c.fecha_inicio, c.fecha_fin, c.modalidad, h.rango, d.rango, c.costo FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id where c.id = %s', (curso))
            datosCurso = cursor.fetchall()
            cursor.execute('SELECT nombre, nick, correo, numero FROM Usuario WHERE id = %s', (idUser))
            datosUsuario = cursor.fetchall()
        conexion.close()
        nombre = alumno[0][0] + ' ' + alumno[0][1]
        mes = datosCurso[0][1].month
        nombreMes = obtenerMes(mes)
        mesFin = datosCurso[0][2].month
        valorCurso = locale.format_string('%d', datosCurso[0][6], grouping=True)
        nombreMesFin = obtenerMes(mesFin)
        enviarEmailBienvenidaCBC(nombre, alumno[0][2], datosCurso[0][0], datosCurso[0][1].strftime("%d de "+nombreMes+" del %Y"), datosCurso[0][2].strftime("%d de "+nombreMesFin+" del %Y"), datosCurso[0][5], datosCurso[0][4], datosCurso[0][3], linkSense, datosUsuario[0][0], datosUsuario[0][2], datosUsuario[0][3], valorCurso)
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno_Estado(id_estado, id_alumno, fecha, id_usuario) VALUES (14, %s, now(), %s)', (id, idUser,))
        conexion.commit()
        conexion.close()
        flash('Correo enviado correctamente!', category='success')
        session['cursoActivo'] = curso
        session['idAlumnoSearch'] = id
        return redirect(url_for('busqueda'))
    return redirect(url_for('index'))

@app.route('/envioCorreoBienvenidaAACSearch/<int:id>/<int:curso>', methods=['GET', 'POST'])
def envioCorreoBienvenidaAACSearch(id, curso):
    if request.method == 'POST':
        linkSense = request.form['linkSense']
        idUser = session['id']
        selected=curso
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT DISTINCT a.nombre, a.apellido, a.email FROM Alumno a WHERE a.id = %s;', (id))
            alumno = cursor.fetchall()
            cursor.execute('SELECT c.nombre, c.fecha_inicio, c.fecha_fin, c.modalidad, h.rango, d.rango, c.costo FROM Curso c JOIN Horario h ON c.id_horario = h.id JOIN Dias d ON c.id_dias = d.id where c.id = %s', (curso))
            datosCurso = cursor.fetchall()
            cursor.execute('SELECT nombre, nick, correo, numero FROM Usuario WHERE id = %s', (idUser))
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
        session['cursoActivo'] = curso
        session['idAlumnoSearch'] = id
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
            cursor.execute('SELECT DISTINCT a.nombre, a.apellido, a.email FROM Alumno a WHERE a.id = %s;', (id))
            alumno = cursor.fetchall()
            cursor.execute('SELECT c.nombre, c.codigo_curso, c.costo FROM Curso c where c.id = %s', (curso))
            datosCurso = cursor.fetchall()
            cursor.execute('SELECT nombre, nick, correo, numero FROM Usuario WHERE id = %s', (idUser))
            datosUsuario = cursor.fetchall()
        conexion.close()
        nombre = alumno[0][0] + ' ' + alumno[0][1]
        enviarEmailPago(nombre, alumno[0][2], datosCurso[0][0], datosCurso[0][1], str(datosCurso[0][2]), medioPago, datosUsuario[0][0], datosUsuario[0][2], datosUsuario[0][3])
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO Alumno_Estado(id_estado, id_alumno, fecha, id_usuario) VALUES (19, %s, now(), %s)', (id, idUser,))
        conexion.commit()
        conexion.close()
        flash('Correo enviado correctamente!', category='success')
        session['cursoActivo'] = curso
        session['idAlumnoSearch'] = id
        return redirect(url_for('busqueda'))
    return redirect(url_for('index'))

@app.route('/cursos', methods=['GET', 'POST'])
def cursos():
    if 'loggedin' in session:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT *, h.rango, d.rango, DATEDIFF(c.fecha_inicio, now()) AS Diferencia, date_format(c.fecha_inicio, "%d-%m-%Y") AS fechaInicio, date_format(c.fecha_fin, "%d-%m-%Y") AS fechaFin FROM Curso c JOIN Horario h ON h.id = c.id_horario JOIN Dias d ON d.id = c.id_dias order by c.id desc')
            cursos = cursor.fetchall()
            cursor.execute('SELECT * FROM Horario order by id desc')
            horario = cursor.fetchall()
            cursor.execute('SELECT * FROM Dias order by id desc')
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
            cursor.execute('SELECT DISTINCT a.id, a.nombre, a.apellido, a.email FROM Alumno_Estado ae JOIN Alumno a ON a.id = ae.id_alumno JOIN Curso c ON a.id_curso = c.id WHERE ae.id_estado = (select de.id_estado AS Id FROM Alumno_Estado de WHERE id_alumno = ae.id_alumno order by de.fecha desc limit 1) AND c.id = %s AND ae.id_estado in (18,19) order by a.id desc', (idCurso))
            alumnosPagados = cursor.fetchall()
            cursor.execute('SELECT nombre, nick, correo, numero FROM Usuario WHERE id = %s', (idUser))
            datosUsuario = cursor.fetchall()
        conexion.close()
        for x in alumnosPagados:
            nombreAlumno = x[1] + ' ' + x[2]
            enviarEmailBienvenida(nombreAlumno, x[3], nombreCurso, urlZoom, idReunionZoom, codigoAccesoZoom, inicioCurso, nombreProfesor, horarioCurso, datosUsuario[0][0], datosUsuario[0][2], datosUsuario[0][3])
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute('INSERT INTO Alumno_Estado(id_alumno, id_estado, fecha,id_usuario) VALUES (%s, 20, now(), 1)', (x[0]))
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
            cursor.execute('SELECT * FROM Alumno where id_curso = 1 order by id desc')
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
    if 'loggedin' in session:
        mensajes = []
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM Contacto order by id desc")
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

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT * FROM Usuario WHERE id = %s', (session['id'],))
            account = cursor.fetchone()
        conexion.close()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))

@app.route('/api/postular', methods=['POST'])
def postular_aspirante():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "No se recibió un JSON válido"}), 400

        if data.get('api_key')  != API_SECRET_KEY:
            return jsonify({'error': 'Acceso no autorizado'}), 401
        # Crear el objeto Aspirante
        aspirante = AspiranteJSON(data)
        if aspirante.sexo == "M":
            aspirante.sexo = "Hombre"
        else:
            aspirante.sexo = "Mujer"
        rut = aspirante.rut.upper()
        rut = rut.replace("-","")
        rut = rut.replace(".","")
        cursos = obtener_cursos_activos()
        aspiranteVer = verificar_postulacion_existente(rut, aspirante.curso)
        if aspiranteVer:
            return jsonify({"cargado": "Usted ya ha postulado al curso!, en breve nos comunicaremos con usted."}), 400
        if not validar_rut(rut):
            return jsonify({"cargado": "Rut no válido! Favor vuelva a intentarlo"}), 400
        if len(rut) < 6:
            return jsonify({"cargado": "Rut no válido! Favor vuelva a intentarlo"}), 400
        # Guardar en la base de datos
        registrar_aspirante(aspirante, rut)
        curso_ = obtener_info_curso(aspirante.curso)
        nombre = aspirante.nombre + ' ' + aspirante.apellido
        curso = curso_[0][1]
        mes = curso_[0][3].month
        nombreMes = obtenerMes(mes)
        mesFin = curso_[0][4].month
        nombreMesFin = obtenerMes(mesFin)
        enviarEmail(nombre, aspirante.telefono, curso, aspirante.correo, curso_[0][3].strftime("%d de "+nombreMes+" del %Y") , curso_[0][4].strftime("%d de "+nombreMesFin+" del %Y"), curso_[0][2], curso_[0][5], curso_[0][6])
        
        return jsonify({"cargado": "Postulación realizada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Ocurrió un error: {str(e)}"}), 500

@app.route('/api/cursos_activos', methods=['GET'])
def obtener_cursos_activos_n():
    cursosSalida = []
    cursos__ = obtener_cursos_activos()
    for fila in cursos__:
                id, nombre, codigo_curso, horario, dias, fecha_inicio, fecha_fin = fila
                curso = Curso(id, nombre, codigo_curso, horario, dias, fecha_inicio, fecha_fin)
                cursosSalida.append(curso)
    return jsonify([curso.to_dict() for curso in cursosSalida])

@app.route('/api/hashearclaves', methods=['POST'])
def hashearClavesAdm():
    try:
        hashearClaves()
        return jsonify({"cargado": "Hashed"}), 200
    except Exception as e:
        return jsonify({"error": f"Ocurrió un error: {str(e)}"}), 500

@app.route('/api/crear_usuario', methods=['POST'])
def api_crear_usuario():
    try:
        data = request.get_json()

        if data.get('api_key') != API_SECRET_KEY:
            return jsonify({'error': 'Acceso no autorizado'}), 401

        nombre = data.get('nombre')
        nick = data.get('nick')
        clave_plana = data.get('clave')
        numero = data.get('numero')
        correo = data.get('correo', None) 

        if not all([nombre, nick, clave_plana]):
            return jsonify({'error': 'Faltan campos obligatorios'}), 400

        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id FROM Usuario WHERE nick = %s", (nick,))
            if cursor.fetchone():
                return jsonify({'error': 'El nombre de usuario (nick) ya existe'}), 409

            clave_hashed = bcrypt.hashpw(clave_plana.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            cursor.execute("INSERT INTO Usuario (nombre, nick, clave, correo, numero, activo) VALUES (%s, %s, %s, %s, %s,1)",
                           (nombre, nick, clave_hashed, correo, numero))
            conexion.commit()
        conexion.close()

        return jsonify({'estado': 'ok', 'mensaje': 'Usuario creado exitosamente'})

    except Exception as e:
        return jsonify({'error': f'Ocurrió un error: {str(e)}'}), 500
def get_aspirantes(offset=0, per_page=100, aspirantes=[]):
    return aspirantes[offset: offset + per_page]

def get_mensajes(offset=0, per_page=100, mensajes=[]):
    return mensajes[offset: offset + per_page]

def get_pagos(offset=0, per_page=100, pagos=[]):
    return pagos[offset: offset + per_page]

def validar_rut(rut):
	rut = rut.upper()
	rut = rut.replace("-","")
	rut = rut.replace(".","")
	aux = rut[:-1]
	dv = rut[-1:]
 
	revertido = map(int, reversed(str(aux)))
	factors = cycle(range(2,8))
	s = sum(d * f for d, f in zip(revertido,factors))
	res = (-s)%11
 
	if str(res) == dv:
		return True
	elif dv=="K" and res==10:
		return True
	else:
		return False

def hashearClaves():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, clave FROM Usuario")
        usuarios = cursor.fetchall()

        for usuario in usuarios:
            id_usuario = usuario[0]
            clave_plana = usuario[1]

            if clave_plana.startswith("$2b$"):
                continue

            clave_hashed = bcrypt.hashpw(clave_plana.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            cursor.execute("UPDATE Usuario SET clave = %s WHERE id = %s", (clave_hashed, id_usuario))

        conexion.commit()
    conexion.close()
    print("Contraseñas actualizadas exitosamente.")

# def build_otex_url(path: str) -> str:
#     """
#     Construye UrlRetoma/UrlError absolutas usando OTEC_BASE_URL (sin slash final).
#     """
#     return f"{OTEC_BASE_URL.rstrip('/')}{path}"

# # ------------------------ LOGIN SENCE UI ------------------------------
# @app.get("/login-sence")
# def login_sence_form():
#     """
#     Muestra el formulario de login SENCE para que el alumno ingrese su RUT.
#     Puedes pre-llenar cod_sence y codigo_curso con querystring:
#     /login-sence?cod_sence=1234567890&codigo_curso=CURSO-0001
#     """
#     cod_sence = (request.args.get("cod_sence") or "").strip()
#     codigo_curso = (request.args.get("codigo_curso") or "").strip()
#     return render_template("loginSence.html", cod_sence=cod_sence, codigo_curso=codigo_curso)

# @app.post("/login-sence")
# def login_sence_submit():
#     """
#     Recibe el formulario con: run_alumno, cod_sence, codigo_curso.
#     Valida y construye el POST hacia SENCE (auto-submit).
#     """
#     cod_sence = (request.form.get("cod_sence") or "").strip()
#     codigo_curso = (request.form.get("codigo_curso") or "").strip()
#     run_alumno_raw = (request.form.get("run_alumno") or "").strip()

#     # --- VALIDACIONES BACKEND ---

#     # 1️⃣ RUT chileno formato xxxxxxxx-x
#     if not re.match(r"^[0-9]{7,8}-[0-9Kk]{1}$", run_alumno_raw):
#         flash("RUT inválido. Debe tener el formato correcto (ej: 12345678-9).", "error")
#         return redirect(url_for("login_sence_form"))

#     # 2️⃣ Código SENCE (solo letras/números, máx 10)
#     if not re.match(r"^[A-Za-z0-9]+$", cod_sence) or len(cod_sence) > 10:
#         flash("Código SENCE inválido. Solo letras/números, máximo 10 caracteres.", "error")
#         return redirect(url_for("login_sence_form"))

#     # 3️⃣ Código del curso (mínimo 8, máximo 50)
#     if not (8 <= len(codigo_curso) <= 50):
#         flash("Código del curso inválido. Debe tener entre 8 y 50 caracteres.", "error")
#         return redirect(url_for("login_sence_form"))


#     # Si pasa las validaciones, continúa con el flujo normal:
#     run_alumno = normalizar_rut_formato_envio(run_alumno_raw)
#     id_sesion_alumno = generar_id_sesion_alumno()

#     # (Opcional) Si tienes validar_rut, úsala:
#     # from main import validar_rut  # si la tienes definida
#     # if not validar_rut(run_alumno):
#     #     flash("RUT inválido (DV).", "error")
#     #     return redirect(url_for("login_sence_form", cod_sence=cod_sence, codigo_curso=codigo_curso))

#     # Genera y guarda IdSesionAlumno para cotejar en el retorno
#     id_sesion_alumno = generar_id_sesion_alumno()
#     session["sence_id_sesion_alumno"] = id_sesion_alumno
#     session["sence_cod_sence"] = cod_sence
#     session["sence_codigo_curso"] = codigo_curso
#     session["sence_run_alumno"] = run_alumno

#     url_retoma = build_otex_url("/sence/callback/success")
#     url_error = build_otex_url("/sence/callback/error")

#     # Devolvemos un HTML con un form que se auto-envía por POST a SENCE
#     html = f"""
#     <html><body onload="document.forms[0].submit()">
#       <p>Redirigiendo a SENCE…</p>
#       <form action="{SENCE_LOGIN_URL}" method="POST">
#         <input type="hidden" name="RutOtec" value="{OTEC_RUT}">
#         <input type="hidden" name="Token" value="{OTEC_TOKEN}">
#         <input type="hidden" name="CodSence" value="{cod_sence}">
#         <input type="hidden" name="CodigoCurso" value="{codigo_curso}">
#         <input type="hidden" name="LineaCapacitacion" value="{SENCE_LINEA_CAPACITACION}">
#         <input type="hidden" name="RunAlumno" value="{run_alumno}">
#         <input type="hidden" name="IdSesionAlumno" value="{id_sesion_alumno}">
#         <input type="hidden" name="UrlRetoma" value="{url_retoma}">
#         <input type="hidden" name="UrlError" value="{url_error}">
#         <noscript><button type="submit">Continuar</button></noscript>
#       </form>
#     </body></html>
#     """
#     return render_template_string(html)

# # ------------------------ CALLBACKS SENCE -----------------------------
# def _validar_callback_basico(frm) -> tuple[bool, str]:
#     """
#     Valida presencia y longitud básica de campos requeridos en retorno de éxito.
#     También coteja IdSesionAlumno con el que guardamos en session.
#     """
#     required = {
#         "CodSence": 10,
#         "CodigoCurso": 50,
#         "IdSesionAlumno": 149,
#         "RunAlumno": 10,
#         "FechaHora": 19,
#         "ZonaHoraria": 100,
#         "LineaCapacitacion": 10,  # aunque sea entero, aquí llega como string
#     }
#     for k, mlen in required.items():
#         val = (frm.get(k) or "").strip()
#         if not validar_largo(val, mlen):
#             return False, f"Campo {k} inválido."

#     expected = session.get("sence_id_sesion_alumno")
#     if expected and frm.get("IdSesionAlumno") != expected:
#         return False, "La sesión del alumno no coincide (expirada o nueva ventana)."

#     return True, ""

# @app.post("/sence/callback/success")
# def sence_callback_success():
#     frm = request.form

#     ok, msg = _validar_callback_basico(frm)
#     if not ok:
#         flash(f"Retorno SENCE inválido: {msg}", "error")
#         return redirect(url_for(ERROR_REDIRECT_ENDPOINT))

#     # Extra de éxito
#     id_sesion_sence = (frm.get("IdSesionSence") or "").strip()

#     # TODO (opcional): persistir en BD auditoría del inicio de sesión SENCE
#     # registrar_inicio_sesion_sence(...)

#     flash("¡Inicio de sesión SENCE exitoso! Ya puedes continuar con tu curso.", "success")
#     return redirect(url_for(SUCCESS_REDIRECT_ENDPOINT))

# @app.post("/sence/callback/error")
# def sence_callback_error():
#     frm = request.form

#     # Validación básica (similar a éxito, pero sin exigir IdSesionSence)
#     required = {
#         "CodSence": 10,
#         "CodigoCurso": 50,
#         "IdSesionAlumno": 149,
#         "RunAlumno": 10,
#         "FechaHora": 19,
#         "ZonaHoraria": 100,
#         "LineaCapacitacion": 10,
#     }
#     for k, mlen in required.items():
#         val = (frm.get(k) or "").strip()
#         if not validar_largo(val, mlen):
#             flash(f"Retorno SENCE inválido: {k} incorrecto.", "error")
#             return redirect(url_for(ERROR_REDIRECT_ENDPOINT))

#     glosa = (frm.get("GlosaError") or "").strip()
#     mensaje = ERRORES_SENCE.get(glosa, "No fue posible iniciar sesión en SENCE. Intenta nuevamente.")

#     # TODO (opcional): persistir error para auditoría
#     # registrar_error_sence(...)

#     flash(mensaje, "error")
#     return redirect(url_for(ERROR_REDIRECT_ENDPOINT))


if __name__ == '__main__':
    app.run(port = 3000, debug = True) 