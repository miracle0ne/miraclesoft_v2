from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo
)


class RegisterForm(FlaskForm):

    name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )


    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )


    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )


    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Passwords must match"
            )
        ]
    )


    submit = SubmitField(
        "Register"
    )



class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )


    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )


    submit = SubmitField(
        "Login"
    )
class ForgetPassword(FlaskForm):
  email = StringField("Email",
                      validators=[DataRequired(),Email()])
  submit=SubmitField("send reset link")
class ResetPassword(FlaskForm):
  password =PasswordField("New password",
                          validators=[DataRequired(),
                                      Length(min=6)])
  confirm_password=PasswordField("confirm password",
                                 validators=[DataRequired(),
                                             EqualTo("password")])
  submit =SubmitField("reset password")