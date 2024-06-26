from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

from config import config

app=Flask(__name__)

conexion  = MySQL(app=app)

@app.route('/categorias', methods=['GET'])
def listar_categorias():
    try:
        cursor = conexion.connection.cursor()
        sql = "select id_categoria, nombre_categoria from categoria"
        cursor.execute(sql)
        datos = cursor.fetchall()
        categorias = []
        for fila in datos:
            categoria = {'id_categoria':fila[0], 'nombre_categoria':fila[1]}
            categorias.append(categoria)
        return jsonify({'categorias':categorias, 'mensaje':"Categorias listadas: "})
    except Exception as ex:
        return jsonify({'mensaje':"Error!!!! "})
    

@app.route('/categorias/<id_cat>', methods=['GET'])
def leer_categoria(id_cat):
    try:
        cursor = conexion.connection.cursor()
        sql = "select id_categoria, nombre_categoria from categoria where id_categoria = '{0}'".format(id_cat)
        cursor.execute(sql)
        datos = cursor.fetchall()
        #print(type(datos))
        categorias = []
        if (datos):
            for fila in datos:
                categoria = {'id_categoria':fila[0], 'nombre_categoria':fila[1]}
                categorias.append(categoria)
        else:
            return jsonify({'mensaje':"No hay datos para el codigo de categoria: {0}!!!! ".format(id_cat)})
        return jsonify({'categorias':categorias, 'mensaje':"Categorias listadas: "})
    except Exception as ex:
        return jsonify({'mensaje':"Error!!!! "})
    
@app.route('/categorias', methods=['POST'])
def registrar_categoria():
    try:
        cursor = conexion.connection.cursor()
        sql = "select id_categoria, nombre_categoria from categoria where id_categoria = '{0}'".format(request.json['id_categoria'])
        cursor.execute(sql)
        datos = cursor.fetchall()
        if (datos):
            return jsonify({'mensaje':"La categoria: {0} ya existe en la bbdd!!!! ".format(request.json['id_categoria'])})
        else:
            sql= """insert into categoria (id_categoria, nombre_categoria) values ({0},'{1}')""".format(request.json['id_categoria'],request.json['nombre_categoria'])
            print(sql)
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje':"Categoria registrada!!!! "})
    except Exception as ex:
        return jsonify({'mensaje':ex.__doc__})
    

@app.route('/categorias/<id_cat>', methods=['DELETE'])
def eliminar_categoria(id_cat):
    try:
        cursor = conexion.connection.cursor()
        sql = "select id_categoria, nombre_categoria from categoria where id_categoria = '{0}'".format(id_cat)
        cursor.execute(sql)
        datos = cursor.fetchall()
        if (datos):
            sql= "delete from categoria where id_categoria = {0}".format(id_cat)
            print(sql)
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje':"Categoria eliminada correctamente!!!! "})
        else:
            return jsonify({'mensaje':"La categoria {0} no existe en la bbdd!!!! ".format(id_cat)})        
    except Exception as ex:
        return jsonify({'mensaje':ex.__doc__})
    
@app.route('/categorias/<id_cat>', methods=['PUT'])
def actualizar_categoria(id_cat):
    try:
        cursor = conexion.connection.cursor()
        sql = "select id_categoria, nombre_categoria from categoria where id_categoria = '{0}'".format(id_cat)
        cursor.execute(sql)
        datos = cursor.fetchall()
        if (datos):
            sql= "update categoria set nombre_categoria = '{1}' where id_categoria = {0}".format(id_cat, request.json['nombre_categoria'])
            print(sql)
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje':"Categoria actualizada correctamente!!!! "})
        else:
            return jsonify({'mensaje':"La categoria {0} no existe en la bbdd!!!! ".format(id_cat)})        
    except Exception as ex:
        return jsonify({'mensaje':ex.__doc__})


def pagina_no_encontrada(error):
    return "<h1> La pagina no existe mas querido</h1>", 404


if __name__=='__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()