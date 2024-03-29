from co.edu.unbosque.model.Archivo import Archivo
from co.edu.unbosque.model.Factura import Factura

class Formapago:
    def __init__(self):
        self.archivo = Archivo()
        self.factura = Factura()
    def realizarPago(self, nfactura, valor, nombre):
        cantidad = self.archivo.realizarSQL("select count(*) from formapago")
        cantidad = cantidad[0][0]
        if(self.archivo.realizarSQL(f"select * from formapago f where f.nfactura='{nfactura}'")!=[]):
            return "Ya se pago esta factura"
        r = self.archivo.realizarInsertSQL(
            f"insert into formapago values('{cantidad + 1}', '{nfactura}', '{valor}','{nombre}')")
        return r
    def cantidadFormaPago(self):
        r = self.archivo.realizarSQL("select f.nombre, count(*) from formapago f group by 1")
        return r