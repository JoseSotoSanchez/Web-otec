from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'otec'

mysql = MySQL(app)

@app.route('/')
def Index():
    return render_template('navegador.html')

@app.route('/inicio')
def Inicio():
    return render_template('inicio.html')

@app.route('/cursos')
def Cursos():
    return render_template('cursos.html')
if __name__ == '__main__':
    app.run(port = 3000, debug = True) 

