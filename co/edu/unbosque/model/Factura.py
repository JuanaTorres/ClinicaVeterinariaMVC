from co.edu.unbosque.model.Archivo import Archivo
from co.edu.unbosque.model.Servicio import Servicio


class Factura:
    def __init__(self):
        self.archivo = Archivo()
        self.servicio = Servicio()

    def generarFactura(self, fecha, total, id_registro, listaServicios):
        if self.archivo.realizarSQL(f"select * from factura f where f.id_registro = '{id_registro}'"):
            return "Ya existe una factura con ese id de registro"
        else:
            cantidad = self.archivo.realizarSQL("select count(*) from factura")
            cantidad = cantidad[0][0]
            r = self.archivo.realizarInsertSQL(
                f"insert into factura values('{cantidad + 1}', '{fecha}', '{total}','{id_registro}')")
            if r != "OK":
                return r
            else:
                for i in listaServicios:
                    if self.servicio.validarID(i) == "OK":
                        a = self.generarDetalleFactura(cantidad + 1, i)
                        if a != "OK":
                            self.archivo.realizarInsertSQL(f"delete from factura f where f.nfactura='{cantidad+1}'")
                            return a

    def obtenerFacturaMascota(self, id_mascota):
        r = self.archivo.realizarInsertSQL(f"select f.nfactura,f.tarifa from factura f, registrohistorico r, mascota ma  where f.id_registro=r.id_registro and r.id_mascota=ma.id_mascota and r.id_mascota='{id_mascota}')")
        return r
    def generarDetalleFactura(self, nfactura, id_servicio):
        r = self.archivo.realizarInsertSQL(f"insert into facturadetalle values('{id_servicio}', '{nfactura}')")
        return r

    def obtenerTotalFacturas(self):
        consulta = "select  count (*) as cantidad ,sum(f.tarifa) as Total from facturas f"
        resultado = self.archivo.realizarSQL(consulta)
        if resultado == []:
            return "No existen datos"
        else:
            return resultado