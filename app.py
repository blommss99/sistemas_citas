from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)

# Archivos donde se guardan los datos
PACIENTES_FILE = 'data/pacientes.json'
CITAS_FILE = 'data/citas.json'

# Funciones auxiliares
def cargar_datos(archivo):
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def guardar_datos(archivo, datos):
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/registrar_paciente', methods=['GET', 'POST'])
def registrar_paciente():
    pacientes = cargar_datos(PACIENTES_FILE)
    if request.method == 'POST':
        nuevo = {
            'nombre': request.form['nombre'],
            'cedula': request.form['cedula'],
            'telefono': request.form['telefono'],
            'correo': request.form['correo']
        }
        pacientes.append(nuevo)
        guardar_datos(PACIENTES_FILE, pacientes)
        return redirect(url_for('inicio'))
    return render_template('registrar_paciente.html')

@app.route('/agendar_cita', methods=['GET', 'POST'])
def agendar_cita():
    citas = cargar_datos(CITAS_FILE)
    pacientes = cargar_datos(PACIENTES_FILE)
    if request.method == 'POST':
        nueva_cita = {
            'paciente': request.form['paciente'],
            'fecha': request.form['fecha'],
            'hora': request.form['hora'],
            'medico': request.form['medico']
        }
        citas.append(nueva_cita)
        guardar_datos(CITAS_FILE, citas)
        return redirect(url_for('listar_citas'))
    return render_template('agendar_cita.html', pacientes=pacientes)

@app.route('/listar_citas')
def listar_citas():
    citas = cargar_datos(CITAS_FILE)
    return render_template('listar_citas.html', citas=citas)

if __name__ == '__main__':
    app.run(debug=True)
