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
        return jsonify (objClient.to_json())
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

    return jsonify(clientList)


#POST PRODUCT SERVICE
@app.route('/user/<int:id_user>/product_service', methods=['POST']) 
@token_required
@user_resources
def create_product_service(id_user):
    name = request.get_json()["name"]
    # stock = request.get_json()["stock"] 
    price = request.get_json()["price"] 
    description= request.get_json()["description"]
    img = request.get_json()["img"]
    type = request.get_json()["type"]
    id_user = id_user

    if type == "Producto": 
        stock = request.get_json()["stock"]
    else:   #la tabla stock en caso de ser un Servicio se le asignara 1 (revisar!)
        stock = 1
    cur = mysql.connection.cursor()


    #control si existe el name
    cur.execute('SELECT * FROM product_service WHERE name = %s AND id_user = %s AND deleted = 1 ', (name, id_user)) 
    row = cur.fetchone()                                           

    if row: #si no hay nada da null
        return jsonify({"message": "nombre ya registrado"})

    #acceso a BD INSERT INTO
    cur.execute ('INSERT INTO product_service (name, stock, price, description, img, type, id_user) VALUES (%s, %s, %s, %s, %s, %s, %s)', (name, stock, price, description, img, type, id_user))
    mysql.connection.commit() #guardado
    cur.execute('SELECT LAST_INSERT_ID()') #obtener el ultimo ID del registro creado
    row = cur.fetchone() 
    return jsonify({"id": row[0],"name": name, "stock": stock, "price": price, "description": description, "img": img, "type": type, "id_user": id_user })


#UPDATE CLIENT
@app.route('/user/<int:id_user>/product_service/<int:id_product_service>', methods = ['PUT'])
@token_required
@user_resources
@product_service_resource
def update_product_service(id_product_service, id_user):
    name = request.get_json()["name"]
    stock = request.get_json()["stock"] #recuperamos los datos del json con la libreria request y la funcion
    price = request.get_json()["price"] #get_json
    description= request.get_json()["description"]
    img = request.get_json()["img"]
    type = request.get_json()["type"]
    cur = mysql.connection.cursor()

     #control si existe el name PERO no del del recurso que edita
    #(esto permite editar campos de product_service sin que se bloque el UPDATE porque el producto ya tiene su name registrado)

    cur.execute('SELECT * FROM product_service WHERE name = %s AND id != %s AND id_user = %s AND deleted = 1 ', (name, id_product_service, id_user))
    row = cur.fetchone()                                           

    if row: #si no hay nada da null
        return jsonify({"message": "nombre ya registrado"})


    #acceso a BD SELECT --- UPDATE SET -- WHERE
    cur.execute('UPDATE product_service SET name = %s, stock = %s, price = %s, description = %s, img = %s, type = %s  WHERE id = %s ', (name, stock, price, description, img, type, id_product_service))
    mysql.connection.commit() #guardado
    return jsonify({"id": id_product_service , "name": name, "stock": stock, "description": description, "img": img, "type": type})


#REMOVE PRODUCT SERVICE
@app.route('/user/<int:id_user>/product_service/<int:id_product_service>', methods = ['DELETE'])
@token_required
@user_resources
@product_service_resource
def remove_product_service(id_product_service,id_user):
    #acceso a BD SELECT --- DELETE FROM WHERE
    cur = mysql.connection.cursor()
    cur.execute('UPDATE product_service SET deleted = 0 WHERE id = %s', (id_product_service,)) 
    mysql.connection.commit()
    return jsonify({"message": "deleted", "id": id_product_service})