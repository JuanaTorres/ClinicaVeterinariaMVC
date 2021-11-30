from co.edu.unbosque.model.Archivo import Archivo
from co.edu.unbosque.model.Servicio import Servicio


class Factura:
    def __init__(self):
        self.archivo = Archivo()
        self.servicio = Servicio()

    def generarFactura(self, fecha, total, id_registro, listaServicios):
        cantidad = self.archivo.realizarSQL("select count(*) from factura")
        cantidad = cantidad[0][0]
        r = self.archivo.realizarInsertSQL(
            f"insert into factura values('{cantidad + 1}', '{fecha}', '{total}','{id_registro}'")
        if r != "OK":
            return r
        else:
            for i in listaServicios:
                if self.servicio.obtenerIdServicio(i) == "OK":
                    a = self.generarDetalleFactura(cantidad + 1, i)
                    if a != "OK":
                        return a

    def generarDetalleFactura(self, nfactura, id_servicio):
        r = self.archivo.realizarInsertSQL(f"insert into detallefactura values('{id_servicio}', '{nfactura}'")
        return r

    def obtenerTotalFacturas(self):
        consulta = "select  count (*) as cantidad ,sum(f.tarifa) as Total from facturas f"
        resultado = self.archivo.realizarSQL(consulta)
        if resultado == []:
            return "No existen datos"
        else:
            return resultado