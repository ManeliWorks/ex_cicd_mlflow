from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .database_models import db, User, userResult
from .forms import UserForm, LoginForm, ResultForm
from .model import predict_price
from . import login_manager
main = Blueprint("main", __name__)

# store user session information
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.login_view = "login"

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/register", methods=["GET", "POST"])
def register():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = generate_password_hash(form.password.data)

        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "danger")
            return redirect(url_for("main.register"))
        
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "danger")
            return redirect(url_for("main.register"))

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful!", "success")
        return redirect(url_for("main.login"))
    
    return render_template("register.html", form=form)

@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("main.profile"))
        flash("Invalid username or password.", "danger")
    return render_template("login.html", form=form)

@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@main.route("/result", methods=["GET", "POST"])
@login_required
def result():
    form = ResultForm()
    if form.validate_on_submit():
        input_data = {
            "color": form.color.data,
            "cut": form.cut.data,
            "clarity": form.clarity.data,
            "carat": form.carat.data,
            "depth": form.depth.data,
            "table": form.table.data,
            "x": form.x.data,
            "y": form.y.data,
            "z": form.z.data,
        }
        result = predict_price(input_data)
        new_result = userResult(**input_data, result=result, user_id=current_user.id)
        db.session.add(new_result)
        db.session.commit()
        flash("Result saved!", "success")
        return redirect(url_for("main.profile"))
    return render_template("result.html", form=form)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("main.home"))
