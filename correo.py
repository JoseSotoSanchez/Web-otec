import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage

def enviarEmail(nombre, telefono, curso, correo):
    curso = curso.replace("-", " ").capitalize()
    nombre = nombre.capitalize()
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
            <td align="center" style="background:#dd9b6d94;">
              <img src="http://iccapacitacionlaboral.cl/static/Imagenes/logo-3.png" alt="" width="300" style="height:auto;display:block;" />
            </td>
          </tr>
          <tr>
            <td style="padding:36px 30px 42px 30px;">
              <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;">
                <tr>
                  <td style="padding:0 0 36px 0;color:#153643;">
                    <h1 style="font-size:24px;margin:0 0 20px 0;font-family:Arial,sans-serif;">Estimado """+nombre+"""</h1>
                    <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"> Su postulación al curso de su interés se hizo de forma correcta, usaremos los siguientes datos para comunicarnos con usted.</p>
                    <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Nombre:</strong> """+nombre+"""</p>
                    <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Teléfono:</strong> """+telefono+"""</p>
                    <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Email:</strong> """+correo+"""</p>
                    <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif; text-align:center; "><strong> Curso:</strong> """+curso+"""</p>
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
            <td style="padding:30px;background:#dd9b6d;">
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