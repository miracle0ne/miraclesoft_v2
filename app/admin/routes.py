from decimal import Decimal
from flask import render_template,flash,redirect,url_for
from flask_login import login_required

from app.models import Product,Order,User,AdminNotification,Commission
from . import admin
from .Decorator import admin_requred
from .form import ProductForm,StatusForm,PaymentStatus,DeleteForm 
from app.extension import db
from werkzeug.utils import secure_filename
from flask import current_app
import os
from slugify import slugify
from sqlalchemy import func
from . import reports

@admin.route("/products")
@login_required
@admin_requred
def products():
  
    delete_form = DeleteForm()
    products = Product.query.filter_by(active=True).order_by(
        Product.create_at.desc()
    ).all()

    return render_template(
        "admin/products/index.html",
        products=products,
        delete_form=delete_form
    )
@admin.route("/products/create", methods=["GET", "POST"])
@login_required
@admin_requred
def create_product():

    form = ProductForm()

    if form.validate_on_submit():
      base_slug =slugify(form.name.data)
      slug=base_slug
      count=1
      while Product.query.filter_by(slug=slug).first():
        slug =f"{base_slug}-{count}"
        count +=1
      
      filename =None
      if form.image.data:
        filename =secure_filename(form.image.data.filename)
        form.image.data.save(os.path.join(
          current_app.config["UPLOAD_FOLDER"],filename))

      product = Product(
          name=form.name.data,
          slug=slug,
          description=form.description.data,
          price=form.price.data,
          stock=form.stock.data,
          image =filename,
          active=form.active.data
        )

      db.session.add(product)
      db.session.commit()

      flash(
            "Product created successfully",
            "success"
        )
    

      return redirect(
            url_for("admin.products")
        )
    else:
      print(form.errors)
    return render_template(
        "admin/products/create.html",
        form=form
    )
@admin.route("/orders/<int:order_id>/status",methods=["POST"])
def update_order_status(order_id):
  order =Order.query.get_or_404(order_id)
  form =StatusForm()
  if form.validate_on_submit():
    order.status = form.status.data
    db.session.commit()
    flash(f"order # {{ order.id }} update_status successfully","success")
    return redirect(url_for("admin.orders"))
  else:
    flash("invalid order","denger")
  form.status.data =order.status
  return redirect("admin.orders")
@admin.route("/dashboard")
def dashboard():

    products_count = Product.query.filter_by(
    active=True).count()
    deleted_products = Product.query.filter_by(
    active=False
).count()

    orders_count = Order.query.count()

    users_count = User.query.count()

    pending_orders = Order.query.filter_by(
        status="pending"
    ).count()

    delivered_orders = Order.query.filter_by(
        status="delivered"
    ).count()

    total_sales = db.session.query(
        func.coalesce(func.sum(Order.total), 0)
    ).filter(
        Order.payment_status == "paid"
    ).scalar()

    recent_orders = Order.query.order_by(
        Order.created_at.desc()
    ).limit(5).all()

    return render_template(
        "admin/dashboard.html",
        products_count=products_count,
        deleted_products=deleted_products,
        orders_count=orders_count,
        users_count=users_count,
        pending_orders=pending_orders,
        delivered_orders=delivered_orders,
        total_sales=total_sales,
        recent_orders=recent_orders
    )
@admin.route("/orders")
@login_required
def orders():

  orders = Order.query.order_by(
        Order.created_at.desc()
    ).all()

  forms = {}
  paymentforms={}

  for order in orders:
    
    form = StatusForm()
    form.status.data = order.status
    forms[order.id] = form
    #updte PaymentStatus
    paymentform=PaymentStatus()
    paymentform.payment_status.data=order.payment_status
    paymentforms[order.id]=paymentform
  return render_template("admin/order.html",orders=orders
  ,forms=forms
  ,paymentforms=paymentforms
    )
@admin.route("/orders/<int:order_id>")
@login_required
def order_details(order_id):
  order = Order.query.get_or_404(order_id)

  form = StatusForm()

  form.status.data = order.status
  payment_form = PaymentStatus()
  payment_form.payment_status.data = order.payment_status


  return render_template(
        "admin/order_details.html",
        order=order,
        form=form,
        payment_form=payment_form
    )

@admin.route("/orders/<int:order_id>/payment-status", methods=["POST"])
@login_required
def update_payment_status(order_id):
  order = Order.query.get_or_404(order_id)

  form = PaymentStatus()

  if form.validate_on_submit():

    print("PAYMENT DEBUG:", order.id, "OLD:", order.payment_status, "NEW:", form.payment_status.data)

    old_status = order.payment_status
    new_status = form.payment_status.data

    order.payment_status = new_status

    # ==========================================
    # MIRACLESOFT 5% COMMISSION
    # ==========================================

    if new_status == "paid" and old_status != "paid":

      existing_commission = Commission.query.filter_by(
        order_id=order.id
      ).first()

      if not existing_commission:

        commission_amount = order.total * Decimal("0.05")

        commission = Commission(
          order_id=order.id,
          sale_amount=order.total,
          commission_rate=5.00,
          commission_amount=commission_amount
        )

        db.session.add(commission)

    db.session.commit()

    flash(
      f"Order #{order.id} payment status updated successfully",
      "success"
    )

  else:

    print("payment_erros", form.errors)

    flash(
      f"Invalid payment status: {form.errors}",
      "danger"
    )

  return redirect(url_for("admin.orders"))

@admin.route("/notifications")
@login_required
def notifications():

  notifications = AdminNotification.query.order_by(
    AdminNotification.created_at.desc()
  ).all()

  return render_template(
    "admin/notifications.html",
    notifications=notifications
  )

@admin.route("/notifications/<int:notification_id>/read")
@login_required
def mark_notification_read(notification_id):

  notification = AdminNotification.query.get_or_404(
    notification_id
  )

  notification.is_read = True

  db.session.commit()

  if notification.notification_type == "order":
    return redirect(url_for("admin.orders"))

  return redirect(url_for("admin.notifications"))

@admin.route("/notifications/unread")
@login_required
def unread_notifications_api():

  notifications = AdminNotification.query.filter_by(
    is_read=False
  ).order_by(
    AdminNotification.created_at.desc()
  ).all()

  return {
    "count": len(notifications),
    "notifications": [
      {
        "id": n.id,
        "title": n.title,
        "message": n.message,
        "type": n.notification_type
      }
      for n in notifications
    ]
  }
