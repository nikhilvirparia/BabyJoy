from flask_app import app
# from flask_app.models.baby import Painting
from flask_app.models.user import User
from flask_app.models.product import Product
from flask_app.models.product import Product2
from flask import render_template, redirect, session, request, flash

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# ============================
# Dashboard Route
# ============================

@app.route("/dashboard")
def dashboard():
    if not 'user_id' in session:
        return redirect("/")

    data = {
        "user_id": session['user_id']
    }
    lists = Product.search('baby food')
    user = User.get_user_info(data)
    return render_template("dashboard.html", user=user, lists = lists)

@app.route("/product/<itemId>")
def product(itemId):
    if not 'user_id' in session:
        return redirect("/")

    data = {
        "user_id": session['user_id']
    }
    product = Product.getOne(itemId)
    user = User.get_user_info(data)
    return render_template("product.html", user=user, product = product)

@app.route("/babyfood")
def babyfood():
    if not 'user_id' in session:
        return redirect("/")

    data = {
        "user_id": session['user_id']
    }
    lists = Product2.search('baby food')
    user = User.get_user_info(data)
    return render_template("babyfood.html", user=user, lists = lists)

@app.route("/snacks")
def snack():
    if not 'user_id' in session:
        return redirect("/")

    data = {
        "user_id": session['user_id']
    }
    lists = Product2.search('organic baby snacks')
    user = User.get_user_info(data)
    return render_template("snacks.html", user=user, lists = lists)

@app.route("/formula")
def formula():
    if not 'user_id' in session:
        return redirect("/")

    data = {
        "user_id": session['user_id']
    }
    lists = Product2.search('formula')
    user = User.get_user_info(data)
    return render_template("formula.html", user=user, lists = lists)

@app.route("/organicfood")
def organic():
    if not 'user_id' in session:
        return redirect("/")

    data = {
        "user_id": session['user_id']
    }
    lists = Product2.search('organic baby food')
    user = User.get_user_info(data)
    return render_template("organicfood.html", user=user, lists = lists)

@app.route("/addtocart/<itemId>")
def cart(itemId):
    if not 'user_id' in session:
        return redirect("/")
    if not 'cart' in session:
        session['cart'] = []
    session['cart'].append(itemId)
    products=[] 
    for id in session['cart']:
        product = Product.getOne(id) 
        products.append(product)
    data = {
        "user_id": session['user_id']
    }
    
    # lists = Product2.search(query)
    user = User.get_user_info(data)
    return render_template("addtocart.html", user=user, products = products)

@app.route("/addtocart")
def add():
    if not 'user_id' in session:
        return redirect("/")
    products=[] 
    if 'cart' in session:
        
        for id in session['cart']:
            product = Product.getOne(id) 
            products.append(product)
    data = {
        "user_id": session['user_id']
    }
    
    # lists = Product2.search(query)
    user = User.get_user_info(data)
    return render_template("addtocart.html", user=user, products = products)



@app.route("/search", methods = ['POST'])
def search():
    if not 'user_id' in session:
        return redirect("/")
    query = request.form['search']
    # query = "search" : request.form[‘search’]
    
    data = {
        "user_id": session['user_id']
    }

    lists = Product2.search(query)
    user = User.get_user_info(data)
    return render_template("search.html", user=user, lists = lists)    

@app.route('/checkout') 
def checkout():
    if not 'user_id' in session:
        return redirect("/")
    data = {
        "user_id": session['user_id']
        }
    user = User.get_user_info(data)
    session['cart'].pop()
    return render_template("checkout.html", user=user)