from api import app
from api.models.receipt import Receipt
from api.utils import token_required, user_resources, receipt_resource
from flask import jsonify, request
from api.db.db import mysql
from datetime import datetime

def is_valid_date(date_str, date_format="%Y-%m-%d"):
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False


#GET FACTURA BY ID
@app.route('/user/<int:id_user>/receipt/<int:id_receipt>', methods = ['GET'])
@token_required
@user_resources
@receipt_resource
def get_receipt_by_id(id_user,id_receipt):
    #acceso a BD SELECT --- WHERE
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM receipt WHERE id = %s AND deleted = 1', (id_receipt,)) 
    dataReceipt = cur.fetchall()
    if cur.rowcount>0:
        cur.execute('SELECT * FROM receipt_detail WHERE id_receipt = %s', (id_receipt,)) 
        dataReceipt_detail = cur.fetchall()
        objReceipt = Receipt(dataReceipt[0],dataReceipt_detail)
        return jsonify (objReceipt.to_json())
    return jsonify({"message": "id not found"}),404

#GET TODAS LAS FACTURAS
@app.route('/user/<int:id_user>/receipt', methods = ['GET'])
@token_required
@user_resources
def get_all_receipt_by_user_id(id_user):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM receipt WHERE id_user = {0} AND deleted = 1'.format(id_user))
    dataReceipt = cur.fetchall()
    receiptList = []
    for row in dataReceipt:

        id_receipt = row[0]
        cur.execute('SELECT * FROM receipt_detail WHERE id_receipt = %s', (id_receipt,)) 
        dataReceipt_detail = cur.fetchall()
        objClient = Receipt(row,dataReceipt_detail)
        receiptList.append(objClient.to_json())

    return jsonify(receiptList)


#POST FACTURA
@app.route('/user/<int:id_user>/receipt', methods=['POST']) 
@token_required
@user_resources
def create_receipt(id_user):


    request_data = request.get_json()

    # Verificar la existencia de todas las claves requeridas
    required_keys = ['date', 'code', 'dni_client', 'receipt_detail']
    if not all(key in request_data for key in required_keys):
        return jsonify({"error": "Missing required keys"}), 400
    
    # Verificar si 'date' es una cadena y sigue el formato de fecha esperado
    if 'date' in request_data and not (isinstance(request_data['date'], str) and is_valid_date(request_data['date'])):
        return jsonify({"error": "Invalid data type or format for date"}), 400

    # Verificar si 'code' y 'dni_client' son cadenas (str)
    if not all(isinstance(request_data[key], str) for key in ['code', 'dni_client']):
        return jsonify({"error": "Invalid data types for code or dni_client"}), 400

    # Verificar si 'receipt_detail' es una lista
    if 'receipt_detail' in request_data and not isinstance(request_data['receipt_detail'], list):
        return jsonify({"error": "Invalid data type for receipt_detail, expected list"}), 400
    
    for item in request_data['receipt_detail']:
        # Verificar si el objeto es un diccionario
        if not isinstance(item, dict):
            return jsonify({"error": "Each item in receipt_detail should be a dictionary"}), 400

        # Verificar la presencia de 'name' y 'quantity' en el objeto
        if 'name' not in item or 'quantity' not in item:
            return jsonify({"error": "Each item in receipt_detail should have 'name' and 'quantity'"}), 400

        # Verificar que 'name' sea una cadena y 'quantity' sea un entero
        if not (isinstance(item['name'], str) and isinstance(item['quantity'], int)):
            return jsonify({"error": "Invalid data types for 'name' or 'quantity' in receipt_detail"}), 400   

    date = request.get_json()["date"]
    code = request.get_json()["code"] #recuperamos los datos del json con la libreria request y la funcion
    dni_client = request.get_json()["dni_client"] #get_json
    id_user = id_user
    receipt_detail = request.get_json()["receipt_detail"] #debe contener campo"
                                                          #name, y quantity

    
    cur = mysql.connection.cursor()

    #Ver si existe el cliente
    cur.execute('SELECT * FROM client WHERE dni = %s AND deleted = 1 AND id_user = %s', (dni_client, id_user))
    if cur.rowcount == 0:
        return jsonify({"error": f"Cliente no encontrado"}), 404
    id_client = cur.fetchone()[0]


    sum_by_name = {}

