from co.edu.unbosque.model.Archivo import Archivo


class Mascota:

    def __init__(self):
        self.archivo = Archivo()

    def crearMascota(self, nombre, especie, raza, color, peso, fecha, propietario):
        valorEspecie = self.manejoEspecie(especie.lower())
        valorRaza = self.manejoRaza(raza.lower())
        valorColor = self.manejoColor(color.lower())
        nombre = nombre.lower()
        sql = f"SELECT * FROM mascota m where m.nombre='{nombre}' AND m.especie='{valorEspecie}' AND m.raza='{valorRaza}' AND m.color='{valorColor}' AND m.peso='{peso}' AND m.fecha_nacimiento='{fecha}' AND usuario_propietario='{propietario}'"
        if (self.archivo.realizarSQL(sql) != []):
            return "Ya existe una mascota con esos datos"
        else:
            cantidad = self.archivo.realizarSQL(f"SELECT count(*) FROM mascota ")
            cantidad = cantidad[0][0]
            sql = f"INSERT INTO mascota values('{cantidad+1}','{nombre}', '{valorEspecie}', '{valorRaza}', '{valorColor}', '{peso}', '{fecha}', '{propietario}','A')"
            return self.archivo.realizarInsertSQL(sql)

    def manejoEspecie(self, especie):
        consulta = self.archivo.realizarSQL(
            f"SELECT e.id_especie FROM especie e where e.descripcion='{especie}'")
        if consulta != []:
            return consulta[0][0]
        else:
            cantidad = self.archivo.realizarSQL(f"SELECT count(*) FROM especie e")
            cantidad = cantidad[0][0]
            self.archivo.realizarInsertSQL(
                f"insert into especie values('{cantidad + 1}','{especie}','A')")
            return cantidad + 1

    def manejoColor(self, color):
        consulta = self.archivo.realizarSQL(
            f"SELECT c.id_color FROM color c where c.descripcion='{color}'")
        if (consulta != []):
            return consulta[0][0]
        else:
            cantidad = self.archivo.realizarSQL(f"SELECT count(*) FROM color c")
            cantidad = cantidad[0][0]
            self.archivo.realizarInsertSQL(
                f"insert into color values('{cantidad + 1}','{color}','A')")
            return cantidad + 1

    def manejoRaza(self, raza):
        consulta = self.archivo.realizarSQL(
            f"SELECT r.id_raza FROM raza r WHERE r.descripcion='{raza}'")
        if (consulta != []):
            return consulta[0][0]
        else:
            cantidad = self.archivo.realizarSQL(f"SELECT count(*) FROM raza r")
            cantidad = cantidad[0][0]
            self.archivo.realizarInsertSQL(
                f"insert into raza values('{cantidad + 1}','{raza}','A')")
            return cantidad + 1

    def obtenerMascotas(self):
        consulta = "select m.id_mascota as id, m.nombre as nombre , e.descripcion as especie , r.descripcion as raza, c.descripcion as color, m.peso as peso, m.fecha_nacimiento as fecha_nacimiento , m.usuario_propietario as propietario from mascota m, especie e, raza r, color c where m.especie=e.id_especie AND m.raza=r.id_raza AND m.color=c.id_color AND m.estado='A' group by m.id_mascota, m.nombre, e.descripcion, r.descripcion, c.descripcion, m.peso, m.fecha_nacimiento, m.usuario_propietario"
        resultado = self.archivo.realizarSQL(consulta)
        if (resultado == []):
            return "No existen mascotas"
        else:
            return resultado

    def obtenerMascotasID(self):
        consulta = f"select m.id_mascota from mascota m where m.estado='A'"
        resultado = self.archivo.realizarSQL(consulta)
        if (resultado == []):
            return "No existe esa mascota"
        else:
            return resultado

    def obtenerMascotasporPropietario(self):
        consulta = f"select m.usuario_propietario, count(*) from mascota m where m.estado='A' group by 1"
        resultado = self.archivo.realizarSQL(consulta)
        if (resultado == []):
            return "No existe esa mascota"
        else:
            return resultado

    def obtenerMascotasporUsuario(self, username):
        consulta = f"select m.id_mascota as id, m.nombre as nombre , e.descripcion as especie , r.descripcion as raza, c.descripcion as color, m.peso as peso, m.fecha_nacimiento as fecha_nacimiento from mascota m, especie e, raza r, color c where m.especie=e.id_especie AND m.raza=r.id_raza AND m.color=c.id_color AND m.estado='A' AND m.usuario_propietario='{username}'group by m.id_mascota, m.nombre, e.descripcion, r.descripcion, c.descripcion, m.peso, m.fecha_nacimiento, m.usuario_propietario"
        resultado = self.archivo.realizarSQL(consulta)
        if (resultado == []):
            return "No existe esa mascota"
        else:
            return resultado
