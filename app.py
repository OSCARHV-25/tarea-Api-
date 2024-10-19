from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#  base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://oscar:5592@localhost:3306/bd_tarea'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definir el modelo de Estudiante
class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'edad': self.edad
        }

# Crear estudiante
@app.route('/estudiante', methods=['POST'])
def crear_estudiante():
    body = request.get_json()
    nuevo_estudiante = Estudiante(
        nombre=body['nombre'],
        apellido=body['apellido'],
        edad=body['edad']
    )
    db.session.add(nuevo_estudiante)
    db.session.commit()
    return jsonify(nuevo_estudiante.to_dict()), 201

# Obtener todos los estudiantes
@app.route('/estudiantes', methods=['GET'])
def obtener_todos_estudiantes():
    estudiantes = Estudiante.query.all()
    return jsonify([estudiante.to_dict() for estudiante in estudiantes]), 200

# Obtener un estudiante por ID
@app.route('/estudiante/<int:id_estudiante>', methods=['GET'])
def obtener_estudiante(id_estudiante):
    estudiante = Estudiante.query.get(id_estudiante)
    if estudiante:
        return jsonify(estudiante.to_dict()), 200
    else:
        return jsonify({'error': 'Estudiante no encontrado'}), 404

# Modificar un estudiante por ID
@app.route('/estudiante/<int:id_estudiante>', methods=['PUT'])
def actualizar_estudiante(id_estudiante):
    body = request.get_json()
    estudiante = Estudiante.query.get(id_estudiante)
    if estudiante:
        estudiante.nombre = body.get('nombre', estudiante.nombre)
        estudiante.apellido = body.get('apellido', estudiante.apellido)
        estudiante.edad = body.get('edad', estudiante.edad)
        db.session.commit()
        return jsonify(estudiante.to_dict()), 200
    else:
        return jsonify({'error': 'Estudiante no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
