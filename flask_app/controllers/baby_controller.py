from flask_app import app
# from flask_app.models.baby import Painting
from flask_app.models.user import User
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

    user = User.get_user_info(data)
    return render_template("dashboard.html", user=user)
    # all_paintings = Painting.get_all_paintings()

    # return render_template("dashboard.html", user=user, paintings=all_paintings)

@app.route("/babyfood")
def babyfood():
    if not 'user_id' in session:
        return redirect("/")

    data = {
        "user_id": session['user_id']
    }
    user = User.get_user_info(data)
    return render_template("babyfood.html", user=user)

# @app.route("/snacks")
# def snack():
#     if not 'user_id' in session:
#         return redirect("/")

#     data = {
#         "user_id": session['user_id']
#     }
#     user = User.get_user_info(data)
#     return render_template("snacks.html", user=user)
