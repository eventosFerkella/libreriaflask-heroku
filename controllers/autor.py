from flask_restful import Resource, reqparse
from models.autor import AutorModel

serializer= reqparse.RequestParser()
serializer.add_argument(
    'autor_nombre',
    type=str,
    required=True,
    help='Falta el nombre autor'
)

class AutoresController(Resource):
    def post(self):
        informacion=serializer.parse_args()
        nuevoAutor=AutorModel(informacion['autor_nombre'])
        nuevoAutor.save()
        print(nuevoAutor)
        return {
            'success': True,
            'content': None,
            'message': 'Autor creado exitosamente'
        }, 201

    def get(self):
        lista_autores=AutorModel.query.all()
        resultado=[]
        for autor in lista_autores:
            resultado.append(autor.json())
            print(autor.json())
        return {
	            'success':True,
	            'content': resultado,
	            'message': None
	        }

class AutorController(Resource):
    def get(self,id):
        #.all() => retorna todas las coincidencias (retorna una lista de instancias)
        #.first() => retorna el primer registro de las coincidencias (retorna una instancia)
        autorEncontrado = AutorModel.query.filter_by(autorId=id).first()
        print(autorEncontrado)
        # si el autor se encontro retorna en el content su contenido pero sino se hallo dicho autor indicar que 
        #el id no existe con un statos 404
        if autorEncontrado:
            return {
                'success': True,
                'content': autorEncontrado.json(),
                'messaje': None                
            }
        else:
            return {
                'success': False,
                'content': None,
                'message': 'el autor no existe'
            }

    def put(self,id):
        autorEncontrado = AutorModel.query.filter_by(autorId=id).first()
        #no siempre es necesario hacer la validación que el objeto exista puesto que el front se debe encargar de hacer
        #esta validación
        if autorEncontrado:
            data = serializer.parse_args()
            autorEncontrado.autorNombre=data['autor_nombre']
            autorEncontrado.save()
            return {
                'success': True,
                'content': autorEncontrado.json(),
                'message': 'Se actualizo el autor con éxito'
            }, 201
        return {
            'success': False,
            'content': None,
            'message': 'No se encontró el autor a actualizar'
        }, 404

    def delete(self,id):
	        autorEncontrado=AutorModel.query.filter_by(autorId=id).first()
	        if autorEncontrado:
	            autorEncontrado.delete()
	            return {
	                'success': True,
	                'content': None,
	                'message': 'Se elimino exitosamente el autor de la bd'
	            }
	        else:
	            return {
	                'success': False,
	                'content': None,
	                'message': 'No se encontro el autor a eliminar'
	            }, 404




