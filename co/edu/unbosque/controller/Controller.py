import os

from co.edu.unbosque.model import Usuario
from co.edu.unbosque.model import Mascota
from co.edu.unbosque.model import Factura
from co.edu.unbosque.model import Formapago
from co.edu.unbosque.model import Registro
from co.edu.unbosque.model import Servicio
from flask import Flask, render_template, request, flash, redirect, url_for
import secrets


class Controller:
    app = Flask(__name__,
                template_folder='../view/templates',
                static_folder=os.path.abspath('../view/static'))

    def __init__(self):
        secret = secrets.token_urlsafe(32)
        self.app.secret_key = secret
        self.app.run()

    @staticmethod
    @app.route('/detfactura', methods=['GET', 'POST'])
    def detfactura():
        username = request.args.get('username')
        a = request.args.get('a', 0, type=int)
        usuario = Usuario.Usuario()
        servicio = Servicio.Servicio()
        factura1 = (Factura.Factura().obtenerdetServico(a))
        rol = usuario.obtenerRol(username)
        mascota = Controller.listaMascotas(username)
        factura = Controller.listaFactura(username)
        data = Controller.listaMascotasID()
        regis = Controller.listaRegistroID(username)
        detalle = []
        for i in range(0, len(factura1)):
            s = servicio.obtenerServicios(factura1[i][0])
            for j in range(0, len(s)):
                detalle.append(s[j])
        return render_template(f'{rol}.html', QTc_result=username, colour=data, regis=regis, mascota=mascota,
                               factura=factura, detalle=detalle)

    @staticmethod
    @app.route('/')
    def principal():
        return render_template('index.html')

    @staticmethod
    def listaMascotasID():
        mascota = Mascota.Mascota()
        idmascota = mascota.obtenerMascotasID()
        data = []
        if (idmascota == "No existe datos"):
            return ["","No existe datos"]
        for i in range(0, len(idmascota)):
            data.append(idmascota[i][0])
        return data

    @staticmethod
    def listaRegistro(username):
        registro = Registro.Registro()
        historico = registro.obtenerRegistro(username)
        data = []
        if (historico == "No existe datos"):
            return ""
        for i in range(0, len(historico)):
            data.append(historico[i])
        return data

    @staticmethod
    def listaUsuariosRol():
        usuario = Usuario.Usuario()
        list = usuario.obtenerUsuarioporTipo()
        data = []
        if (list == "No existe datos"):
            return ""
        for i in range(0, len(list)):
            data.append(list[i])
        return data

    @staticmethod
    def listaMascotaPropietario():
        mascota = Mascota.Mascota()
        list = mascota.obtenerMascotasporPropietario()
        data = []
        if (list == "No existe datos"):
            return ""
        for i in range(0, len(list)):
            data.append(list[i])
        return data

    @staticmethod
    def listaRegistroVet():
        registro = Registro.Registro()
        list = registro.obtenerRegistrosPorVeterinario()
        data = []
        if (list == "No existe datos"):
            return ""
        for i in range(0, len(list)):
            data.append(list[i])
        return data

    @staticmethod
    def listafacturasT():
        facturas = Factura.Factura()
        list = facturas.obtenerTotalFacturas()
        data = []
        if (list == "No existe datos"):
            return ""
        for i in range(0, len(list)):
            data.append(list[i])
        return data

    @staticmethod
    def listaFactura(username):
        mascota = Mascota.Mascota()
        idmascota = mascota.obtenerMascotasporUsuario(username)
        data = []
        if (idmascota == "No existe esa mascota"):
            return ""
        for i in range(0, len(idmascota)):
            factura = (Factura.Factura().obtenerFacturaMascota(idmascota[i][0]))
            for j in range(0, len(factura)):
                data.append(factura[j])
        return data

    @staticmethod
    def listaMascotas(username):
        mascota = Mascota.Mascota()
        idmascota = mascota.obtenerMascotasporUsuario(username)
        data = []
        if (idmascota == "No existe esa mascota"):
            return ""
        for i in range(0, len(idmascota)):
            data.append(idmascota[i])
        return data

    @staticmethod
    def listaRegistroID(username):
        registro = Registro.Registro()
        idregistro = registro.obtenerIDRegistro(username)
        data = []
        if (idregistro == "No existe datos"):
            return ["","No existe datos"]
        for i in range(0, len(idregistro)):
            data.append(idregistro[i][0])
        return data

    @staticmethod
    @app.route('/inscripcion.html')
    def principal2():
        return render_template('inscripcion.html')

    @staticmethod
    @app.route('/index.html', methods=['GET', 'POST'])
    def validarUsuario():
        if request.method == 'POST':
            username = request.form.get("user")
            password = request.form.get("password")
            usuario = Usuario.Usuario()
            rol = usuario.validarUsuario(username, password)

            if rol == "No existe este usuario" or rol == "Ocurrio un error":
                flash(rol)
                return redirect(url_for("validarUsuario"))
            else:
                rol = rol[0][0].lower()
                mascota = Controller.listaMascotas(username)
                factura = Controller.listaFactura(username)
                registros = Controller.listaRegistro(username)
                vres = Controller.listaRegistroVet()
                fact = Controller.listafacturasT()
                masc = Controller.listaMascotaPropietario()
                user = Controller.listaUsuariosRol()
                data = Controller.listaMascotasID()
                regis = Controller.listaRegistroID(username)
                if rol == "veterinario" and registros == "":
                    flash("Aun no existen dados para llenar todas las tablas")
                if rol == "propietario" and (mascota == "" or factura == ""):
                    flash("Aun no existen dados para llenar todas las tablas")
                if rol == "administrador" and (user == "" or masc == "" or fact == "" or vres == ""):
                    flash("Aun no existen dados para llenar todas las tablas")
                return render_template(f'{rol}.html', QTc_result=username, colour=data, regis=regis, mascota=mascota,
                                       factura=factura, registros=registros, user=user, masc=masc, fact=fact, vres=vres)
        return render_template('index.html')

    @staticmethod
    @app.route('/inicio', methods=['GET', 'POST'])
    def crearUsuario():
        if request.method == 'POST':
            username = request.form.get("user")
            password = request.form.get("password")
            cedula = request.form.get("cedula")
            telefono = request.form.get("telefono")
            nombre = request.form.get("nombre")
            apellidos = request.form.get("apellido")
            direccion = request.form.get("direccion")
            correo = request.form.get("correo")
            rol = request.form.get("rol")
            usuario = Usuario.Usuario()
            resultado = usuario.crearUsuario(username, password, cedula, telefono, nombre, apellidos, direccion, correo,
                                             rol)

            if resultado != "OK":
                flash(resultado)
                return redirect(url_for("crearUsuario"))
            else:
                return render_template('index.html')
        return render_template('inscripcion.html')

    @staticmethod
    @app.route('/propietario.html', methods=['GET', 'POST'])
    def crearMascota():
        if request.method == 'POST':
            username = request.form.get('username')
            nombre = request.form.get("name")
            especie = request.form.get("species")
            raza = request.form.get("raza")
            peso = request.form.get("peso")
            color = request.form.get("color")
            fecha = request.form.get("fecha")
            mascota = Mascota.Mascota()
            r = mascota.crearMascota(nombre, especie, raza, color, peso, fecha, username)
            if r != "OK" or r == "Ocurrio un error":
                mascota = Controller.listaMascotas(username)
                factura = Controller.listaFactura(username)
                data = Controller.listaMascotasID()
                regis = Controller.listaRegistroID(username)
                if mascota == "" or factura == "":
                    flash(f"{r}\nAun no existen dados para llenar todas las tablas")
                else:
                    flash(r)
                return render_template(f'propietario.html', QTc_result=username, colour=data, regis=regis,
                                       mascota=mascota,
                                       factura=factura)
            else:
                mascota = Controller.listaMascotas(username)
                factura = Controller.listaFactura(username)
                data = Controller.listaMascotasID()
                regis = Controller.listaRegistroID(username)
                if mascota == "" or factura == "":
                    flash("Aun no existen dados para llenar todas las tablas")
                return render_template(f'propietario.html', QTc_result=username, colour=data, regis=regis,
                                       mascota=mascota,
                                       factura=factura)
        return render_template('propietario.html')

    @staticmethod
    @app.route('/cambiarDirrecion', methods=['GET', 'POST'])
    def cambiarDireccion():
        if request.method == 'POST':
            username = request.form.get('username1')
            direccion = request.form.get("dirección")
            usuario = Usuario.Usuario()
            r = usuario.actualizarDireccion(username, direccion)
            print(r)
            if r != "OK" or r == "Ocurrio un error":
                rol = usuario.obtenerRol(username)
                mascota = Controller.listaMascotas(username)
                factura = Controller.listaFactura(username)
                registros = Controller.listaRegistro(username)
                data = Controller.listaMascotasID()
                regis = Controller.listaRegistroID(username)
                if rol == "veterinario" and registros == "":
                    flash(f"{r}\nAun no existen dados para llenar todas las tablas")
                elif rol == "propietario" and (mascota == "" or factura == ""):
                    flash(f"{r}\nAun no existen dados para llenar todas las tablas")
                else:
                    flash(r)
                return render_template(f'{rol}.html', QTc_result=username, colour=data, regis=regis, mascota=mascota,
                                       factura=factura, registros=registros)
            else:
                rol = usuario.obtenerRol(username)
                mascota = Controller.listaMascotas(username)
                factura = Controller.listaFactura(username)
                data = Controller.listaMascotasID()
                regis = Controller.listaRegistroID(username)
                registros = Controller.listaRegistro(username)
                if rol == "veterinario" and registros == "":
                    flash(f"Aun no existen dados para llenar todas las tablas")
                elif rol == "propietario" and (mascota == "" or factura == ""):
                    flash(f"Aun no existen dados para llenar todas las tablas")
                return render_template(f'{rol}.html', QTc_result=username, colour=data, regis=regis,
                                       mascota=mascota, registros=registros,
                                       factura=factura)
        return render_template('index.html')

    @staticmethod
    @app.route('/registro', methods=['GET', 'POST'])
    def crearRegistro():
        if request.method == 'POST':
            username = request.form.get("usernameR")
            fecha = request.form.get("fechaR")
            mascota = request.form.get("idmascota")
            descripcion = request.form.get("descrip")
            registro = Registro.Registro()

            r = registro.realizarRegistro(fecha, descripcion, mascota, username)
            print(mascota, r)
            if r == "No existe este usuario" or r == "Ocurrio un error":
                data = Controller.listaMascotasID()
                registros = Controller.listaRegistro(username)
                regis = Controller.listaRegistroID(username)
                if registros == "":
                    flash(f"{r}\nAun no existen dados para llenar todas las tablas")
                else:
                    flash(r)
                return render_template(f'veterinario.html', QTc_result=username, colour=data, regis=regis,
                                       registros=registros)
            else:
                registros = Controller.listaRegistro(username)
                data = Controller.listaMascotasID()
                regis = Controller.listaRegistroID(username)
                if registros == "":
                    flash(f"Aun no existen dados para llenar todas las tablas")
                return render_template(f'veterinario.html', QTc_result=username, colour=data, regis=regis,
                                       registros=registros)
        return render_template('veterinario.html')

    @staticmethod
    @app.route('/gfactura', methods=['GET', 'POST'])
    def crearFactura():
        if request.method == 'POST':
            username = request.form.get("usernamef")
            fecha = request.form.get("fechaf")
            registro = request.form.get("registroID")
            total = request.form.get("TotalF")
            factura = Factura.Factura()
            lista = []
            if total == "Seleccione los servicios":
                data = Controller.listaMascotasID()
                regis = Controller.listaRegistroID(username)
                registros = Controller.listaRegistro(username)
                if registros == "":
                    flash(f"Debe elegir los serivios prestados\nAun no existen dados para llenar todas las tablas")
                else:
                    flash("Debe elegir los serivios prestados")
                return render_template(f'veterinario.html', QTc_result=username, colour=data, regis=regis,
                                       registros=registros)
            if registro == "No existe datos":
                data = Controller.listaMascotasID()
                regis = Controller.listaRegistroID(username)
                registros = Controller.listaRegistro(username)
                if registros == "":
                    flash(f"No es posible realizar el registro sin id de registro\nAun no existen dados para llenar todas las tablas")
                else:
                    flash("No es posible realizar el registro sin id de registro")
                return render_template(f'veterinario.html', QTc_result=username, colour=data, regis=regis,
                                       registros=registros)
            else:
                for i in range(1, 9):
                    if request.form.get(f"n{i}") != None:
                        lista.append(request.form.get(f"n{i}"))
                r = factura.generarFactura(fecha, total, registro, lista)
                if r != "OK" or r == "Ocurrio un error" or r == "Ya existe una factura con ese id de registro":
                    data = Controller.listaMascotasID()
                    regis = Controller.listaRegistroID(username)
                    registros = Controller.listaRegistro(username)
                    if registros == "":
                        flash(f"{r}\nAun no existen dados para llenar todas las tablas")
                    else:
                        flash(r)
                    return render_template(f'veterinario.html', QTc_result=username, colour=data, regis=regis,
                                           registros=registros)

                else:
                    data = Controller.listaMascotasID()
                    regis = Controller.listaRegistroID(username)
                    registros = Controller.listaRegistro(username)
                    if registros == "":
                        flash(f"Aun no existen dados para llenar todas las tablas")
                    return render_template(f'veterinario.html', QTc_result=username, colour=data, regis=regis,
                                           registros=registros)
        return render_template('veterinario.html')

    @staticmethod
    @app.route('/pagar', methods=['GET', 'POST'])
    def pagarFactura():
        if request.method == 'POST':
            username = request.form.get("usernamep")
            factura = request.form.get("nfactu")
            forma = request.form.get("forma")
            total = request.form.get("ptotal")
            formapago = Formapago.Formapago()

            r = formapago.realizarPago(factura, total, forma)
            if r != "OK" or r == "Ocurrio un error":
                mascota = Controller.listaMascotas(username)
                factura = Controller.listaFactura(username)
                data = Controller.listaMascotasID()
                regis = Controller.listaRegistroID(username)
                if mascota == "" or factura == "":
                    flash(f"{r}\nAun no existen dados para llenar todas las tablas")
                else:
                    flash(r)
                return render_template(f'propietario.html', QTc_result=username, colour=data, regis=regis,
                                       mascota=mascota,
                                       factura=factura)
            else:
                mascota = Controller.listaMascotas(username)
                factura = Controller.listaFactura(username)
                data = Controller.listaMascotasID()
                regis = Controller.listaRegistroID(username)
                if mascota == "" or factura == "":
                    flash(f"Aun no existen dados para llenar todas las tablas")
                return render_template(f'propietario.html', QTc_result=username, colour=data, regis=regis,
                                       mascota=mascota,
                                       factura=factura)
        return render_template('propietario.html')
