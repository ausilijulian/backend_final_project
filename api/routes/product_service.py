from api import app
from api.models.product_service import Product_Service
from api.utils import token_required, user_resources, product_service_resource
from flask import jsonify, request
from api.db.db import mysql

#GET PRODUCT SERCVICE BY ID
@app.route('/user/<int:id_user>/product_service/<int:id_product_service>', methods = ['GET'])
@token_required
@user_resources
@product_service_resource
def get_product_service_by_id(id_user,id_product_service):
    #acceso a BD SELECT --- WHERE
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM product_service WHERE id = %s AND deleted = 1', (id_product_service,)) 
    data = cur.fetchall()
    if cur.rowcount>0:
        objClient = Product_Service(data[0])
        return jsonify (objClient.to_json()),200
    return jsonify({"message": "id not found"}),404

#GET ALL PRODUCT SERVICE
@app.route('/user/<int:id_user>/product_service', methods = ['GET'])
@token_required
@user_resources
def get_all_product_service_by_user_id(id_user):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM product_service WHERE id_user = {0} AND deleted = 1'.format(id_user))
    data = cur.fetchall()
    clientList = []
    print(data)
    for row in data:
        objClient = Product_Service(row)
        clientList.append(objClient.to_json())

    return jsonify(clientList),200


#POST PRODUCT SERVICE
@app.route('/user/<int:id_user>/product_service', methods=['POST']) 
@token_required
@user_resources
def create_product_service(id_user):
    request_data = request.get_json()

    # Verificar la existencia de todas las claves requeridas
    required_keys = ['name', 'description', 'img', 'type', 'price','stock']
    if not all(key in request_data for key in required_keys):
        return jsonify({"error": "Missing required keys"}), 400
    
    if not all(isinstance(request_data[key], str) for key in ['name', 'description', 'img', 'type']):
        return jsonify({"error": "Invalid data types for name, description, img, or type"}), 400

    type = request.get_json()["type"]

    if type == "Producto": 
        for key in ['price', 'stock']:
            if key in request_data and not isinstance(request_data[key], (int, float)):
                return jsonify({"error": f"Invalid data type for {key}"}), 400
    else:
        for key in ['price']:
            if key in request_data and not isinstance(request_data[key], (float,int)):
                return jsonify({"error": f"Invalid data type for {key}"}), 400
            

    name = request.get_json()["name"]
    price = request.get_json()["price"] 
    description= request.get_json()["description"]
    img = request.get_json()["img"]
    
    id_user = id_user

    if type == "Producto": 
        stock = request.get_json()["stock"]
    else:   
        stock = 1
  
    cur = mysql.connection.cursor()

    #control si existe el name
    cur.execute('SELECT * FROM product_service WHERE name = %s AND id_user = %s AND deleted = 1 ', (name, id_user)) 
    row = cur.fetchone()                                           

    if row: #si no hay nada da null
        return jsonify({"error": "nombre ya registrado"}),400

    #acceso a BD INSERT INTO
    cur.execute ('INSERT INTO product_service (name, stock, price, description, img, type, id_user) VALUES (%s, %s, %s, %s, %s, %s, %s)', (name, stock, price, description, img, type, id_user))
    mysql.connection.commit() #guardado
    cur.execute('SELECT LAST_INSERT_ID()') #obtener el ultimo ID del registro creado
    row = cur.fetchone() 
    return jsonify({"id": row[0],"name": name, "stock": stock, "price": price, "description": description, "img": img, "type": type, "id_user": id_user }),201


#UPDATE PRODUCT SERVICE
@app.route('/user/<int:id_user>/product_service/<int:id_product_service>', methods = ['PUT'])
@token_required
@user_resources
@product_service_resource
def update_product_service(id_product_service, id_user):

    request_data = request.get_json()

    # Verificar la existencia de todas las claves requeridas
    required_keys = ['name', 'description', 'img', 'type', 'price','stock']
    if not all(key in request_data for key in required_keys):
        return jsonify({"error": "Missing required keys"}), 400
    
    if not all(isinstance(request_data[key], str) for key in ['name', 'description', 'img', 'type']):
        return jsonify({"error": "Invalid data types for name, description, img, or type"}), 400

    for key in ['price', 'stock']:
        if key in request_data and not isinstance(request_data[key], (int, float)):
            return jsonify({"error": f"Invalid data type for {key}"}), 400
        
        
    name = request.get_json()["name"]
    stock = request.get_json()["stock"] #recuperamos los datos del json con la libreria request y la funcion
    price = request.get_json()["price"] #get_json
    description= request.get_json()["description"]
    img = request.get_json()["img"]
    type = request.get_json()["type"]
    cur = mysql.connection.cursor()

     #control si existe el name PERO no del del producto que se edita
    #(esto permite editar campos de product_service sin que se bloque el UPDATE porque el producto ya tiene su name registrado)

    cur.execute('SELECT * FROM product_service WHERE name = %s AND id != %s AND id_user = %s AND deleted = 1 ', (name, id_product_service, id_user))
    row = cur.fetchone()                                           

    if row: #si no hay nada da null
        return jsonify({"error": "nombre ya registrado"}),400


    #acceso a BD SELECT --- UPDATE SET -- WHERE
    cur.execute('UPDATE product_service SET name = %s, stock = %s, price = %s, description = %s, img = %s, type = %s  WHERE id = %s ', (name, stock, price, description, img, type, id_product_service))
    mysql.connection.commit() #guardado
    return jsonify({"id": id_product_service , "name": name, "stock": stock, "description": description, "img": img, "type": type}),201


#REMOVE PRODUCT SERVICE
@app.route('/user/<int:id_user>/product_service/<int:id_product_service>', methods = ['DELETE'])
@token_required
@user_resources
@product_service_resource
def remove_product_service(id_product_service,id_user):
    #acceso a BD SELECT --- DELETE FROM WHERE
    cur = mysql.connection.cursor()
    result = cur.execute('UPDATE product_service SET deleted = 0 WHERE id = %s', (id_product_service,))
    
    if result == 0:
        # Si ninguna fila fue afectada, el producto o servicio no fue encontrado
        cur.close()
        return jsonify({"error": "Product or service not found"}), 404

    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Product or service deleted", "id": id_product_service}), 200