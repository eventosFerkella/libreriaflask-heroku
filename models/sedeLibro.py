from config.base_datos import bd
from sqlalchemy import Column, ForeignKey, types

class SedeLibroModel(bd.Model):
    __tablename__="t_sede_libro"
    sedeLibroId=Column(name="sede_libro_id",
                        type_=types.Integer,
                        primary_key=True,
                        autoincrement=True,
                        unique=True)

    sede=Column(ForeignKey('t_sede.sede_id'),
                name="sede_id",
                type_=types.Integer)
    libro=Column(ForeignKey('t_libro.libro_id'),
                name="libro_id",
                type_=types.Integer)

    def __init__(self, sede_id, libro_id):
        self.sede = sede_id
        self.libro = libro_id

    def save(self):
        bd.session.add(self)
        bd.session.commit()
