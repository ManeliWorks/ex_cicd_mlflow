# libraries
from flask import Flask, request, render_template, url_for, redirect, flash # for app
from flask_sqlalchemy import SQLAlchemy # for database
from flask_wtf import FlaskForm # for input data
from wtforms import StringField, PasswordField, SubmitField, # take this data as form
from wtforms.validators import DataRequired, Regexp, Length, Email
from flask_wtf.csrf import CSRFProtect # for url security
from werkzeug.security import generate_password_hash, check_password_hash # for password security
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user # user session management
import uuid
import os


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
    # result = db.relationship("userResult", backref='author', lazy=True)

    def __init__(self, fullname, username, email, password):
        self.fullname = fullname
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)  

# Create the database tables
with app.app_context():
    db.create_all()

# store user session information
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class UserForm(FlaskForm):
    fullname = StringField(label="Full Name", validators=[
        DataRequired(),
        Length(max=100, message="Full name must be under 100 characters.")
    ])
    username = StringField(label="Username", validators=[
        DataRequired(),
        Regexp(
            regex="^[a-zA-Z0-9_]{3,10}$",
            message="Username must be between 3 and 10 characters and can only contain letters, numbers, and underscores."
        )
    ])
    email = StringField(label="Email", validators=[
        DataRequired(),
        Email(message="Please enter a valid email address.")
    ])
    password = PasswordField(label="Password", validators=[
        DataRequired(),
        Length(min=6, message="Password must be at least 6 characters long.")
    ])
    
class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])

    submit = SubmitField(label='Login')

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
        if user and check_password_hash(user.password, password):
            # Log the user in using Flask-Login
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("profile"))
        else:
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


@app.route("/logout")
@login_required
def logout():
    logout_user()  # Logs the user out
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("home"))  # Redirect to home page or login page


if __name__ == "__main__":
    app.run(debug=True)