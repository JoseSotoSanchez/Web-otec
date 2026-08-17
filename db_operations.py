from bd import obtener_conexion

def obtener_cursos_activos():
    conexion = obtener_conexion()
    cursos = []
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT c.id, c.nombre, c.codigo_curso, h.rango, d.rango, c.fecha_inicio, c.fecha_fin 
                FROM Curso c 
                JOIN Horario h ON c.id_horario = h.id 
                JOIN Dias d ON c.id_dias = d.id 
                WHERE c.activo = 1 
                ORDER BY c.id DESC
            ''')
            cursos = cursor.fetchall()
    finally:
        conexion.close()
    return cursos

def verificar_postulacion_existente(rut, id_curso):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT rut, id FROM Alumno WHERE rut = %s AND id_curso = %s
            ''', (rut, id_curso))
            return cursor.fetchone()
    finally:
        conexion.close()

def registrar_aspirante(aspiranteNew, rut):
    conexion = obtener_conexion()
    telefono = aspiranteNew.telefono.strip()
    if telefono.startswith("+569"):
        telefono_final = telefono

    else:
        if len(telefono) == 8:
            telefono_final = "+569" + telefono

        elif len(telefono) == 9 and telefono.startswith("9"):
            telefono_final = "+56" + telefono

        else:
            telefono_final = "+569" + telefono[:8] 


    aspiranteNew.telefono = telefono_final
    try:
        with conexion.cursor() as cursor:
            # Insertar alumno
            cursor.execute('''
                INSERT INTO Alumno (
                    nombre, apellido, rut, sexo, edad, nacionalidad, estado_civil, email, telefono,
                    profesion, nivel_estudios, situacion_laboral, direccion, region, fecha, id_curso,
                    id_subsidio, ingreso
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), %s, 1, %s
                )
            ''', (
                aspiranteNew.nombre, aspiranteNew.apellido, rut, aspiranteNew.sexo, aspiranteNew.edad,
                aspiranteNew.nacionalidad, aspiranteNew.ecivil, aspiranteNew.correo, aspiranteNew.telefono,
                aspiranteNew.profesion, aspiranteNew.nestudios, aspiranteNew.slaboral,
                aspiranteNew.direccion, aspiranteNew.region, aspiranteNew.curso, aspiranteNew.ingreso
            ))

            id_alumno = cursor.lastrowid

            # Estado del alumno
            cursor.execute('''
                INSERT INTO Alumno_Estado (id_alumno, id_estado, fecha, id_usuario)
                VALUES (%s, 6, now(), 1)
            ''', (id_alumno,))

            # Log de usuario
            cursor.execute('''
                INSERT INTO LogUsuario (estado, fecha, ip, curso, idAlumno)
                VALUES ("postulación de curso", now(), %s, %s, %s)
            ''', (
                aspiranteNew.hostnameAddr, aspiranteNew.curso, id_alumno
            ))

        conexion.commit()
        return {
            "ok": True,
            "id_alumno": id_alumno,
            "telefono": telefono_final
        }
    finally:
        conexion.close()

def obtener_info_curso(id_curso):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT c.id, c.nombre, c.codigo_curso, c.fecha_inicio, c.fecha_fin, h.rango, d.rango
                FROM Curso c
                JOIN Horario h ON c.id_horario = h.id
                JOIN Dias d ON c.id_dias = d.id
                WHERE c.id = %s
            ''', (id_curso,))
            return cursor.fetchall()
    finally:
        conexion.close()

def insertar_log_usuario(usuario, clave, estado, ip):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                INSERT INTO LogUsuario (nick, clave, estado, fecha, ip)
                VALUES (%s, %s, %s, NOW(), %s)
            ''', (usuario, clave, estado, ip))
            conexion.commit()
    finally:
        conexion.close()

