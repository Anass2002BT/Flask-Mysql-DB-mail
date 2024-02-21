from flask import Flask, render_template, request, redirect, url_for
from appdb import conectar_bd  # Asumiendo que tienes una función conectar_bd en appdb
import mysql.connector

app = Flask(__name__, template_folder='template')

# Ruta para el formulario
@app.route('/')
def formulario():
    return render_template('base.html', estilos=url_for('static', filename='estilos.css'), template='formulario')

# Ruta para manejar la consulta de correo
@app.route('/getmail', methods=['GET','POST'])
def getmail():
    if request.method == 'POST':
        nombre = request.form['nombre']
        try:
            with conectar_bd() as mydb:
                cur = mydb.cursor(dictionary=True)
                cur.execute("SELECT correo FROM usuarios WHERE nombre = %s", (nombre,))
                result = cur.fetchone()
        except mysql.connector.Error as err:
            return f"Error al consultar la base de datos: {err}"
        else:
            if result:
                email = result['correo']
                return render_template('base.html', nombre=nombre, email=email, template='resultado')
            else:
                mensaje = f"No se encontró un correo electrónico para el nombre: {nombre}"
                return render_template('base.html', mensaje=mensaje, template='resultado')

# Ruta para agregar correo electrónico
@app.route('/addmail', methods=['GET', 'POST'])
def addmail():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        try:
            with conectar_bd() as mydb:
                cur = mydb.cursor()
                cur.execute("INSERT INTO usuarios (nombre, correo) VALUES (%s, %s)", (nombre, email))
                mydb.commit()
        except mysql.connector.Error as err:
            return f"Error al insertar en la base de datos: {err}"
        else:
            # Redirigir a la página de éxito después de agregar el correo electrónico
            return redirect(url_for('addmail_exito'))
    return render_template('1.addmail.html', estilos=url_for('static', filename='estilos.css'))

# Ruta para la página de éxito después de agregar correo electrónico
@app.route('/admail_exito')
def addmail_exito():
    return render_template('1.addmail_exito.html', estilos=url_for('static', filename='estilos.css'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
