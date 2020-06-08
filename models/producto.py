import sqlite3

class Producto(object):

    def __init__(self, codigo:str, nombre: str, descripcion: str, estado: str, precio: float,
                 descuento: float):
        self.__codigo = None
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__precio = precio
        self.__descuento = descuento
        self.__precio_desc = self.precio_venta
        self.__estado = estado


    def agregar_producto(self) -> bool:
        estado_op = False
        database = sqlite3.connect("data/linioexp.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                    INSERT INTO productos(codigo, nombre, descripcion, precio_venta, precio_normal,
                    estado, descuento)
                    VALUES ('{}', '{}', '{}', {}, {},'{}',{})
                    '''.format(self.__generar_codigo(), self.__nombre, self.__descripcion,
                               self.precio_venta, self.__precio, self.__estado, self.__descuento)
            cursor.execute(query)
            database.commit()  # CONFIRMAR CAMBIOS QUERY
            estado_op = True
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return estado_op

    @classmethod
    def obtener_producto_nombre(cls, nombre:str) -> list:
        lista_productos = None
        database = sqlite3.connect("data/linioexp.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                    SELECT codigo, nombre, descripcion, estado, precio_normal, precio_venta, descuento
                    FROM producto
                    WHERE nombre LIKE '%{}%'
                    '''.format(nombre)
            cursor.execute(query)
            lista_productos = cursor.fetchall()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        lista = []
        if lista_productos is not None:
            for item in lista_productos:
                lista.append(cls(item[0], item[1], item[2], item[3], item[4], item[5]))
        return lista

    @classmethod
    def obtener_productos(self) -> list:
        list_product = None
        database = sqlite3.connect("data/linioexp.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            SELECT * FROM productos
            '''
            cursor.execute(query)  # EJECUTA LA OPERACION
            list_product = cursor.fetchall()
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            raise e
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return list_product

    def actualizar_datos(self) -> bool:
        estado_ope: bool = False
        database = sqlite3.connect("data/linioexp.db")  # ABRIR CONEXION CON BASE DE DATOS

        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            UPDATE productos
            SET descripcion = '{}', precio_normal = {}, estado = '{}',  descuento = {}, precio_venta = {}
            WHERE codigo = '{}'
            '''.format(self.__descripcion, self.__precio, self.__estado, self.__descuento,
                       self.precio_venta, self.__codigo)
            cursor.execute(query)  # EJECUTA LA OPERACION
            database.commit()  # CONFIRMAR CAMBIOS QUERY
            estado_ope = True
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            raise e
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return estado_ope

    def __generar_codigo(self) -> str:
        count = 0
        database = sqlite3.connect("data/linioexp.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            SELECT COUNT(*) FROM productos'''
            cursor.execute(query)
            count = cursor.fetchone()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return "PROD" + "0" * (4 - len(str(count[0] + 1))) + str(count[0] + 1)

    @property
    def precio_venta(self) -> float:
        return self.__precio - (self.__precio * self.__descuento)

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @property
    def precio(self) -> float:
        return self.__precio

    @property
    def descuento(self) -> float:
        return self.__descuento

    @property
    def estado(self) -> str:
        return self.__estado


    @descripcion.setter
    def descripcion(self, new_value):
        self.__descripcion = new_value

    @precio.setter
    def precio(self, new_value):
        self.__precio = new_value

    @descuento.setter
    def descuento(self, new_value):
        self.__descuento = new_value

    @estado.setter
    def estado(self, new_value):
        self.__estado = new_value


    def __str__(self) -> str:
        return "{}-> nombre= {}, precio= {}, estado= {} ".format(self.__class__.__name__,
                                                                 self.__nombre, self.__precio,
                                                                 self.__estado)
