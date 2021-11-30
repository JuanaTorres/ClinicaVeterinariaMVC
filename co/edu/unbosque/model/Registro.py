from co.edu.unbosque.model.Archivo import Archivo


class Registro:

    def __init__(self):
        self.archivo = Archivo()

    def realizarRegistro(self, fecha, descripcion, mascota, veterinario):
        veterinario = self.archivo.realizarSQL(f"select u.username from usuario u, rol r where r.descripcion='VETERINARIO'AND r.id_rol=u.rol AND u.username='{veterinario}'")
        if veterinario == []:
            return "No existe veterinario"
        else:
            cantidad = self.archivo.realizarSQL("select count(*) from registrohistorico ")
            cantidad = cantidad[0][0]
            consulta = f"insert into registrohistorico values('{cantidad + 1}','{fecha}','{descripcion}','{mascota}', '{veterinario[0][0]}','A')"
            return self.archivo.realizarInsertSQL(consulta)

    def obtenerRegistrosPorVeterinario(self):
        consulta = "select r.usuario_veterinario , count(*) from registrohistorico r group by 1"
        resultado = self.archivo.realizarSQL(consulta)
        if (resultado == []):
            return "No existen datos"
        else:
            return resultado

    def obtenerRegistro(self, usuarioV):
        consulta = f"select r.id_registro , r.fecha, r.descripcion ,r.id_mascota from registrohistorico r where r.usuario_veterinario='{usuarioV}' AND r.estado='A' "
        resultado = self.archivo.realizarSQL(consulta)
        if (resultado == []):
            return "No existe datos"
        else:
            return resultado
    def obtenerIDRegistro(self):
        consulta =f"select r.id_registro from registrohistorico r where r.estado='A'"
        resultado = self.archivo.realizarSQL(consulta)
        if (resultado == []):
            return "No existe datos"
        else:
            return resultado
