from flask import Flask,render_template
from .config import Config
from app.models.User import User
from .extension import (
  db,
  migrate,
  login_manager)
from flask_wtf.csrf import CSRFProtect
csrf=CSRFProtect()
login_manager.login_view ="auth.login"
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))
def create_app():
  app=Flask(__name__)
  app.config.from_object(Config)
  print("secret",app.config.get("SECRET_KEY"))
  db.init_app(app)
  migrate.init_app(app,
  db)
  csrf.init_app(app)
  login_manager.init_app(app)
  from .import models
  from .auth import auth
  from app.shop import shop
  app.register_blueprint(shop)
  
  app.register_blueprint(auth)
  from app.cart import cart
  app.register_blueprint(cart)
  from app.admin import admin
  app.register_blueprint(admin)
  @app.route("/")
  def home():
    return render_template("base.html")
    
  return app