from app.extension import db

class Role(db.Model):
  ___tablename__ ="roles"
  id =db.Column(db.Integer,primary_key=True)
  name =db.Column(db.String(200),nullable=False,unique=True)
  user =db.relationship("User", back_populates="role")
  