def obtener_aspirantes_por_curso(curso_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT DISTINCT 
                    a.id, a.nombre, a.apellido, a.rut, a.sexo, a.edad, a.nacionalidad, 
                    a.estado_civil, a.email, a.telefono, a.profesion, a.nivel_estudios, 
                    a.situacion_laboral, a.direccion, a.region, a.fecha, 
                    c.nombre AS nombreCurso, c.codigo_curso, 
                    ea.estado, u.nick, ea.id,
                    c.costo, a.ingreso,
                    (
                        SELECT SUM(p.monto) 
                        FROM Pagos p 
                        WHERE p.id_alumno = a.id AND p.id_curso = a.id_curso
                    ) AS total_pagos 
                FROM Alumno_Estado ae 
                JOIN Alumno a ON a.id = ae.id_alumno 
                JOIN Curso c ON a.id_curso = c.id 
                JOIN Estado_Alumno ea ON ae.id_estado = ea.id 
                JOIN Usuario u ON ae.id_usuario = u.id 
                WHERE ae.id_estado = (
                    SELECT de.id_estado 
                    FROM Alumno_Estado de 
                    WHERE id_alumno = ae.id_alumno 
                    ORDER BY de.fecha DESC 
                    LIMIT 1
                )
                AND ae.fecha = (
                    SELECT de.fecha 
                    FROM Alumno_Estado de 
                    WHERE id_alumno = ae.id_alumno 
                    ORDER BY de.fecha DESC 
                    LIMIT 1
                )
                AND c.id = %s 
                ORDER BY a.id DESC;
            ''', (curso_id,))
            return cursor.fetchall()
    finally:
        conexion.close()

def obtener_cursos():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('SELECT id, nombre, codigo_curso FROM Curso ORDER BY id DESC')
            return cursor.fetchall()
    finally:
        conexion.close()

def obtener_datos_curso_por_id(curso_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('SELECT nombre, codigo_curso, id FROM Curso WHERE id = %s', (curso_id,))
            return cursor.fetchall()
    finally:
        conexion.close()

def obtener_estados_alumno():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('SELECT id, estado FROM Estado_Alumno')
            return cursor.fetchall()
    finally:
        conexion.close()

def guardar_contacto(nombre, correo, telefono, motivo, mensaje):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                INSERT INTO Contacto(nombre, correo, telefono, motivo, mensaje, fecha)
                VALUES (%s, %s, %s, %s, %s, NOW())
            ''', (nombre, correo, telefono, motivo, mensaje))
        conexion.commit()
    finally:
        conexion.close()

