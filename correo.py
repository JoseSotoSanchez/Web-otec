import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage

def enviarEmail(nombre, telefono, curso, correo, inicio, fin, codigoCurso, horario, dias):
    curso = upperFirst(curso.replace("-", " ").lower())
    nombre = upperFirst(nombre.lower())
    email_user = 'postulaciones@iccapacitacionlaboral.cl'
    email_password = '$$PKhg!pB'

    email_send = correo
    subject = "Postulación exitosa al curso "+curso+""
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject
    h = str("Holder")
    c = str("course")
    t = str("trainer")
    html = """\
    <!DOCTYPE html>
 <html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width,initial-scale=1">
      <meta name="x-apple-disable-message-reformatting">
      <title></title>
      <style>
        table, td, div, h1, p 
      </style>
    </head>
    <body style="margin:0;padding:0;">
      <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;background:#ffffff;">
        <tr>
          <td align="center" style="padding:0;">
            <table role="presentation" style="width:602px;border-collapse:collapse;border:1px solid #cccccc;border-spacing:0;text-align:left;">
              <tr>
                <td align="center" style="background:#1c68c4;">
                  <img src="http://iccapacitacionlaboral.cl/static/Imagenes/logo-ic-capacitacion-1.png" alt="" width="300" style="height:auto;display:block;" />
                </td>
              </tr>
              <tr>
                <td style="padding:36px 30px 42px 30px;">
                  <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;">
                    <tr>
                      <td style="padding:0 0 36px 0;color:#153643;">
                        <h1 style="font-size:24px;margin:0 0 20px 0;font-family:Arial,sans-serif;">Estimado (a) """+nombre+"""</h1>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"> Su postulación al curso de su interés se hizo de forma correcta, usaremos los siguientes datos para comunicarnos con usted.</p>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Nombre:</strong> """+nombre+"""</p>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Teléfono:</strong> """+telefono+"""</p>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Email:</strong> """+correo+"""</p>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Curso:</strong> """+curso+""" ("""+codigoCurso+""")</p>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Horario:</strong> """+horario+""" - """+dias+"""</p>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Fecha Inicio:</strong> """+inicio+"""</p>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Fecha Fin:</strong> """+fin+"""</p>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"> Un coordinador se comunicará vía e-mail, llamado telefónico o whatsapp y le indicará los pasos a seguir para formalizar su matrícula.</p>
                          <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"> Si la información enviada es incorrecta enviar correo a <a href="mailto:postulaciones@iccapacitacionlaboral.cl?Subject=Cambio%20de%20información">postulaciones@iccapacitacionlaboral.cl</a> para modificar sus datos.</p>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:0;">
                        <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;">
                        </table>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
              <tr>
                <td style="padding:30px;background:#0a73b9;">
                  <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;font-size:9px;font-family:Arial,sans-serif;">
                    <tr>
                      <td style="padding:0;width:70%;" align="left">
                        <p style="margin:0;font-size:14px;line-height:20px;font-family:Arial,sans-serif;color:#ffffff;"> La información recopilada es de carácter confidencial.<br/>
                        </p>
                      </td>
                      <td style="padding:0;width:50%;" align="right">
                        <table role="presentation" style="border-collapse:collapse;border:0;border-spacing:0;">
                          <tr>
                            <td style="padding:0 0 0 10px;width:38px;">
                              <a href="https://api.whatsapp.com/send?phone=56920742757" style="color:#ffffff;"><img src="http://assets.stickpng.com/images/580b57fcd9996e24bc43c543.png" alt="Twitter" width="38" style="height:auto;display:block;border:0;" /></a>
                            </td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
  </html>
    """.format(h=h , c=c , t=t) 
        
    msg.attach(MIMEText(html,'html'))
    server = smtplib.SMTP('iccapacitacionlaboral.cl',25)
    server.starttls()
    server.login(email_user,email_password)
    server.sendmail(email_user,email_send,msg.as_string())
    server.quit()

