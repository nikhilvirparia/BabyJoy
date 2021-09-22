from flask_app.models.user import User
from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# ============================
# Render Login/Reg Route
# ============================


@app.route("/")
def index():

    return render_template("index.html")

# ============================
# Register Route
# ============================


@app.route("/register", methods=['POST'])
def register():

    # validate user
    if not User.validate_register(request.form):
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }

    # Call the save @classmethod on User
    user_id = User.register_user(data)

    # store user id into session
    session['user_id'] = user_id
    return redirect("/dashboard")

# ============================
# Login Route
# ============================

@app.route("/login", methods=["POST"])
def login():

    data = {
        "email": request.form["email"]
    }
    
    user_in_db = User.get_by_email(data)

    validation_data = {
        "user" : user_in_db,
        "password" : request.form['password']
    }
    
    if not User.validate_login(validation_data):
        return redirect("/")

    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/dashboard")


# ============================
# Logout Route
# ============================

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")