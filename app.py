from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask.globals import request
from flask import  redirect 
from flask import  url_for
from flask import  flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#Conexion base de datos
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] ='root'
app.config['MYSQL_PASSWORD'] ='admi'
app.config['MYSQL_DB'] ='registro'
mysql=MySQL(app)


# Sesion
app.secret_key = 'mysecretkey'

#Funciones
#Inicio de pagina
@app.route('/')
def index():
    return render_template('index.html')

#
@app.route('/agregar', methods = ['POST'])
def agregar():
    if request.method == 'POST':
        #guardando las  variables en los valores
        dni = request.form['dni']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        email = request.form['email']
        #Insertar a mysql
        cur = mysql.connection.cursor()
        #Insertar consulta
        cur.execute('INSERT INTO contactos (dni, nombre, apellido, telefono, direccion, email) VALUES (%s, %s, %s, %s, %s, %s)',
        (dni, nombre, apellido,telefono, direccion, email))
        #Ejecucion de consulta
        mysql.connection.commit()
        #Mensaje
        #Redireccionar a una url
        return redirect(url_for('control'))

@app.route('/editar/<dni>')
def editar(dni):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos WHERE dni = %s', [dni])
    contactos= cur.fetchall()
    return render_template('inicio.html', contactos = contactos[0])

@app.route('/actualizar/<dni>', methods = ['POST'])
def actualizar(dni):
    if request.method == 'POST':
        #guardado en variables
        dnis = dni
        dni = request.form['dni']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        email = request.form['email']
        
        cur = mysql.connection.cursor()
        cur.execute(""" 
            UPDATE contactos
            SET dni = %s,
                nombre = %s,
                apellido = %s,
                telefono = %s,
                direccion = %s,
                email = %s
            WHERE dni = %s
        """, (dni, nombre, apellido, telefono, direccion, email, dnis))
        mysql.connection.commit()
        return redirect(url_for('control'))

@app.route('/eliminar/<dni>')
def eliminar(dni):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contactos WHERE dni = %s', [dni])
    mysql.connection.commit()
    return redirect(url_for('control'))

@app.route('/control')
def control():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos')
    contactos = cur.fetchall()
    return render_template('control.html', contactos = contactos)


if __name__ == "__main__":
    app.run(debug=True)    