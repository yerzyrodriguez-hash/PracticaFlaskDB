from app import app, db
from flask import render_template, request, redirect, url_for
import formularios
from models import Tarea

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', subtitulo="Actividad en Grupo")

@app.route('/sobrenosotros', methods =['GET', 'POST'])
def sobrenosotros():
    formulario = formularios.formAgregarTareas()
    if formulario.validate_on_submit():
        nueva_tarea = Tarea (titulo = formulario.titulo.data)
        db.session.add(nueva_tarea)
        db.session.commit()
        print('se envio correctamente', formulario.titulo.data)
        return redirect(url_for('sobrenosotros'))
    todas_las_tareas = Tarea.query.all()
    return render_template('sobrenosotros.html', form = formulario, tareas=todas_las_tareas)

@app.route('/saludo')
def saludo():
    return 'Hola bienvenido a tallerapp'

@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Hola {nombre} bienvenido a tallerapp'

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    tarea = Tarea.query.get_or_404(id)
    formulario = formularios.formAgregarTareas()
    if request.method == 'GET':
        formulario.titulo.data = tarea.titulo
    if formulario.validate_on_submit():
        tarea.titulo = formulario.titulo.data
        db.session.commit()
        print('Se editó correctamente la tarea a:', formulario.titulo.data)
        return redirect(url_for('sobrenosotros'))
    return render_template('editar.html', form=formulario, tarea=tarea)

if __name__== '__main__' :
    app.run(debug=True)