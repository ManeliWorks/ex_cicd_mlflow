from flask_wtf import FlaskForm # for input data
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, Regexp, Length, Email



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
    submit = SubmitField(label='submit')

    
class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])

    submit = SubmitField(label='Login')


class ResultForm(FlaskForm):
    color = StringField("Color", validators=[DataRequired()])
    cut = SelectField("Cut", choices=["Fair", "Good", "Very Good", "Premium", "Ideal"], validators=[DataRequired()])
    clarity = StringField("Clarity", validators=[DataRequired()])
    carat = FloatField("Carat", validators=[DataRequired()])
    depth = FloatField("Depth", validators=[DataRequired()])
    table = FloatField("Table", validators=[DataRequired()])
    x = FloatField("X", validators=[DataRequired()])
    y = FloatField("Y", validators=[DataRequired()])
    z = FloatField("Z", validators=[DataRequired()])
    submit = SubmitField("Submit")