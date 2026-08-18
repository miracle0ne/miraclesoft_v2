from app.extension import db

class OrderItem(db.Model):
  id =db.Column(db.Integer,primary_key=True)
  order_id =db.Column(db.Integer,db.ForeignKey("orders.id"),nullable=False)
  product_id =db.Column(db.Integer,db.ForeignKey("products.id"),nullable=False)
  price=db.Column(db.Float, nullable=False)
  quantity =db.Column(db.Integer,nullable=False
  )
  order =db.relationship("Order",back_populates="items")
  product=db.relationship("Product")
  def subtotal(self):
    return self.price * self.quantity
  def __repr__(self):
    return f"<OrderItem :{self.id}>"