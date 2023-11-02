from api import app
from api.models.receipt import Receipt
from api.utils import token_required, user_resources, receipt_resource
from flask import jsonify, request
from api.db.db import mysql



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
    date = request.get_json()["date"]
    code = request.get_json()["code"] #recuperamos los datos del json con la libreria request y la funcion
    id_client = request.get_json()["id_client"] #get_json
    id_user = id_user
    receipt_detail = request.get_json()["receipt_detail"] #debe contener campo"
                                                          #name, y quantity

    #CHEQUEAMOS SI HAY STOCK Y SI EXISTEN LOS PRODUCTOS
    for product in receipt_detail:
        print(product)
        cur = mysql.connection.cursor()
        cur.execute('SELECT stock FROM product_service WHERE name = %s AND deleted = 1', (product['name'],))
        if cur.rowcount>0:
            stock_product = cur.fetchone()[0]
            if (product['quantity'] > stock_product):
                return jsonify({"message": f"Product {product['name']} insufficient stock"}), 404
        else:
            return jsonify({"message": f"Product {product['name']} not found"}), 404

    #INSERTAMOS LOS CAMPOS EN LAS COLUMNAS DE FACTURA
    cur = mysql.connection.cursor()
    #acceso a BD INSERT INTO
    cur.execute ('INSERT INTO receipt (date, code, id_client, id_user) VALUES (%s, %s, %s, %s)', (date, code, id_client, id_user))
    mysql.connection.commit()
    cur.execute('SELECT LAST_INSERT_ID()') #obtener el ultimo ID del registro creado
    id_receipt = cur.fetchone()[0] 

    details=[]
    for product in receipt_detail:
        #seleccionamos el ID del nombre de la factura que viene del front
        cur.execute('SELECT id FROM product_service WHERE name = %s ', (product['name'],))
        id_product_service = cur.fetchone()[0] 
        id_receipt = id_receipt
        quantity = product['quantity']
        #seleccionamos el precio del producto segun su nombre
        cur.execute('SELECT price FROM product_service WHERE name = %s ', (product['name'],))
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
        #restamos la quantity al stock
        cur.execute('UPDATE product_service SET stock = stock - %s WHERE id = %s', (quantity, id_product_service))
        mysql.connection.commit() #guardado
        details.append(detail)
    return jsonify({"code":code, "date": date, "details": details, "id": id_receipt, "id_client": id_client, "id_user": id_user})


#REMOVE 
@app.route('/user/<int:id_user>/receipt/<int:id_receipt>', methods = ['DELETE'])
@token_required
@user_resources
@receipt_resource
def remove_receipt(id_receipt,id_user):
    #acceso a BD SELECT --- DELETE FROM WHERE
    cur = mysql.connection.cursor()
    cur.execute('UPDATE receipt SET deleted = 0 WHERE id = %s', (id_receipt,)) 
    mysql.connection.commit()
    return jsonify({"message": "deleted", "id": id_receipt})