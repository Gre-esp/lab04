from models.usuario import Usuario
from datetime import datetime
import sqlite3


class Cliente(Usuario):

    LISTA_ESTADO = {"NUEVO":"N", "PENDIENTE": "P", "VALIDADO": "V"}

    def __init__(self, dni: str = None, nombres: str = None, ape_pat: str = None, ape_mat: str = None,
                 genero: str = None, fecha_nac: datetime = None, fecha_creacion: datetime = None,
                 estado: str = None, email: str = None, password: str = None, preferencias: list = None):
        Usuario.__init__(self, dni, nombres, ape_pat, ape_mat, genero, fecha_nac,
                       fecha_creacion, estado, email, password)
        self.__preferencias = preferencias

    def crear_cuenta(self )-> bool:
        estado_op = False
        database = sqlite3.connect("data/linioexp.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:

            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            INSERT INTO clientes(email, password, fecha_creacion, estado, nombres)
            VALUES ('{}', '{}', '{}', '{}', '{}')
            '''.format(self.email, self.password, datetime.now(),
                       Cliente.LISTA_ESTADO.get("PENDIENTE"), self.nombres)
            cursor.execute(query)
            database.commit()  # CONFIRMAR CAMBIOS QUERY
            estado_op = True
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return estado_op

    def actualizar_datos(self)-> bool:
        estado_op = False
        database = sqlite3.connect("data/linioexp.db")
        try:

            cursor = database.cursor()
            query = '''
            UPDATE clientes
            SET documento_identidad = '{}', nombres = '{}', apellido_paterno = '{}', apellido_materno = '{}',
            genero = '{}', fecha_nacimiento = {}, estado = '{}'
            WHERE email = '{}'
            '''.format(self.documento_identidad, self.nombres, self.apellido_paterno,
                       self.apellido_materno, self.genero, self.fecha_nac,
                       Cliente.LISTA_ESTADO.get("VALIDADO"), self.email)
            cursor.execute(query)
            database.commit()
            estado_op = True
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return estado_op

    def obtener_usuarios():
        try:
            database = sqlite3.connect("data/linioexp.db")  # ABRIR CONEXION CON BASE DE DATOS
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            SELECT * FROM clientes
            '''
            cursor.execute(query)
            usuario = cursor.fetchall()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS
        return usuario

    @classmethod
    def obtener_usuario(cls, email: str):
        usuario = None
        try:
            database = sqlite3.connect("data/linioexp.db")  # ABRIR CONEXION CON BASE DE DATOS
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            SELECT email, password, documento_identidad, nombres, apellido_paterno, apellido_materno, genero,
            fecha_nacimiento, fecha_creacion, estado, preferencias
            FROM clientes WHERE email = '{}'
            '''.format(email)
            cursor.execute(query)
            usuario = cursor.fetchone()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return Cliente(email=usuario[0], password=usuario[1], dni=usuario[2], nombres=usuario[3],
                       ape_pat=usuario[4], ape_mat=usuario[5], genero=usuario[6], fecha_nac=usuario[7],
                       fecha_creacion=usuario[8], estado=usuario[9], preferencias=usuario[10])

    def __str__(self):
        return "{}-> email= '{}', estado= '{}', nombre= '{} {} {}'.".format(self.__class__.__name__, self.email,
                                                                            self.estado, self.nombres,
                                                                            self.apellido_paterno,
                                                                            self.apellido_materno)
