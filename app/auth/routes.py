from flask import (render_template,redirect,request,url_for,flash,session,current_app)
from werkzeug.security import (generate_password_hash,check_password_hash)
from app.models.User import User
from app.models.role import Role
from app.auth import auth
from app.extension import db
import secrets

from flask_login import (login_user,logout_user)
from app.auth.form import (RegisterForm,LoginForm,ForgetPassword,ResetPassword)
from app.auth.service import generate_token,verification_email,reset_password_email
@auth.route("/register",methods=["GET","POST"])

def register():
  
  form = RegisterForm()
 
  if form.validate_on_submit():
    
    existing = User.query.filter_by(email=form.email.data).first()
    if existing:
      flash("email is exist use another")
      return redirect(url_for('auth.register'))
    custormer_role =Role.query.filter_by(name="Customer").first() 
    
    user =User(name=form.name.data,
    email=form.email.data,
    password=generate_password_hash(form.password.data),
    role=custormer_role,
    email_verified=False,
    email_verification_token=generate_token()
    )
    db.session.add(user)
    db.session.commit()
    verification_email(user)
    flash("account create succesfuly"
         
         )
    
  
    
    return redirect(url_for("auth.login"))
  return render_template("auth/register.html",form=form)
@auth.route("/verify-email/<token>")
def verify_email(token):

  user = User.query.filter_by(
    email_verification_token=token
  ).first()

  if not user:

    flash(
      "Invalid or expired verification link.",
       "danger"
     )

    return redirect(
      url_for("auth.login")
    )

  user.email_verified = True

  user.email_verification_token = None

  db.session.commit()

  flash(
    "Your email has been verified successfully. You can now login.",
      "success"
   )

  return redirect(
    url_for("auth.login")
    
  )
@auth.route("/login", methods =["GET","POST"])
def login():
  
  form = LoginForm()
  if form.validate_on_submit():
    
    user = User.query.filter_by(email=form.email.data).first()

    if user and check_password_hash(user.password,form.password.data):
      if  user.email_verified is False:
        flash("please  verify your email before continue login","warning")
        return redirect(url_for("auth.login"))
      login_user(user)
      flash("login succesfuly")
      if user.role and user.role.name=="Admin":
        return redirect(url_for("admin.dashboard"))
      return redirect(url_for("shop.home"))
    else:
      flash("email and password is incorrect")
  return render_template("auth/login.html",form=form)
@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    form = ForgetPassword()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user:

            user.password_reset_token = generate_token()

            db.session.commit()

            reset_password_email(user)

        flash(
            "If that email exists, a password reset link has been sent.",
            "info"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "auth/forgetpassword.html",
        form=form
    )
@auth.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):

    user = User.query.filter_by(
        password_reset_token=token
    ).first()

    if not user:

        flash(
            "Invalid or expired password reset link.",
            "danger"
        )

        return redirect(
            url_for("auth.login")
        )

    form = ResetPassword()

    if form.validate_on_submit():

        user.password = generate_password_hash(
            form.password.data
        )

        user.password_reset_token = None

        db.session.commit()

        flash(
            "Your password has been reset successfully. You can now login.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "auth/resetpassword.html",
        form=form
    )
@auth.route("/logout")
def logout():
  logout_user()
  flash("logout succesfuly")
  return redirect("/")
  