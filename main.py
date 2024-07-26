from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuración de la base de datos usando variables de entorno
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://x2:1234@localhost/flask_app')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la extensión SQLAlchemy
db = SQLAlchemy(app)

# Definir un modelo
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'

# Crear las tablas en la base de datos y agregar un usuario de prueba
with app.app_context():
    db.create_all()
    if not Usuario.query.first():
        usuario_prueba = Usuario(nombre='Prueba', email='prueba@example.com')
        db.session.add(usuario_prueba)
        db.session.commit()

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/usuarios/<int:id>')
def obtener_usuario(id):
    usuario = db.session.get(Usuario, id)
    if usuario:
        return {'id_usuario': usuario.id, 'nombre_usuario': usuario.nombre}
    else:
        return {'message': 'Usuario no encontrado'}, 404
    

@app.route('/usuarios/total')
def total_usuarios():
    total = Usuario.query.count()
    arrayUsuarios = [{'id_usuario': usuario.id, 'nombre_usuario': usuario.nombre} for usuario in Usuario.query.all()]
    return {'total_usuarios': total, 'usuarios': arrayUsuarios}

if __name__ == '__main__':
    app.run(debug=True)