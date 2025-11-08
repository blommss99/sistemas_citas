from flask import Flask, render_template, request, redirect, url_for, flash
import json, os
import uuid  # IDs únicos

app = Flask(__name__)
app.secret_key = "supersecreto123"

# Archivos de datos
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

# Página principal
@app.route('/')
def inicio():
    return render_template('index.html')

# Registrar paciente
@app.route('/registrar_paciente', methods=['GET', 'POST'])
def registrar_paciente():
    pacientes = cargar_datos(PACIENTES_FILE)
    if request.method == 'POST':
        nuevo = {
            'id': str(uuid.uuid4()),
            'nombre': request.form['nombre'],
            'cedula': request.form['cedula'],
            'telefono': request.form['telefono'],
            'correo': request.form['correo']
        }
        pacientes.append(nuevo)
        guardar_datos(PACIENTES_FILE, pacientes)
        flash("Paciente registrado correctamente ✅")
        return redirect(url_for('inicio'))
    return render_template('registrar_paciente.html')

# ✅ Listar pacientes (único, sin duplicados)
@app.route('/listar_pacientes')
def listar_pacientes():
    pacientes = cargar_datos(PACIENTES_FILE)
    return render_template('listar_pacientes.html', pacientes=pacientes)

# Eliminar paciente
@app.route('/eliminar_paciente/<string:id>')
def eliminar_paciente(id):
    pacientes = cargar_datos(PACIENTES_FILE)
    paciente_a_eliminar = next((p for p in pacientes if p['id'] == id), None)

    if paciente_a_eliminar:
        pacientes.remove(paciente_a_eliminar)
        guardar_datos(PACIENTES_FILE, pacientes)
        flash(f"Paciente {paciente_a_eliminar['nombre']} eliminado correctamente.")
    else:
        flash("Paciente no encontrado", "error")

    return redirect(url_for('listar_pacientes'))

# Agendar cita
@app.route('/agendar_cita', methods=['GET', 'POST'])
def agendar_cita():
    citas = cargar_datos(CITAS_FILE)
    pacientes = cargar_datos(PACIENTES_FILE)
    if request.method == 'POST':
        nueva_cita = {
            'id': str(uuid.uuid4()),
            'paciente': request.form['paciente'],
            'fecha': request.form['fecha'],
            'hora': request.form['hora'],
            'motivo': request.form['motivo']
        }
        citas.append(nueva_cita)
        guardar_datos(CITAS_FILE, citas)
        flash("Cita agendada correctamente ✅")
        return redirect(url_for('inicio'))
    return render_template('agendar_cita.html', pacientes=pacientes)

# Listar citas
@app.route('/listar_citas')
def listar_citas():
    citas = cargar_datos(CITAS_FILE)
    return render_template('listar_citas.html', citas=citas)

# Eliminar cita
@app.route('/eliminar_cita/<string:id>')
def eliminar_cita(id):
    citas = cargar_datos(CITAS_FILE)
    cita_a_eliminar = next((c for c in citas if c.get('id') == id), None)

    if cita_a_eliminar:
        citas.remove(cita_a_eliminar)
        guardar_datos(CITAS_FILE, citas)
        flash(f"Cita de {cita_a_eliminar['paciente']} eliminada correctamente.")
    else:
        flash("Cita no encontrada", "error")

    return redirect(url_for('listar_citas'))

# Ejecutar
if __name__ == '__main__':
    if not os.path.exists('data'):
        os.makedirs('data')

    if not os.path.exists(PACIENTES_FILE):
        guardar_datos(PACIENTES_FILE, [])

    if not os.path.exists(CITAS_FILE):
        guardar_datos(CITAS_FILE, [])

    app.run(debug=True)




