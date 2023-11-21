from api import app
from api.models.users import Users
# from api.utils import token_required, user_resources, client_resource
from flask import jsonify, request
from api.db.db import mysql
import datetime
import jwt

@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    
    #CONTROL SI EXISTEN VALORES PARA LA AUTENTICACION
    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "Login Incorrecto"}),401
    #CONTROL SI EXISTE Y COINCIDE EN LA BD
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE username = %s AND password = %s',(auth.username, auth.password))
    row = cur.fetchone()
   
    if not row:
        return jsonify({"message": "Login Incorrecto"}),401
    
    token = jwt.encode({'id':row[0],
                        'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
    
    return jsonify({"token": token, "username": auth.username, "id":row[0]})