def obtener_info_alumno_por_id(idalumno):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT DISTINCT
                    a.id, a.nombre, a.apellido, a.rut, a.sexo, a.edad, a.nacionalidad, a.estado_civil,
                    a.email, a.telefono, a.profesion, a.nivel_estudios, a.situacion_laboral,
                    a.direccion, a.region, a.fecha, c.nombre AS nombreCurso, c.codigo_curso,
                    ea.estado, u.nick, ea.id, c.costo, a.ingreso, c.id,
                    (SELECT SUM(p.monto)
                     FROM Pagos p
                     WHERE p.id_alumno = a.id AND p.id_curso = a.id_curso) AS total_pagos
                FROM Alumno_Estado ae
                JOIN Alumno a ON a.id = ae.id_alumno
                JOIN Curso c ON a.id_curso = c.id
                JOIN Estado_Alumno ea ON ae.id_estado = ea.id
                JOIN Usuario u ON ae.id_usuario = u.id
                WHERE ae.id_estado = (
                        SELECT de.id_estado
                        FROM Alumno_Estado de
                        WHERE id_alumno = ae.id_alumno
                        ORDER BY de.fecha DESC
                        LIMIT 1
                    )
                    AND ae.fecha = (
                        SELECT de.fecha
                        FROM Alumno_Estado de
                        WHERE id_alumno = ae.id_alumno
                        ORDER BY de.fecha DESC
                        LIMIT 1
                    )
                    AND a.id = %s
                ORDER BY a.id DESC
            ''', (idalumno,))
            return cursor.fetchall()
    finally:
        conexion.close()

def buscar_alumnos_por_nombre(nombreAlumno):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''
                SELECT DISTINCT
                    a.id, a.nombre, a.apellido, a.rut, a.sexo, a.edad, a.nacionalidad, a.estado_civil,
                    a.email, a.telefono, a.profesion, a.nivel_estudios, a.situacion_laboral,
                    a.direccion, a.region, a.fecha, c.nombre AS nombreCurso, c.codigo_curso,
                    ea.estado, u.nick, ea.id, c.costo, a.ingreso, c.id,
                    (SELECT SUM(p.monto)
                     FROM Pagos p
                     WHERE p.id_alumno = a.id AND p.id_curso = a.id_curso) AS total_pagos
                FROM Alumno_Estado ae
                JOIN Alumno a ON a.id = ae.id_alumno
                JOIN Curso c ON a.id_curso = c.id
                JOIN Estado_Alumno ea ON ae.id_estado = ea.id
                JOIN Usuario u ON ae.id_usuario = u.id
                WHERE ae.id_estado = (
                        SELECT de.id_estado
                        FROM Alumno_Estado de
                        WHERE id_alumno = ae.id_alumno
                        ORDER BY de.fecha DESC
                        LIMIT 1
                    )
                    AND ae.fecha = (
                        SELECT de.fecha
                        FROM Alumno_Estado de
                        WHERE id_alumno = ae.id_alumno
                        ORDER BY de.fecha DESC
                        LIMIT 1
                    )
                    AND (a.nombre LIKE %s OR a.apellido LIKE %s)
                ORDER BY a.id DESC
            '''
            like_param = f'%{nombreAlumno}%'
            cursor.execute(query, (like_param, like_param))
            return cursor.fetchall()
    finally:
        conexion.close()

def buscar_alumno_por_rut(rutAlumno):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''
                SELECT DISTINCT
                    a.id, a.nombre, a.apellido, a.rut, a.sexo, a.edad, a.nacionalidad, a.estado_civil,
                    a.email, a.telefono, a.profesion, a.nivel_estudios, a.situacion_laboral,
                    a.direccion, a.region, a.fecha, c.nombre AS nombreCurso, c.codigo_curso,
                    ea.estado, u.nick, ea.id, c.costo, a.ingreso, c.id,
                    (SELECT SUM(p.monto)
                     FROM Pagos p
                     WHERE p.id_alumno = a.id AND p.id_curso = a.id_curso) AS total_pagos
                FROM Alumno_Estado ae
                JOIN Alumno a ON a.id = ae.id_alumno
                JOIN Curso c ON a.id_curso = c.id
                JOIN Estado_Alumno ea ON ae.id_estado = ea.id
                JOIN Usuario u ON ae.id_usuario = u.id
                WHERE ae.id_estado = (
                        SELECT de.id_estado
                        FROM Alumno_Estado de
                        WHERE id_alumno = ae.id_alumno
                        ORDER BY de.fecha DESC
                        LIMIT 1
                    )
                    AND ae.fecha = (
                        SELECT de.fecha
                        FROM Alumno_Estado de
                        WHERE id_alumno = ae.id_alumno
                        ORDER BY de.fecha DESC
                        LIMIT 1
                    )
                    AND a.rut LIKE %s
                ORDER BY a.id DESC
            '''
            like_rut = f'%{rutAlumno}%'
            cursor.execute(query, (like_rut,))
            return cursor.fetchall()
    finally:
        conexion.close()

def buscar_alumno_por_correo(correoAlumno):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''
                SELECT DISTINCT
                    a.id, a.nombre, a.apellido, a.rut, a.sexo, a.edad, a.nacionalidad, a.estado_civil,
                    a.email, a.telefono, a.profesion, a.nivel_estudios, a.situacion_laboral,
                    a.direccion, a.region, a.fecha, c.nombre AS nombreCurso, c.codigo_curso,
                    ea.estado, u.nick, ea.id, c.costo, a.ingreso, c.id,
                    (SELECT SUM(p.monto)
                     FROM Pagos p
                     WHERE p.id_alumno = a.id AND p.id_curso = a.id_curso) AS total_pagos
                FROM Alumno_Estado ae
                JOIN Alumno a ON a.id = ae.id_alumno
                JOIN Curso c ON a.id_curso = c.id
                JOIN Estado_Alumno ea ON ae.id_estado = ea.id
                JOIN Usuario u ON ae.id_usuario = u.id
                WHERE ae.id_estado = (
                        SELECT de.id_estado
                        FROM Alumno_Estado de
                        WHERE id_alumno = ae.id_alumno
                        ORDER BY de.fecha DESC
                        LIMIT 1
                    )
                    AND ae.fecha = (
                        SELECT de.fecha
                        FROM Alumno_Estado de
                        WHERE id_alumno = ae.id_alumno
                        ORDER BY de.fecha DESC
                        LIMIT 1
                    )
                    AND a.email LIKE %s
                ORDER BY a.id DESC
            '''
            like_correo = f'%{correoAlumno}%'
            cursor.execute(query, (like_correo,))
            return cursor.fetchall()
    finally:
        conexion.close()