# Crear una nueva lista para almacenar los datos unificados
    new_details = []

    # Procesar los detalles y actualizar la lista new_details
    for item in receipt_detail:
        name = item['name']
        quantity = item['quantity']

        # Comprobar si el nombre ya está en el diccionario
        if name in sum_by_name:
            # Si ya existe, sumar la cantidad
            sum_by_name[name] += quantity
        else:
            # Si no existe, crear una nueva entrada en el diccionario
            sum_by_name[name] = quantity
    print(sum_by_name)
    # Crear un nuevo elemento de detalle unificado para cada nombre
    for name, total_quantity in sum_by_name.items():
        new_item = {
            "name": name,
            "quantity": total_quantity
        }
        new_details.append(new_item)
    print(new_details)
    # Sobrescribir details con los datos unificados
    receipt_detail = new_details

    #CHEQUEAMOS SI HAY STOCK Y SI EXISTEN LOS PRODUCTOS
    for product in receipt_detail:
        
        # cur = mysql.connection.cursor()
        cur.execute('SELECT stock FROM product_service WHERE name = %s AND deleted = 1 AND id_user = %s ', (product['name'], id_user))
        if cur.rowcount>0: #Chequea si la consulta devolvio alguna fila
            stock_product = cur.fetchone()[0] 
            cur.execute('SELECT type FROM product_service WHERE name = %s AND deleted = 1 AND id_user = %s ', (product['name'], id_user))
            type_product = cur.fetchone()[0] 
            if type_product == "Producto": #si el type es producto nos fijamos que la quantity no supere el stock.
                if (product['quantity'] > stock_product):
                    return jsonify({"error": f"Product {product['name']} insufficient stock"}), 404
        else: 
            return jsonify({"error": f"Product {product['name']} not found"}), 404

    #INSERTAMOS LOS CAMPOS EN LAS COLUMNAS DE FACTURA
    # cur = mysql.connection.cursor()
    #acceso a BD INSERT INTO
    cur.execute ('INSERT INTO receipt (date, code, id_client, id_user) VALUES (%s, %s, %s, %s)', (date, code, id_client, id_user))
    mysql.connection.commit()
    cur.execute('SELECT LAST_INSERT_ID()') #obtener el ultimo ID del registro creado
    id_receipt = cur.fetchone()[0] 

    details=[]
    for product in receipt_detail:
        #seleccionamos el ID del nombre de la factura que viene del front
        cur.execute('SELECT id FROM product_service WHERE name = %s AND deleted = 1 AND id_user = %s ', (product['name'], id_user))
        id_product_service = cur.fetchone()[0] 
        quantity = product['quantity']
        #seleccionamos el precio del producto segun su id
        cur.execute('SELECT price FROM product_service WHERE id = %s ', (id_product_service,))
        unit_price = cur.fetchone()[0] 
        #Insertamos el producto en la factura_detalle
        cur.execute ('INSERT INTO receipt_detail (id_receipt, id_product_service, quantity, unit_price) VALUES (%s, %s, %s, %s)', (id_receipt, id_product_service, quantity, unit_price))
        mysql.connection.commit() #guardado
        detail = {
                    "id_product_service": id_product_service,
                    "name": product['name'],
                    "quantity": product['quantity'],
                    "unit_price": unit_price
                }
        #restamos la quantity al stock en en caso de ser producto
        cur.execute('UPDATE product_service SET stock = stock - %s WHERE id = %s AND type = "Producto"', (quantity, id_product_service))
        mysql.connection.commit() #guardado
        details.append(detail)
    return jsonify({"code":code, "date": date, "details": details, "id": id_receipt, "id_client": id_client, "id_user": id_user})


# #REMOVE 
# @app.route('/user/<int:id_user>/receipt/<int:id_receipt>', methods = ['DELETE'])
# @token_required
# @user_resources
# @receipt_resource
# def remove_receipt(id_receipt,id_user):
#     #acceso a BD SELECT --- DELETE FROM WHERE
#     cur = mysql.connection.cursor()
#     cur.execute('UPDATE receipt SET deleted = 0 WHERE id = %s', (id_receipt,)) 
#     mysql.connection.commit()
#     return jsonify({"message": "deleted", "id": id_receipt})


# Ruta para obtener un ranking de productos por cantidad
@app.route('/user/<int:id_user>/receiptRanking', methods=['GET'])
@token_required
@user_resources
def get_product_ranking(id_user):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM receipt WHERE id_user = {0} '.format(id_user))
    dataReceipt = cur.fetchall()
    receiptList = []
    for row in dataReceipt:

        id_receipt = row[0]
        cur.execute('SELECT * FROM receipt_detail WHERE id_receipt = %s', (id_receipt,)) 
        dataReceipt_detail = cur.fetchall()
        objClient = Receipt(row,dataReceipt_detail)
        receiptList.append(objClient.to_json())
    # Crear diccionarios para los rankings de Producto y Servicio
    product_ranking = {}
    service_ranking = {}

    # Recorrer la lista de objetos
    for item in receiptList:
        details = item.get("details", [])
        for detail in details:
            name = detail.get("name")
            quantity = detail.get("quantity")
            type = detail.get("type")

            if type == "Producto":
                if name in product_ranking:
                    product_ranking[name] += quantity
                else:
                    product_ranking[name] = quantity
            elif type == "Servicio":
                if name in service_ranking:
                    service_ranking[name] += quantity
                else:
                    service_ranking[name] = quantity

    # Ordenar los rankings por cantidad descendente
    product_ranking = {k: v for k, v in sorted(product_ranking.items(), key=lambda item: item[1], reverse=True)}
    service_ranking = {k: v for k, v in sorted(service_ranking.items(), key=lambda item: item[1], reverse=True)}

    # Crear un objeto JSON que contiene ambos rankings
    ranking = {"products": product_ranking, "services": service_ranking}
    return jsonify(ranking)