def enviarEmailAceptacion(nombre, correo, nombreCurso, inicioCurso, finCurso, diasCurso, horarioCurso, modalidad, urlPago, nombreUsuario, correoUsuario, numeroUsuario):
    nombre = upperFirst(nombre.lower())
    email_user = 'postulaciones@iccapacitacionlaboral.cl'
    email_password = '$$PKhg!pB'

    email_send = correo
    subject = "Financiamiento Programa Emplea (Curso capacitación Laboral)"
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject
    h = str("Holder")
    c = str("course")
    t = str("trainer")
    html = """\
   <!DOCTYPE html>
 <html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width,initial-scale=1">
      <meta name="x-apple-disable-message-reformatting">
      <title></title>
      <style>
        table, td, div, h1, p 
      </style>
    </head>
    <body style="margin:0;padding:0;">
      <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;background:#ffffff;">
        <tr>
          <td align="center" style="padding:0;">
            <table role="presentation" style="width:602px;border-collapse:collapse;border:1px solid #cccccc;border-spacing:0;text-align:left;">
              <tr>
                <td align="center" style="background:#1c68c4;">
                  <img src="http://iccapacitacionlaboral.cl/static/Imagenes/logo-ic-capacitacion-1.png" alt="" width="300" style="height:auto;display:block;" />
                </td>
              </tr>
              <tr>
                <td style="padding:36px 30px 42px 30px;">
                  <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;">
                    <tr>
                      <td style="padding:0 0 36px 0;color:#153643;">
                        <h1 style="font-size:35px;margin:0 0 20px 0;font-family:Arial,sans-serif; color:#1c68c4; text-align:center;">FELICITACIONES</h1>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"> Estimado (a) <strong>"""+nombre+"""</strong> IC Capacitación agradece su preferencia y confianza, esperando cumplir con sus expectativas de desarrollo e ingreso a un mejor campo laboral.</p>
                           <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"> Hemos revisado su postulación y nos es grato informar a usted que ha sido seleccionada con beneficio de subvención, la que considera un descuento que asciende al 75% del valor del curso, debiendo pagar solo la suma de <strong>$85.000.-</strong> pesos</p>
                           <h1 style="font-size:17px;margin:0 0 20px 0;font-family:Arial,sans-serif;">Detalles del curso:</h1>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Nombre:</strong> """+nombreCurso+"""</p>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Fecha Inicio:</strong> """+inicioCurso+"""</p>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Fecha Termino:</strong> """+finCurso+"""</p>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Dias:</strong> """+diasCurso+"""</p>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Horario:</strong> """+horarioCurso+""" </p>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Modalidad:</strong> """+modalidad+"""</p>
                        <h1 style="font-size:17px;margin:0 0 20px 0;font-family:Arial,sans-serif;">El curso incluye:</h1>
                        <ol style="font-family:Arial,sans-serif;">
                          <li>Certificación digital con validación código QR</li>
                          <li>Descuento de 75% del valor del curso</li>
                          <li><strong>Taller de Inserción Laboral</strong> (“CREATIVIDAD Y CONSEJOS PARA ENCONTRAR TRABAJO”)</li>
                          <li>Beneficios adicionales ( verificar con el coordinador del curso si corresponde según curso realizado)</li>
                        </ol>	
                        <h1 style="font-size:17px;margin:0 0 20px 0;font-family:Arial,sans-serif;">Pago:</h1>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"> Mediante transferencia bancaria a: </p>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Titular:</strong> Instituto de Capacitación Laboral Spa</p>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Rut:</strong> 77.558.994-9</p>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Banco:</strong> Banco De Chile</p>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Tipo:</strong> Cuenta Corriente</p>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Numero:</strong> 8005934800</p>
                      <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"> Boton de pago: </p>
                      <p align="center">
                      <a style="background-color: #1c68c4; color: white; padding: 13px 32px; text-align: center;text-decoration: none; display: inline-block; font-size: 20px; margin: 4px 2px; cursor: pointer; border-radius: 11px;" href=\""""+urlPago+"""\">Pagar</a>  
                      <p align="center">
                      <img src="http://iccapacitacionlaboral.cl/static/Imagenes/red-compra.png" alt="" width="300" style="height:auto;display:block;" align="center" /></p>
                      </td>
                      
                    </tr>
                    <tr>
                      <td style="padding:0;">
                        <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;">
                        </table>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
              <tr>
                <td style="padding:30px;background:#0a73b9;">
                  <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;font-size:9px;font-family:Arial,sans-serif;">
                    <tr>
                      <td style="padding:0;width:70%;" align="left">
                        <p style="margin:0;font-size:14px;line-height:20px;font-family:Arial,sans-serif;color:#ffffff;"> La información recopilada es de carácter confidencial.<br/>
                        </p>
                      </td>
                      <td style="padding:0;width:50%;" align="right">
                        <table role="presentation" style="border-collapse:collapse;border:0;border-spacing:0;">
                          <tr>
                            <td style="padding:0 0 0 10px;width:38px;">
                              <a href="https://api.whatsapp.com/send?phone=56920742757" style="color:#ffffff;"><img src="http://assets.stickpng.com/images/580b57fcd9996e24bc43c543.png" alt="Twitter" width="38" style="height:auto;display:block;border:0;" /></a>
                            </td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    <footer style="margin-top:100px">
    <h1 style="font-size:14px;margin:0 0 2px 0;font-family:Arial,sans-serif;font-style: oblique; color:#515A5A">"""+nombreUsuario+"""</h1>
     <h1 style="font-size:17px;margin:0 0 2px 0;font-family:Arial,sans-serif;font-style: oblique; color:#515A5A">Coordinador de Curso IC capacitación Laboral</h1>
     <p style="margin:0 0 2px 0;font-size:14px;line-height:24px;font-family:Arial,sans-serif;font-style: oblique;"> """+correoUsuario+"""</p>
     <h1 style="font-size:14px;margin:0 0 2px 0;font-family:Arial,sans-serif;font-style: oblique; color:#515A5A">contacto: """+numeroUsuario+""" Whatsapp</h1>
     <p  style="font-size:14px;margin:0 0 2px 0"><a href="url">iccapacitacionlaboral.cl</a></p>
                        <table role="presentation" style="border-collapse:collapse;border:0;border-spacing:0;">
                          <tr>
                              <td><img src="http://iccapacitacionlaboral.cl/static/Imagenes/correo1.png" alt=".." width="130" style="height:auto;display:block;border:0;" />
                            </td>
                            <td><img src="http://iccapacitacionlaboral.cl/static/Imagenes/correo2.jpg" alt=".." width="130" style="height:auto;display:block;border:0;" />
                            </td>
                            <td><img src="http://iccapacitacionlaboral.cl/static/Imagenes/correo3.jpg" alt=".." width="100" style="height:auto;display:block;border:0;" />
                            </td>
                          </tr>
                        </table>
    </footer>
  </html>
    """.format(h=h , c=c , t=t) 
        
    msg.attach(MIMEText(html,'html'))
    server = smtplib.SMTP('iccapacitacionlaboral.cl',25)
    server.starttls()
    server.login(email_user,email_password)
    server.sendmail(email_user,email_send,msg.as_string())
    server.quit()

