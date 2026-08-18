from datetime import datetime
from app.extension import db

class Cart(db.Model):
  __tablename__="cart"
  id = db.Column(db.Integer,primary_key=True)
  product_id =db.Column(db.Integer,db.ForeignKey("products.id"),
  nullable=False)
  user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
  quantity =db.Column(db.Integer,nullable=False,default=1)
  create_at = db.Column(db.DateTime,default=datetime.utcnow)
  user =db.relationship("User",back_populates="cart_item")
  product =db.relationship("Product",
  back_populates="cart_item")
  def total_price(self):
    return self.product.price * self.quantity