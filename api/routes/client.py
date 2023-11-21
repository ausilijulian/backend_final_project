from api import app
from api.models.client import Client
from api.utils import token_required, user_resources, client_resource
from flask import jsonify, request
from api.db.db import mysql

#GET CLIENT BY ID
@app.route('/user/<int:id_user>/client/<int:id_client>', methods = ['GET'])
@token_required
@user_resources
@client_resource
def get_client_by_id(id_user,id_client):
    #acceso a BD SELECT --- WHERE
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM client WHERE id = %s AND deleted = 1', (id_client,)) 
    data = cur.fetchall()
    if cur.rowcount>0:
        objClient = Client(data[0])
        return jsonify (objClient.to_json())
    return jsonify({"message": "id not found"}),404

#GET ALL CLIENTS BY USER ID
@app.route('/user/<int:id_user>/client', methods = ['GET'])
@token_required
@user_resources
def get_all_clients_by_user_id(id_user):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM client WHERE id_user = {0} AND deleted = 1'.format(id_user))
    data = cur.fetchall()
    clientList = []
    for row in data:
        objClient = Client(row)
        clientList.append(objClient.to_json())

    return jsonify(clientList)

#POST CLIENT
@app.route('/user/<int:id_user>/client', methods=['POST']) 
@token_required
@user_resources
def create_client(id_user):

    request_data = request.get_json()

    # Verificar la existencia de todas las claves requeridas
    required_keys = ['name', 'surname', 'email', 'dni']
    if not all(key in request_data for key in required_keys):
        return jsonify({"error": "Missing required keys"}), 400
    
    if not all(isinstance(request_data[key], str) for key in ['name', 'surname', 'email', 'dni']):
        return jsonify({"error": "Invalid data types for name, description, img, or type"}), 400


    name = request.get_json()["name"] #recuperamos los datos del json con la libreria request y la funcion
    surname = request.get_json()["surname"] #get_json
    email = request.get_json()["email"]
    dni = request.get_json()["dni"]
    id_user = id_user

    cur = mysql.connection.cursor()

    #control si existe el email 
    cur.execute('SELECT * FROM client WHERE email = %s AND id_user = %s AND deleted = 1', (email, id_user)) #la coma dsps de email es para que
    row = cur.fetchone()                                           # tome como tupla

    if row: #si no hay nada da null
        return jsonify({"error": "email ya registrado"}),400
    
    #control si existe el dni
    cur.execute('SELECT * FROM client WHERE dni = %s AND id_user = %s AND deleted = 1', (dni, id_user)) 
    row = cur.fetchone()                                           

    if row: #si no hay nada da null
        return jsonify({"error": "dni ya registrado"}),400

    #acceso a BD INSERT INTO
    cur.execute ('INSERT INTO client (name, surname, email, dni, id_user) VALUES (%s, %s, %s, %s, %s)', (name, surname, email, dni, id_user))
    mysql.connection.commit() #guardado
    cur.execute('SELECT LAST_INSERT_ID()') #obtener el ultimo ID del registro creado
    row = cur.fetchone() 
    return jsonify({"id": row[0], "name": name, "surname": surname, "email": email, "dni": dni, "id_user": id_user })


#UPDATE CLIENT
@app.route('/user/<int:id_user>/client/<int:id_client>', methods = ['PUT'])
@token_required
@user_resources
@client_resource
def update_client(id_client,id_user):

    request_data = request.get_json()

    # Verificar la existencia de todas las claves requeridas
    required_keys = ['name', 'surname', 'email', 'dni']
    if not all(key in request_data for key in required_keys):
        return jsonify({"error": "Missing required keys"}), 400
    
    if not all(isinstance(request_data[key], str) for key in ['name', 'surname', 'email', 'dni']):
        return jsonify({"error": "Invalid data types for name, description, img, or type"}), 400

    name=request.get_json()["name"] #recuperamos los datos del json con la libreria request y la funcion
    surname=request.get_json()["surname"] #get_json
    email = request.get_json()["email"]
    dni = request.get_json()["dni"]
   
    cur = mysql.connection.cursor()

    #control si existe el email PERO no del recurso que se edita
    #(esto permite editar otros campos de client sin se que se bloquee el UPDATE porque el cliente ya tiene su email registrado)

    cur.execute('SELECT * FROM client WHERE email = %s AND id != %s AND id_user = %s AND deleted = 1', (email, id_client, id_user))
    row = cur.fetchone()                                          

    if row: #si no hay nada da null
        return jsonify({"error": "email ya registrado"}),400

    cur.execute('SELECT * FROM client WHERE dni = %s AND id != %s AND id_user = %s AND deleted = 1', (dni, id_client, id_user))
    row = cur.fetchone()                                          

    if row: #si no hay nada da null
        return jsonify({"error": "dni ya registrado"}),400

    #acceso a BD SELECT --- UPDATE SET -- WHERE
    cur.execute('UPDATE client SET name = %s, surname = %s, email = %s, dni = %s WHERE id = %s', (name, surname, email, dni, id_client))
    mysql.connection.commit() #guardado
    return jsonify({"id":id_client, "name": name, "surname": surname, "dni": dni, "email": email})


#REMOVE CLIENT
@app.route('/user/<int:id_user>/client/<int:id_client>', methods = ['DELETE'])
@token_required
@user_resources
@client_resource
def remove_client(id_client,id_user):
    #acceso a BD SELECT --- DELETE FROM WHERE
    cur = mysql.connection.cursor()
    cur.execute('UPDATE client SET deleted = 0 WHERE id = %s', (id_client,)) 
    mysql.connection.commit()
    return jsonify({"message": "deleted", "id": id_client})