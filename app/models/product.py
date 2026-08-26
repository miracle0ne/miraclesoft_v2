from datetime import datetime
from app.extension import db

class Product(db.Model):
  __tablename__="products"
  id =db.Column(db.Integer,primary_key=True,nullable=False)
  name =db.Column(db.String(100),nullable=True)
  slug =db.Column(db.String(200),unique=True,nullable=False)
  description = db.Column(db.Text)
  price =db.Column(db.Numeric(10,2),nullable=False)
  image=db.Column(db.String(255),nullable=True,default="default.png")
  stock =db.Column(db.Integer,default=0)
  active =db.Column(db.Boolean)
  create_at =db.Column(db.DateTime,default=datetime.utcnow())
  cart_item=db.relationship("Cart",back_populates="product")
  specifications = db.relationship("ProductSpecification", back_populates="product", cascade="all, delete-orphan")
  def ___repr__(self):
    return f"<Product {{self.name}}>"
  
  