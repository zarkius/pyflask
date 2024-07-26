from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

def mapear_rutas(app):
    rutas = app.url_map.iter_rules()
    rutas = list(map(lambda ruta: {'ruta': str(ruta)}, rutas))
    return {'rutas': rutas}

# Configuración de la base de datos usando variables de entorno
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://X2:1234@localhost/flask_app')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/usuarios/<int:id>')
def obtener_usuario(id):
    usuario = Usuario.query.get(id)
    if usuario:
        return {'id': usuario.id, 'nombre': usuario.nombre, 'email': usuario.email}
    else:
        return {'message': 'Usuario no encontrado'}, 404

# Inicializar la extensión SQLAlchemy
db = SQLAlchemy(app)

# Definir un modelo
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'

@app.route('/usuarios')
def usuarios():
    usuarios = Usuario.query.all()
    usuarios = list(map(lambda usuario: {'id': usuario.id, 'nombre': usuario.nombre, 'email': usuario.email}, usuarios))
    return {'usuarios': usuarios}

@app.route('/rutas')
def generar_mapa():
    rutas = app.url_map.iter_rules()
    rutas = list(map(lambda ruta: {'ruta': str(ruta)}, filter(lambda r: not str(r).startswith('/static'), rutas)))
    return {'rutas': rutas}

if __name__ == '__main__':
    app.run(debug=True)