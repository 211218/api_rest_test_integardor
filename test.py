from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Conexión a la base de datos MySQL
conexion = mysql.connector.connect(
    host='localhost',
    user='root',
    password='211218',
    database='integardor_test'
)

# Crear un cursor para ejecutar consultas SQL
cursor = conexion.cursor(dictionary=True)

# Verificar y crear la tabla de usuarios si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    )
''')
conexion.commit()

# Ruta para obtener todos los usuarios
@app.route('/list_users', methods=['GET'])
def obtener_usuarios():
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    return jsonify(usuarios)

# Ruta para obtener un usuario por su ID
@app.route('/get_user/<int:id>', methods=['GET'])
def obtener_usuario(id):
    cursor.execute('SELECT * FROM usuarios WHERE id = %s', (id,))
    usuario = cursor.fetchone()
    if usuario:
        return jsonify(usuario)
    else:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404

# Ruta para crear un nuevo usuario
@app.route('/create_user', methods=['POST'])
def crear_usuario():
    nuevo_usuario = request.get_json()
    consulta = 'INSERT INTO usuarios (name, email, password) VALUES (%s, %s, %s)'
    datos = (nuevo_usuario['name'], nuevo_usuario['email'], nuevo_usuario['password'])
    cursor.execute(consulta, datos)
    conexion.commit()
    return jsonify({'mensaje': 'Usuario creado correctamente'}), 201

# Ruta para actualizar un usuario por su ID
@app.route('/update_user/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    usuario_actualizado = request.get_json()
    consulta = 'UPDATE usuarios SET name=%s, email=%s, password=%s WHERE id=%s'
    datos = (usuario_actualizado['name'], usuario_actualizado['email'], usuario_actualizado['password'], id)
    cursor.execute(consulta, datos)
    conexion.commit()
    return jsonify({'mensaje': 'Usuario actualizado correctamente'})

# Ruta para eliminar un usuario por su ID
@app.route('/delete_user/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    consulta = 'DELETE FROM usuarios WHERE id = %s'
    cursor.execute(consulta, (id,))
    conexion.commit()
    return jsonify({'mensaje': 'Usuario eliminado correctamente'})

# Ruta para iniciar sesión y devolver a la peticion el id, nombre y email del usuario
@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    consulta = 'SELECT id, name, email FROM usuarios WHERE email = %s AND password = %s'
    cursor.execute(consulta, (datos['email'], datos['password']))
    usuario = cursor.fetchone()
    if usuario:
        return jsonify(usuario)
    else:
        return jsonify({'mensaje': 'Credenciales incorrectas'}), 401
    

if __name__ == '__main__':
    app.run(debug=True, port=3002)