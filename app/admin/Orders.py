from flask import render_template
from flask_login import login_required

from app.models import Order
from app.forms.order import OrderStatusForm

@admin.route("/orders")
@login_required
def orders():

    orders = Order.query.order_by(
        Order.created_at.desc()
    ).all()

    forms = {}

    for order in orders:
        form = OrderStatusForm()
        form.status.data = order.status
        forms[order.id] = form

    return render_template(
        "admin/orders.html",
        orders=orders,
        forms=forms
    )