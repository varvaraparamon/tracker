from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import db, User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_field = request.form.get("login", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(login=login_field).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("index"))
        flash("Неверный логин или пароль", "error")
    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
