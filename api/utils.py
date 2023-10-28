from functools import wraps 
from flask import request, jsonify
import jwt 
from api import app
from api.db.db import mysql

def client_resource(func):  #RECURSOS DE CADA CLIENTE // PARA VER SI EL CLIENTE ES DEL USUARIO QUE SOLICITA
    @wraps(func)
    def decorated(*args, **kwargs):
        print("Argumentos en client_resource: ", kwargs)
        id_cliente = kwargs['id_client'] #ID DE LA RUTA
        cur = mysql.connection.cursor()
        cur.execute('SELECT id_user FROM client WHERE id = {0}'.format(id_cliente)) #BUSCAMOS EL ID DE USUARIO DEL ID CLIENTE PASADO EN LA RUTA
        data = cur.fetchone()
        if data:
            id_prop = data[0]  #ID DE USUARIO QUE VINO EN LA CONSULTA
            user_id = request.headers['user_id'] #ID DE USUARIO DE LA CABECERA 
            if int(id_prop) != int(user_id): #ver si el id del usuario es propietario de esos recursos
                return jsonify ({"message":"No tiene persmisos para acceder a este recurso"}),401
        return func(*args, **kwargs)
    return decorated

def receipt_resource(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        id_receipt = kwargs['id_receipt'] #ID DE LA RUTA
        cur = mysql.connection.cursor()   
        cur.execute('SELECT id_user FROM receipt WHERE id = {0}'.format(id_receipt))
        data = cur.fetchone()
        if data:
            id_prop = data[0]  #ID DE USUARIO QUE VINO EN LA CONSULTA
            user_id = request.headers['user_id'] #ID DE USUARIO DE LA CABECERA 
            if int(id_prop) != int(user_id): #ver si el id del usuario es propietario de esos recursos
                return jsonify ({"message":"No tiene persmisos para acceder a este recurso"}),401
        return func(*args, **kwargs)
    return decorated


def product_service_resource(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        id_prod_serv = kwargs['id_product_service'] #ID DE LA RUTA
        cur = mysql.connection.cursor()   
        cur.execute('SELECT id_user FROM product_service WHERE id = {0}'.format(id_prod_serv))
        data = cur.fetchone()
        if data:
            id_prop = data[0]  #ID DE USUARIO QUE VINO EN LA CONSULTA
            user_id = request.headers['user_id'] #ID DE USUARIO DE LA CABECERA 
            if int(id_prop) != int(user_id): #ver si el id del usuario es propietario de esos recursos
                return jsonify ({"message":"No tiene persmisos para acceder a este recurso"}),401
        return func(*args, **kwargs)
    return decorated


def user_resources(func): #recursos de cada usuario // PARA CONSULTAR TODOS LOS CLIENTES DE UN USUARIO
    @wraps(func)
    def decorated(*args, **kwargs):
        print("Argumentos en user_resources: ", kwargs)
        id_user_route = kwargs['id_user'] #id de la ruta
        user_id = request.headers['user-id'] #ID DE LA CABECERA
        if int(id_user_route) != int(user_id):
            return jsonify({"message": "No tiene permisos para acceder a este recurso"}), 401
        return func(*args, **kwargs)
    return decorated


def token_required(func): #TOKEN DE INICIO 
    @wraps(func)
    def decorated(*args, **kwargs):
        
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify ({"message":"Falta el token"}),401
        
        user_id = None 

        if 'user_id' in request.headers:
            user_id = request.headers['user-id']

        if not user_id:
            return jsonify ({"message":"Falta el usuario"}),401   #ID de la cabezera

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms = ['HS256'])
            token_id= data ['id'] #id recuperado del token

            if int(user_id) != int(token_id): #comprueba si el id del token y el id del usuario son iguales
                return jsonify({"message":"Error de id"}),401
        except Exception as e:
            print(e)
            return jsonify({'message': str(e)}),401

        return func(*args, **kwargs)
    return decorated