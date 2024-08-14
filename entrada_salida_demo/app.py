from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from datetime import datetime
from app import app as application


app = Flask(__name__)

# Configuración de la aplicación
app.config['MAIL_SERVER'] = 'smtp.tuservidor.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'lcb200117@gmail.com'
app.config['MAIL_PASSWORD'] = 'pwrl bxgd vgqn boyq'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# Archivos para registrar las marcas e inconsistencias
LOG_FILE = 'marcas.txt'
INCONSISTENCIA_FILE = 'inconsistencias.txt'

def registrar_marca(tipo):
    with open(LOG_FILE, 'a') as file:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{now} - {tipo}\n")

def registrar_inconsistencia(tipo_inconsistencia, correo_destinatario):
    with open(INCONSISTENCIA_FILE, 'a') as file:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{now} - Inconsistencia: {tipo_inconsistencia}, Correo: {correo_destinatario}\n")

# Ruta para la página principal
@app.route('/')
def index():
    numero_identificacion = "305320334"  # Número de identificación del empleado

    try:
        with open(LOG_FILE, 'r') as file:
            marcas = file.readlines()
    except FileNotFoundError:
        marcas = []

    try:
        with open(INCONSISTENCIA_FILE, 'r') as file:
            inconsistencias = file.readlines()
    except FileNotFoundError:
        inconsistencias = []

    return render_template('index.html', marcas=marcas, inconsistencias=inconsistencias, numero_identificacion=numero_identificacion)

# Ruta para registrar la entrada/salida y redirigir a inconsistencias
@app.route('/marcar', methods=['POST'])
def marcar():
    tipo = request.form['tipo']
    registrar_marca(tipo)
    # Redirigir al formulario de inconsistencias sin tipo prellenado
    return redirect(url_for('mostrar_inconsistencia'))

# Ruta para mostrar el formulario de inconsistencias
@app.route('/inconsistencia', methods=['GET'])
def mostrar_inconsistencia():
    return render_template('inconsistencia.html')

# Ruta para enviar inconsistencias
@app.route('/enviar_inconsistencia', methods=['POST'])
def enviar_inconsistencia():
    tipo_inconsistencia = request.form['tipo_inconsistencia']
    correo_destinatario = request.form['correo_destinatario']
    
    # Registrar la inconsistencia antes de enviarla
    registrar_inconsistencia(tipo_inconsistencia, correo_destinatario)
    
    msg = Message("Inconsistencia Reportada",
                  sender="lcb200117@gmail.com",
                  recipients=[correo_destinatario])
    msg.body = f"Tipo de inconsistencia: {tipo_inconsistencia}"
    
    try:
        mail.send(msg)
        return redirect(url_for('index', mensaje="Inconsistencia enviada con éxito."))
    except Exception as e:
        return redirect(url_for('index', mensaje=f"Error al enviar el correo: {str(e)}"))

if __name__ == '__main__':
    app.run(debug=True)
