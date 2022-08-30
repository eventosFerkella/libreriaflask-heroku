from flask import Flask, request
from flask_restful import Api
from config.base_datos import bd
#from models.autor import 
from controllers.autor import AutoresController, AutorController
from models.sede import SedeModel
from controllers.sede import LibroSedeController, SedesController, LibroCategoriaSedeController
#from models.categoria import CategoriaModel
from controllers.categoria import CategoriaController
#from models.libro import LibroModel
from controllers.libro import LibrosController, LibroModel, RegistroLibroSedeController
#from models.sedeLibro import SedeLibroModel
from flask_cors import CORS
#para documentacion
from flask_swagger_ui import get_swaggerui_blueprint


SWAGGER_URL= '' #esta variable se usa para indicar en que endpoint se encontrará la documentación
API_URL= '/static/swagger.json' #se usa para indicar en que parte del proyecto se encuentra el archivo de la documentación
swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Libreria Flask - Swagger Documentation"
    }
)

app=Flask(__name__)
app.register_blueprint(swagger_blueprint)

api=Api(app)
CORS(app) #permitiendo todos los metodos dominios y headers

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost:3306/flasklibreria'
#para evitar el warning de funcionalidad de sqlalchemy de track :
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bd.init_app(app)
#necesita un driver: pip install mysqlclient
#bd.drop_all(app=app)
bd.create_all(app=app)

@app.route('/buscar')
def buscarLibro():
    #print(request.args.get('palabra'))
    palabra=request.args.get('palabra')
    if palabra:
        resultadoBusqueda=LibroModel.query.filter(LibroModel.libroNombre.like('%'+palabra+'%')).all()
        if resultadoBusqueda:
            resultado=[]
            for libro in resultadoBusqueda:
                resultado.append(libro.json())
            return {
                'success': True,
                'content': resultado,
                'message': None
            }
    return {
        'success': False,
        'content': None,
        'message': 'la búsqueda no tuvo éxito'
    },400



#RUTAS
api.add_resource(AutoresController,'/autores')
api.add_resource(AutorController,'/autor/<int:id>')
api.add_resource(CategoriaController, '/categorias','/categoria')
api.add_resource(LibrosController,'/libro','/libros')
api.add_resource(SedesController,'/sedes','/sede')
api.add_resource(LibroSedeController,'/sedeLibros/<int:id_sede>')
api.add_resource(LibroCategoriaSedeController,'/busquedaLibroSedeCat')
api.add_resource(RegistroLibroSedeController,'/registrarSedesLibro')


if __name__ == "__main__":
    app.run(debug=True)