import Archivo

class Mascota:

    def __init__(self):
        self.archivo = Archivo.Archivo()

    def crearMascota(self, nombre, especie, raza, color, peso, fecha, propietario):
        valorEspecie = self.manejoEspecie(especie)
        valorRaza = self.manejoRaza(raza)
        valorColor = self.manejoColor(color)
        nombre = nombre.low.replace(' ', '')
        sql = f"SELECT * FROM mascota m where m.nombre={nombre} AND m.especie={valorEspecie} AND m.raza={valorRaza} AND m.color={valorColor} AND m.peso={peso} AND m.fecha_nacimiento={fecha} AND usuario_propietario={propietario}"
        if (self.archivo.realizarSQL(sql) != []):
            return "Ya existe una mascota con esos datos"
        else:
            sql = f"INSERT INTO mascota values('{nombre}', '{especie}', '{raza}', '{color}', '{peso}', '{fecha}', '{propietario}'.'A')"
            return self.archivo.realizarInsertSQL(sql)

    def manejoEspecie(self, especie):
        consulta = self.archivo.realizarSQL(
            f"SELECT e.id_especie FROM especie e where e.descripcion={especie.low.replace(' ', '')}")
        if (consulta != []):
            return consulta
        else:
            cantidad = self.archivo.realizarSQL(f"SELECT count(*) FROM especie e")
            cantidad=cantidad[0][0]
            self.archivo.realizarInsertSQL(
                f"insert into especie values('{cantidad + 1}','{especie.low.replace(' ', '')}','A')")
            return cantidad + 1

    def manejoColor(self, color):
        consulta = self.archivo.realizarSQL(
            f"SELECT c.id_color FROM color c where c.descripcion={color.low.replace(' ', '')}")
        if (consulta != []):
            return consulta
        else:
            cantidad = self.archivo.realizarSQL(f"SELECT count(*) FROM color c")
            cantidad = cantidad[0][0]
            self.archivo.realizarInsertSQL(
                f"insert into color values('{cantidad + 1}','{color.low.replace(' ', '')}','A')")
            return cantidad + 1

    def manejoRaza(self, raza):
        consulta = self.archivo.realizarSQL(
            f"SELECT r.id_raza FROM raza r WHERE r.descripcion={raza.low.replace(' ', '')}")
        if (consulta != []):
            return consulta
        else:
            cantidad = self.archivo.realizarSQL(f"SELECT count(*) FROM raza r")
            cantidad = cantidad[0][0]
            self.archivo.realizarInsertSQL(
                f"insert into raza values('{cantidad + 1}','{raza.low.replace(' ', '')}','A')")
            return cantidad + 1

    def obtenerMascotas(self):
        consulta = "select m.id_mascota as id, m.nombre as nombre , e.descripcion as especie , r.descripcion as raza, c.descripcion as color, m.peso as peso, m.fecha_nacimiento as fecha_nacimiento , m.usuario_propietario as propietario from mascota m, especie e, raza r, color c where m.especie=e.id_especie AND m.raza=r.id_raza AND m.color=c.id_color AND m.estado='A' group by m.id_mascota, m.nombre, e.descripcion, r.descripcion, c.descripcion, m.peso, m.fecha_nacimiento, m.usuario_propietario"
        resultado = self.archivo.realizarSQL(consulta)
        if (resultado == []):
            return "No existen mascotas"
        else:
            return resultado

    def obtenerMascotaPorID(self, id):
        consulta = f"select m.id_mascota, m.nombre, e.descripcion, r.descripcion, c.descripcion, m.peso, m.fecha_nacimiento, m.usuario_propietario from mascota m, especie e, raza r, color c where m.especie=e.id_especie AND m.raza=r.id_raza AND m.color=c.id_color AND m.estado='A' group by m.id_mascota, m.nombre, e.descripcion, r.descripcion, c.descripcion, m.peso, m.fecha_nacimiento, m.usuario_propietario AND m.id_mascota={id}"
        resultado = self.archivo.realizarSQL(consulta)
        if (resultado == []):
            return "No existe esa mascota"
        else:
            return resultado
    def obtenerMascotasporPropietario(self):
        consulta=f"select m.usuario_propietario, count(*) from mascota m group by 1"
        resultado = self.archivo.realizarSQL(consulta)
        if (resultado == []):
            return "No existe esa mascota"
        else:
            return resultado