def obtener_aspirante_por_id(id_alumno):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT DISTINCT 
                    a.id, a.nombre, a.apellido, a.rut, a.sexo, a.edad, a.nacionalidad,
                    a.estado_civil, a.email, a.telefono, a.profesion, a.nivel_estudios,
                    a.situacion_laboral, a.direccion, a.region, a.fecha,
                    c.nombre AS nombreCurso, c.codigo_curso, ea.estado, u.nick,
                    ea.id, c.costo, a.ingreso, c.id,
                    (
                        SELECT SUM(p.monto)
                        FROM Pagos p
                        WHERE p.id_alumno = a.id AND p.id_curso = a.id_curso
                    ) AS total_pagos
                FROM Alumno_Estado ae
                JOIN Alumno a ON a.id = ae.id_alumno
                JOIN Curso c ON a.id_curso = c.id
                JOIN Estado_Alumno ea ON ae.id_estado = ea.id
                JOIN Usuario u ON ae.id_usuario = u.id
                WHERE ae.id_estado = (
                        SELECT de.id_estado
                        FROM Alumno_Estado de
                        WHERE de.id_alumno = ae.id_alumno
                        ORDER BY de.fecha DESC
                        LIMIT 1
                    )
                    AND ae.fecha = (
                        SELECT de.fecha
                        FROM Alumno_Estado de
                        WHERE de.id_alumno = ae.id_alumno
                        ORDER BY de.fecha DESC
                        LIMIT 1
                    )
                    AND a.id = %s
                ORDER BY a.id DESC
            ''', (id_alumno,))
            return cursor.fetchall()
    finally:
        conexion.close()

def registrar_pago(id_alumno, id_curso, monto, medio_pago):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                INSERT INTO Pagos(id_alumno, id_curso, monto, medio_pago, fecha)
                VALUES (%s, %s, %s, %s, NOW())
            ''', (id_alumno, id_curso, monto, medio_pago))
        conexion.commit()
    finally:
        conexion.close()

def actualizar_datos_alumno(id_alumno, nombre, apellido, email, telefono):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                UPDATE Alumno
                SET nombre = %s, apellido = %s, email = %s, telefono = %s
                WHERE id = %s
            ''', (nombre, apellido, email, telefono, id_alumno))
        conexion.commit()
    finally:
        conexion.close()

def registrar_estado_alumno(id_estado, id_alumno, id_usuario):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                INSERT INTO Alumno_Estado(id_estado, id_alumno, fecha, id_usuario)
                VALUES (%s, %s, NOW(), %s)
            ''', (id_estado, id_alumno, id_usuario))
        conexion.commit()
    finally:
        conexion.close()


