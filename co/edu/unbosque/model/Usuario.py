from co.edu.unbosque.model.Archivo import Archivo
import hashlib


class Usuario:
    def __init__(self):
        self.archivo = Archivo()

    def validarUsuario(self, usuario, password):
        m = hashlib.sha1()
        m.update(password.encode('utf-8'))
        password = m.hexdigest()
        sql = f"SELECT r.descripcion  FROM usuario u, rol r WHERE u.username='{usuario}' AND u.password='{password}' AND u.rol=r.id_rol "
        r = self.archivo.realizarSQL(sql)
        if r == []:
            return "No existe este usuario"
        else:
            return r

    def crearUsuario(self, username, password, cedula, telefono, nombre, apellidos, direccion, correo, rol):
        cantidadTelefonos = self.archivo.realizarSQL("SELECT count(*) FROM telefono")
        m = hashlib.sha1()
        m.update(password.encode('utf-8'))
        password = m.hexdigest()
        cantidadTelefonos = cantidadTelefonos[0][0]
        if self.archivo.realizarSQL(f"SELECT u.rol FROM usuario u WHERE u.username='{username}'") != []:
            return "Ya existe ese nombre de usuario"
        if self.archivo.realizarSQL(f"SELECT * FROM usuario u WHERE u.cedula='{cedula}'") != []:
            return "Ya existe esa cedula en otro usuario"
        if self.archivo.realizarSQL(f"SELECT * FROM telefono t WHERE t.num_tel='{telefono}'") != []:
            return "Ya existe ese telefono en otro usuario"
        if rol.upper() == "VETERINARIO":
            if self.archivo.realizarSQL("select * from rol r where r.id_rol=1") == []:
                self.archivo.realizarInsertSQL(f"insert into rol values('1','{rol.upper()}','A')")
            self.archivo.realizarInsertSQL(f"insert into telefono values('{cantidadTelefonos + 1}','{telefono}','A')")
            sql = f"insert into usuario values('{username}','{password}','{cedula}','{cantidadTelefonos + 1}','{nombre}','{apellidos}','{direccion}','{correo}','A',1)"
            self.archivo.realizarInsertSQL(sql)
            return "OK"
        elif rol.upper() == "PROPIETARIO":
            if self.archivo.realizarSQL("select * from rol r where r.id_rol=1") == []:
                self.archivo.realizarInsertSQL(f"insert into rol values('2','{rol.upper()}','A')")
            self.archivo.realizarInsertSQL(f"insert into telefono values('{cantidadTelefonos + 1}','{telefono}','A')")
            sql = f"insert into usuario values('{username}','{password}','{cedula}','{cantidadTelefonos + 1}','{nombre}','{apellidos}','{direccion}','{correo}','A',2)"
            self.archivo.realizarInsertSQL(sql)
            return "OK"
        else:
            return "No es posible crear el usuario"
    def obtenerUsuarioporTipo(self):
        consulta = "select r.descripcion , count(u.rol) from rol r, usuario u where u.rol = r.id_rol group by 1"
        resultado = self.archivo.realizarSQL(consulta)
        if (resultado == []):
            return "No existe esa mascota"
        else:
            return resultado