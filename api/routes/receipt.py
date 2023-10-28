from api import app
from api.models.receipt import Receipt
from api.utils import token_required, user_resources, receipt_resource
from flask import jsonify
from api.db.db import mysql




@app.route('/user/<int:id_user>/receipt/<int:id_receipt>', methods = ['GET'])
@token_required
@user_resources
@receipt_resource
def get_receipt_by_id(id_user,id_receipt):
    #acceso a BD SELECT --- WHERE
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM receipt WHERE id = %s', (id_receipt,)) 
    data = cur.fetchall()
    if cur.rowcount>0:
        objClient = Receipt(data[0])
        return jsonify (objClient.to_json())
    return jsonify({"message": "id not found"}),404


@app.route('/user/<int:id_user>/receipt', methods = ['GET'])
@token_required
@user_resources
def get_all_receipt_by_user_id(id_user):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM receipt WHERE id_user = {0}'.format(id_user))
    data = cur.fetchall()
    receiptList = []
    for row in data:
        objClient = Receipt(row)
        receiptList.append(objClient.to_json())

    return jsonify(receiptList)
