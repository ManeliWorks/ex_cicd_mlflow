# libraries
from flask import Flask, render_template, url_for, redirect, flash # for app
from flask_sqlalchemy import SQLAlchemy # for database
from flask_wtf.csrf import CSRFProtect # for url security
from werkzeug.security import generate_password_hash, check_password_hash # for password security
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user # user session management
import os
from datetime import datetime
from forms import UserForm, LoginForm, ResultForm
from model import predict_price

# app setup
app = Flask(__name__)
csrf = CSRFProtect(app)

# create database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", default=os.urandom(24))

# login management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # redirect to login page if not logged in




db = SQLAlchemy(app)

# User Model for SQLAlchemy
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    result = db.relationship("userResult", backref='author', lazy=True)



class userResult(db.Model):
    __tablename__ = "user_result"
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(100), nullable=False)
    cut = db.Column(db.String(100), nullable=False)
    clarity = db.Column(db.String(100), nullable=False)
    carat = db.Column(db.Float, nullable=False)
    depth = db.Column(db.Float, nullable=False)
    table = db.Column(db.Float, nullable=False)
    x = db.Column(db.Float, nullable=False)
    y = db.Column(db.Float, nullable=False)
    z = db.Column(db.Float, nullable=False)
    result = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
# Create the database tables
with app.app_context():
    db.create_all()

# store user session information
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# home page
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = UserForm()
    if form.validate_on_submit():

        fullname = form.fullname.data
        username = form.username.data
        email = form.email.data
        password = form.password.data

        if User.query.filter_by(username=username).first():
            flash("Username already taken, please choose a different one.", "danger")
            return redirect(url_for("register"))

        if User.query.filter_by(email=email).first():
            flash("Email already registered, please use a different one.", "danger")
            return redirect(url_for("register"))
        password_hash = generate_password_hash(password)
        new_user = User(fullname=fullname, username=username, email=email, password=password_hash)
        db.session.add(new_user)
        db.session.commit()

        flash("Successfully registered! Please log in.", "success")
        return redirect(url_for("login"))

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}", "danger")

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                flash("Login successful!", "success")
                return redirect(url_for("profile"))
            else:
                print("Password mismatch")
        else:
            print("User not found")

        flash("Invalid username or password", "danger")

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}", "danger")

    return render_template("login.html", form=form)


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@app.route("/result", methods=["GET", "POST"])
@login_required
def result():
    form = ResultForm()
    if form.validate_on_submit():

        color = form.color.data
        cut = form.cut.data
        clarity = form.clarity.data
        carat = form.carat.data
        depth = form.depth.data
        table = form.table.data
        x = form.x.data
        y = form.y.data
        z = form.z.data
        input_data = {
            "color": color,
            "cut": cut,
            "clarity": clarity,
            "carat": carat,
            "depth": depth,
            "table": table,
            "x": x,
            "y": y,
            "z": z}

        calculated_result = predict_price(input_data)

        # Save the result
        new_result = userResult(
            color=color, cut=cut, clarity=clarity, carat=carat, depth=depth,
            table=table, x=x, y=y, z=z, result=calculated_result, user_id=current_user.id
        )
        db.session.add(new_result)
        db.session.commit()

        flash("Result calculated and saved!", "success")
        return redirect(url_for("profile"))

    return render_template("result.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()  # Logs the user out
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("home"))  # Redirect to home page or login page


if __name__ == "__main__":
    app.run(debug=True)