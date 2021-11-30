from co.edu.unbosque.model.Archivo import Archivo


class Servicio:
    def __init__(self):
        self.archivo = Archivo()
        self.crearServicios()

    def crearServicios(self):
        if (self.archivo.realizarSQL("select * from servicio") == []):
            sql1 = "insert into servicio values ('1','Administración de medicamentos','15000','A')"
            sql2 = "insert into servicio values ('2','Vacunas','20000','A')"
            sql3 = "insert into servicio values ('3','Baño','18000','A')"
            sql4 = "insert into servicio values ('4','Consulta','10000','A')"
            sql5 = "insert into servicio values ('5','Hospitalización','18000','A')"
            sql6 = "insert into servicio values ('6','Cirugía','25000','A')"
            sql7 = "insert into servicio values ('7','Desparasitación inyección','12000','A')"
            sql8 = "insert into servicio values ('8','Desparasitación tabletas','9000','A')"
            sql9 = "insert into servicio values ('9','Cremación','8000','A')"
            self.archivo.realizarInsertSQL(sql1)
            self.archivo.realizarInsertSQL(sql2)
            self.archivo.realizarInsertSQL(sql3)
            self.archivo.realizarInsertSQL(sql4)
            self.archivo.realizarInsertSQL(sql5)
            self.archivo.realizarInsertSQL(sql6)
            self.archivo.realizarInsertSQL(sql7)
            self.archivo.realizarInsertSQL(sql8)
            self.archivo.realizarInsertSQL(sql9)
    def validarID(self, id):
        r= self.archivo.realizarInsertSQL(f"selet * from servicio s where s.id_servicio='{id}'")
        if r==[] or r=="Ocurrio un error":
            return "Ocurrio un error"
        else:
            return 'OK'