from datetime import datetime
from app.extension import db
from flask_login import UserMixin
class User(db.Model, UserMixin):
  __tablename__="users"
  id =db.Column(db.Integer,primary_key=True)
  name=db.Column(db.String(100),nullable=False)
  email =db.Column(db.String(100),unique=True,nullable=False)
  password =db.Column(db.String(255),nullable=False)
  role_id =db.Column(db.Integer,
  db.ForeignKey("role.id")
  )
  active =db.Column(db.Boolean,default=True)
  email_verified = db.Column(
    db.Boolean,
    default=False,
    nullable=False
  )

  email_verification_token = db.Column(
    db.String(255),
    nullable=True,
    unique=True
  )
  password_reset_token = db.Column(
    db.String(255),
    nullable=True,
    unique=True
)
  create_at =db.Column(db.DateTime,default=datetime.utcnow)
  role =db.relationship("Role",
  back_populates="user")
  cart_item = db.relationship(
    "Cart",
    back_populates="user",
    cascade="all, delete-orphan")
  orders= db.relationship("Order", back_populates="user")
