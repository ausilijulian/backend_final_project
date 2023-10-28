from api import app
from api.models.product_service import Product_Service
from api.utils import token_required, user_resources, product_service_resource
from flask import jsonify
from api.db.db import mysql


@app.route('/user/<int:id_user>/product_service/<int:id_product_service>', methods = ['GET'])
@token_required
@user_resources
@product_service_resource
def get_product_service_by_id(id_user,id_product_service):
    #acceso a BD SELECT --- WHERE
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM product_service WHERE id = %s', (id_product_service,)) 
    data = cur.fetchall()
    if cur.rowcount>0:
        objClient = Product_Service(data[0])
        return jsonify (objClient.to_json())
    return jsonify({"message": "id not found"}),404


@app.route('/user/<int:id_user>/product_service', methods = ['GET'])
@token_required
@user_resources
def get_all_product_service_by_user_id(id_user):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM product_service WHERE id_user = {0}'.format(id_user))
    data = cur.fetchall()
    clientList = []
    print(data)
    for row in data:
        objClient = Product_Service(row)
        clientList.append(objClient.to_json())

    return jsonify(clientList)
