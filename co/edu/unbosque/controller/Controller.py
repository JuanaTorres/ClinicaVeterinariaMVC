import os
from co.edu.unbosque.model import Usuario
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
    @app.route('/')
    def principal():
        return render_template('index.html')

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
                print(rol)
                rol = rol[0][0].lower()
                return render_template(f'{rol}.html', QTc_result=username)
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
