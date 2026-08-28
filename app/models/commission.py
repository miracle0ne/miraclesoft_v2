from datetime import datetime
from app.extension import db


class Commission(db.Model):
    __tablename__ = "commissions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id"),
        nullable=False,
        unique=True
    )

    sale_amount = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    commission_rate = db.Column(
        db.Numeric(5, 2),
        nullable=False,
        default=5.00
    )

    commission_amount = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    order = db.relationship(
        "Order",
        backref=db.backref(
            "commission",
            uselist=False
        )
    )
