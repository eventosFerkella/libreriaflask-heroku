

from flask_restful import Resource, reqparse
from models.sedeLibro import SedeLibroModel
from models.libro import LibroModel

serializer=reqparse.RequestParser()
serializer.add_argument(
    'libro_nombre',
    type=str,
    required=True,
    help='Falta el libro nombre',
    location='json'
)
serializer.add_argument(
    'libro_cant',
    type=int,
    required=True,
    help='Falta el libro cantidad',
    location='json'
)
serializer.add_argument(
    'libro_edicion',
    type=str,
    required=True,
    help='Falta el libro edicion',
    location='json'
)
serializer.add_argument(
    'autor_id',
    type=int,
    required=True,
    help='Falta el autor_id',
    location='json'
)
serializer.add_argument(
    'categoria_id',
    type=str,
    required=True,
    help='Falta el categoria_id',
    location='json'
)
class LibrosController(Resource):
    def post(self):
        data=serializer.parse_args()
        nuevoLibro=LibroModel(data['libro_nombre'],data['libro_cant'],data['libro_edicion'],data['autor_id'],data['categoria_id'])
        nuevoLibro.save()
        return {
            'success':True,
            'content':nuevoLibro.json(),
            'message':'se creo el libro exitosamente'
        }, 201

    def get(self):
        libros=LibroModel.query.all()
        print(libros[0].autorLibro.json())
        resultado=[]
        for libro in libros:
            resultadoTemporal=libro.json()
            resultadoTemporal['autor']=libro.autorLibro.json()
            resultadoTemporal['categoria']=libro.categoriaLibro.json()
            del resultadoTemporal['autor_id'] #forma para eliminar una llave de un diccionario
            del resultadoTemporal['categoria_id']
            resultado.append(resultadoTemporal)
        return {
            'success':True,
            'content':resultado,
            'message': None
        }

#Registrar libros en sedes:
class RegistroLibroSedeController(Resource):
    def post(self):
        serializerPost = reqparse.RequestParser(bundle_errors=True)
        serializerPost.add_argument(
            'libro_id',
            type=int,
            required=True,
            help='Falta el libro_id',
            location='json'
        )
        serializerPost.add_argument(
            'sedes',
            type=list,
            required=True,
            help='Falta las sedes',
            location='json'
        )
        data=serializerPost.parse_args()
        #print(data)
        try:
            for sede in data['sedes']:
            #print(sede['sede_id'])
                SedeLibroModel(sede['sede_id'], data['libro_id']).save()
            return {
                'success':True,
                'content': None,
                'message': 'se vinculo correctamente el libro con las sedes'
            }, 201
        except:
            return {
                'success':False,
                'content': None,
                'message': 'Error al registrar los libros con las sedes, vuelva a intentarlo nuevamente'
            }, 500
