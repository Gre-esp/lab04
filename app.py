from functools import wraps
from flask import Flask, render_template, request, redirect, session, g
from models.cliente import Cliente
from models.producto import Producto

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/registro', methods=["get", "post"])
def registration():
    if request.method == "POST":
        user = Cliente(nombres=request.form["name"], email=request.form["email"], password=request.form["password"])
        estado_op = user.crear_cuenta()
        if estado_op:
            return redirect("inicio-sesion")
        else:
            error = 'Invalid email'
            return render_template('users/register.html', error=error)

    return render_template('users/register.html', request=request)


@app.route('/inicio-sesion', methods=["get", "post"])
def login():
    if request.method == "POST":

        user = Cliente.obtener_usuario(email=request.form["email"])

        # Simple password validation
        if request.form["password"] == user.password:
            session['user_name'] = user.nombres
            session['user_email'] = user.email
            return redirect("/")
        else:
            error = 'Invalid password'
            return render_template('users/login.html', error=error)

    return render_template('users/login.html')

# Funcion solo permitir el ingreso si estas logueado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['user_name'] is None:
            return redirect('inicio-sesion')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/logout')
@login_required
def logout():
    session['user_name'] = None
    session['user_email'] = None
    return redirect("/")

@app.route('/productos',methods=["get"])
def product_list():
    productos= Producto.obtener_productos()
    return render_template('layouts/productos.html', productos=productos)

@app.route('/producto/<idproducto>',methods=["get"])
def product_detail(idproducto):
    productos= Producto.obtener_producto(idproducto)
    return render_template('layouts/product_detail.html', productos=productos)





if __name__ == "__main__":
    app.secret_key = "clave_super_ultra_secreta"

    app.run(debug=True)

