from flask import (render_template,redirect,request,url_for,flash,session)
from werkzeug.security import (generate_password_hash,check_password_hash)
from app.models.User import User
from app.models.role import Role
from app.auth import auth
from app.extension import db
from flask_login import (login_user,logout_user)
from app.auth.form import (RegisterForm,LoginForm)
print("===auth_load==")
@auth.route("/register",methods=["GET","POST"])

def register():
  print("register called")
  form = RegisterForm()
 
  if form.validate_on_submit():
    print("form valid")
    print(",form ok")
    print("name",form.data)
    print("email",request.form)
    print("valide",form.validate())
    print("erros",form.errors)
    existing = User.query.filter_by(email=form.email.data).first()
    if existing:
      flash("email is exist use another")
      return redirect(url_for('auth.register'))
    custormer_role =Role.query.filter_by(name="Customer").first() 
    user =User(name=form.name.data,
    email=form.email.data,
    password=generate_password_hash(form.password.data),
    role=custormer_role
    )
    db.session.add(user)
    db.session.commit()
    flash("account create succesfuly")
    return redirect(url_for("auth.login"))
  return render_template("auth/register.html",form=form)
@auth.route("/login", methods =["GET","POST"])
def login():
  
  form = LoginForm()
  if form.validate_on_submit():
    
    user = User.query.filter_by(email=form.email.data).first()

    if user and check_password_hash(user.password,form.password.data):
      login_user(user)
      flash("login succesfuly")
      if user.role and user.role.name=="Admin":
        return redirect(url_for("admin.dashboard"))
      return redirect(url_for("shop.home"))
    else:
      flash("email and password is incorrect")
  return render_template("auth/login.html",form=form)
@auth.route("/logout")
def logout():
  logout_user()
  flash("logout succesfuly")
  return redirect("/")
  