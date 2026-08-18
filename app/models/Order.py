from datetime import datetime
from app.extension import db

class Order(db.Model):
  __tablename__="orders"
  id =db.Column(db.Integer,primary_key=True)
  user_id =db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
  full_name =db.Column(db.String(255),nullable=False)
  address=db.Column(db.String(50),nullable=False)
  phone=db.Column(db.String(20),nullable=False)
  
  total =db.Column(db.Numeric(10,2),nullable=False)
  status =db.Column(db.String(20),default="pending")
  payment_status=db.Column(db.String(50),
  nullable=False,
  default="unpaid")
  created_at =db.Column(db.DateTime,default=datetime.utcnow)
  user =db.relationship("User",back_populates="orders")
  items =db.relationship("OrderItem",back_populates="order",cascade="all,delete-orphan")
  def __repr__(self):
    return f"<Order {self.id}>"