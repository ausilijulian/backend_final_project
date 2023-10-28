from api import app
from api.models.receipt_detail import Receipt_Detail
from api.utils import token_required, user_resources, receipt_resource
from flask import jsonify
from api.db.db import mysql


@app.route('/user/<int:id_user>/receipt/<int:id_receipt>/receipt_detail', methods = ['GET'])
@token_required
@user_resources
@receipt_resource
def get_receipt_detail_by_id_receipt(id_user,id_receipt):
    #acceso a BD SELECT --- WHERE
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM receipt_detail WHERE id_receipt = %s', (id_receipt,)) 
    data = cur.fetchall()
    receipt_detailList = []
    for row in data:
        objClient = Receipt_Detail(row)
        receipt_detailList.append(objClient.to_json())

    return jsonify(receipt_detailList)
