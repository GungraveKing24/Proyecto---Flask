import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../static/database/juegos_datos.db'
db = SQLAlchemy()
db.init_app(app)

# Modelo de la tabla
class games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    juego = db.Column(db.String, nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    runN = db.Column(db.Integer, nullable=False)
    rejugando = db.Column(db.String, nullable=False)
    DatosAdicionales = db.Column(db.String, nullable=False)
    calificacion = db.Column(db.Float(precision=8, asdecimal=True), nullable=False)
    img = db.Column(db.String, nullable=True)
    fecha_finalizado = db.Column(db.Date, nullable=True)

@app.route('/')
def index():

    # Consulta SQL para obtener todos los juegos
    Juegos = games.query.all()
    
    # Renderizar la plantilla HTML y pasar la lista de imágenes como argumento
    return render_template('index.html', titulo='Practica Flask', Juegos=Juegos)

@app.route('/search')
def search():
    search_query = request.args.get('search_query', '')  # Obtener el término de búsqueda del query string
    if search_query:
        # Filtrar los juegos por el término de búsqueda
        Juegos = games.query.filter(games.juego.ilike(f'%{search_query}%')).all()
    else:
        # Si no se proporciona ningún término de búsqueda, mostrar todos los juegos
        Juegos = games.query.all()
    
    return render_template('index.html', titulo='Practica Flask', Juegos=Juegos)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Obtener los datos del formulario
        juego = request.form['juego']
        estado = request.form['estado']
        runN = int(request.form['runN'])
        rejugando = request.form['rejugando']
        DatosAdicionales = request.form['DatosAdicionales']
        calificacion = float(request.form['calificacion'])
        img = request.form['img']
        fecha_finalizado_str = request.form['fecha_finalizado']
        fecha_finalizado = datetime.strptime(fecha_finalizado_str, '%Y-%m-%d') if fecha_finalizado_str else None
        
        # Crear un nuevo objeto Game con los datos del formulario
        new_game = games(juego=juego, estado=estado, runN=runN, rejugando=rejugando, DatosAdicionales=DatosAdicionales,
                        calificacion=calificacion, img=img, fecha_finalizado=fecha_finalizado)
        
        # Agregar el nuevo juego a la base de datos
        db.session.add(new_game)
        db.session.commit()
        
        return redirect(url_for('index'))  # Redirigir a la página principal después de crear el registro
    else:
        # Obtener los estados disponibles desde la base de datos
        estados_disponibles = games.query.with_entities(games.estado).distinct().all()
        estados = [estado[0] for estado in estados_disponibles]
        
        return render_template('create.html', estados=estados)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_game(id):
    # Buscar el juego por su ID
    juego = games.query.get_or_404(id)
    
    # Eliminar el juego de la base de datos
    db.session.delete(juego)
    db.session.commit()

    # Redirigir a la página principal después de la eliminación exitosa
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)