def enviarEmailPago(nombre, correo, nombreCurso, codigoCurso, montoCurso, medioPago, nombreUsuario, correoUsuario, numeroUsuario):
    nombre = upperFirst(nombre.lower())
    email_user = 'pagos@iccapacitacionlaboral.cl'
    email_password = '@Pagos2022'

    email_send = correo
    subject = "Aviso de pago recibido"
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject
    h = str("Holder")
    c = str("course")
    t = str("trainer")
    html = """\
   <!DOCTYPE html>
 <html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width,initial-scale=1">
      <meta name="x-apple-disable-message-reformatting">
      <title></title>
      <style>
        table, td, div, h1, p 
      </style>
    </head>
    <body style="margin:0;padding:0;">
      <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;background:#ffffff;">
        <tr>
          <td align="center" style="padding:0;">
            <table role="presentation" style="width:602px;border-collapse:collapse;border:1px solid #cccccc;border-spacing:0;text-align:left;">
              <tr>
                <td align="center" style="background:#1c68c4;">
                  <img src="http://iccapacitacionlaboral.cl/static/Imagenes/logo-ic-capacitacion-1.png" alt="" width="300" style="height:auto;display:block;" />
                </td>
              </tr>
              <tr>
                <td style="padding:36px 30px 42px 30px;">
                  <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;">
                    <tr>
                      <td style="padding:0 0 36px 0;color:#153643;">
                        <h1 style="font-size:30px;margin:0 0 20px 0;font-family:Arial,sans-serif; color:#1c68c4; text-align:center;">GRACIAS POR SU PAGO</h1>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"> Estimado (a) <strong>"""+nombre+"""</strong> IC Capacitación agradece su preferencia y confianza, esperando cumplir con sus expectativas de desarrollo e ingreso a un mejor campo laboral.</p>
                           
                           <h1 style="font-size:17px;margin:0 0 20px 0;font-family:Arial,sans-serif;">Detalles del pago:</h1>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Concepto:</strong> Pago Curso</p>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Cohorte - curso:</strong> """+codigoCurso+""" / """+nombreCurso+"""</p>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Monto:</strong> """+montoCurso+"""</p>
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Medio de pago:</strong> """+medioPago+"""</p>
                        
                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"> Si considera algún error en los datos, por favor responder a este correo para realizar la revisión y ajuste correspondiente.</p>
                         <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"> Esperamos que el curso cumpla con todas sus expectativas.</p>
                      
                        <p style="margin:0 0 12px 0;font-size:14px;line-height:24px;font-family:Arial,sans-serif;"> Atentamente: </p>
                       <p style="margin:0 0 12px 0;font-size:13px;line-height:24px;font-family:Arial,sans-serif;"> Equipo técnico IC Capacitación Laboral</p>
                      
                    </tr>
                  </table>
                </td>
              </tr>
              <tr>
                <td style="padding:30px;background:#0a73b9;">
                  <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;font-size:9px;font-family:Arial,sans-serif;">
                    <tr>
                      <td style="padding:0;width:70%;" align="left">
                        <p style="margin:0;font-size:14px;line-height:20px;font-family:Arial,sans-serif;color:#ffffff;"> La información es de carácter confidencial.<br/>
                        </p>
                      </td>
                      <td style="padding:0;width:50%;" align="right">
                        <table role="presentation" style="border-collapse:collapse;border:0;border-spacing:0;">
                          <tr>
                            <td style="padding:0 0 0 10px;width:38px;">
                              <a href="https://api.whatsapp.com/send?phone=56920742757" style="color:#ffffff;"><img src="http://assets.stickpng.com/images/580b57fcd9996e24bc43c543.png" alt="Twitter" width="38" style="height:auto;display:block;border:0;" /></a>
                            </td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    <footer style="margin-top:100px">
    <h1 style="font-size:14px;margin:0 0 2px 0;font-family:Arial,sans-serif;font-style: oblique; color:#515A5A">"""+nombreUsuario+"""</h1>
     <h1 style="font-size:17px;margin:0 0 2px 0;font-family:Arial,sans-serif;font-style: oblique; color:#515A5A">Coordinador de Curso IC capacitación Laboral</h1>
     <p style="margin:0 0 2px 0;font-size:14px;line-height:24px;font-family:Arial,sans-serif;font-style: oblique;"> """+correoUsuario+"""</p>
     <h1 style="font-size:14px;margin:0 0 2px 0;font-family:Arial,sans-serif;font-style: oblique; color:#515A5A">contacto: """+numeroUsuario+""" Whatsapp</h1>
     <p  style="font-size:14px;margin:0 0 2px 0"><a href="url">iccapacitacionlaboral.cl</a></p>
                        <table role="presentation" style="border-collapse:collapse;border:0;border-spacing:0;">
                          <tr>
                              <td><img src="http://iccapacitacionlaboral.cl/static/Imagenes/correo1.png" alt=".." width="130" style="height:auto;display:block;border:0;" />
                            </td>
                            <td><img src="http://iccapacitacionlaboral.cl/static/Imagenes/correo2.jpg" alt=".." width="130" style="height:auto;display:block;border:0;" />
                            </td>
                            <td><img src="http://iccapacitacionlaboral.cl/static/Imagenes/correo3.jpg" alt=".." width="100" style="height:auto;display:block;border:0;" />
                            </td>
                          </tr>
                        </table>
    </footer>
  </html>
    """.format(h=h , c=c , t=t) 
        
    msg.attach(MIMEText(html,'html'))
    server = smtplib.SMTP('iccapacitacionlaboral.cl',25)
    server.starttls()
    server.login(email_user,email_password)
    server.sendmail(email_user,email_send,msg.as_string())
    server.quit()

def upperFirst(texto):
  salida = ''
  texto_ = texto.strip()
  lista = texto_.split()
  for n in lista:
    salida += ' '+ n.capitalize()
  salida.strip()
  return salida

def obtenerMes(numeroMes):
  int(numeroMes)
  salida = ''
  if numeroMes == 1:
    salida = 'Enero'
  if numeroMes == 2:
    salida = 'Febrero'
  if numeroMes == 3:
    salida = 'Marzo'
  if numeroMes == 4:
    salida = 'Abril'
  if numeroMes == 5:
    salida = 'Mayo'
  if numeroMes == 6:
    salida = 'Junio'
  if numeroMes == 7:
    salida = 'Julio'
  if numeroMes == 8:
    salida = 'Agosto'
  if numeroMes == 9:
    salida = 'Septiembre'
  if numeroMes == 10:
    salida = 'Octubre'
  if numeroMes == 11:
    salida = 'Noviembre'
  if numeroMes == 12:
    salida = 'Diciembre'
  return salida