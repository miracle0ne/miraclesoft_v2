from flask import Flask,abort,render_template,request,flash,redirect,url_for, Response
from flask_login import login_required,current_user
from sqlalchemy import or_
from . import shop
from app.extension import db
from app.models import AdminNotification, Product,Cart,Order,OrderItem,Review
from .form import CheckoutF,ReviewForm

@shop.route("/")
def home():
  q = request.args.get("q", "").strip()

  query = Product.query.filter_by(active=True)

  if q:
    query = query.filter(
      or_(
        Product.name.ilike(f"%{q}%"),
        Product.description.ilike(f"%{q}%")
      )
    )

  products = (
    query
    .order_by(Product.create_at.desc())
    .limit(8)
    .all()
  )

  return render_template(
    "shop/index.html",
    products=products,
    search_query=q
  )

@shop.route("/product/<slug>")
def product_detail(slug):

  product = Product.query.filter_by(
    slug=slug,
    active=True
  ).first()

  if not product:
    abort(404)

  reviews = Review.query.filter_by(
    product_id=product.id
  ).order_by(
    Review.created_at.desc()
  ).all()

  review_form = ReviewForm()

  # ==========================================
  # REVIEW ELIGIBILITY
  # ==========================================

  can_review = False
  already_reviewed = False
  review_message = None

  if current_user.is_authenticated:

    # Check if customer already reviewed
    existing_review = Review.query.filter_by(
      user_id=current_user.id,
      product_id=product.id
    ).first()

    if existing_review:

      already_reviewed = True
      review_message = "You have already reviewed this product."

    else:

      # Check if customer bought the product
      purchased_order = (
        Order.query
        .join(OrderItem, Order.id == OrderItem.order_id)
        .filter(
          Order.user_id == current_user.id,
          OrderItem.product_id == product.id
        )
        .order_by(Order.created_at.desc())
        .first()
      )

      if purchased_order:

        if purchased_order.status == "delivered":

          can_review = True

        else:

          review_message = (
            "You can review this product after your order has been delivered."
          )

      else:

        review_message = (
          "You can review this product after purchasing it."
        )

  return render_template(
    "shop/product_detail.html",
    product=product,
    reviews=reviews,
    review_form=review_form,
    can_review=can_review,
    already_reviewed=already_reviewed,
    review_message=review_message
  )


@shop.route("/product/<slug>/review", methods=["POST"])
@login_required
def add_review(slug):

  product = Product.query.filter_by(
    slug=slug,
    active=True
  ).first_or_404()

  form = ReviewForm()

  if not form.validate_on_submit():
    flash(
      "Please check your review and try again.",
      "danger"
    )

    return redirect(
      url_for(
        "shop.product_detail",
        slug=product.slug
      )
    )

  # ==========================================
  # CHECK IF CUSTOMER RECEIVED THIS PRODUCT
  # ==========================================

  purchased = (
    Order.query
    .join(OrderItem, Order.id == OrderItem.order_id)
    .filter(
      Order.user_id == current_user.id,
      Order.status == "delivered",
      OrderItem.product_id == product.id
    )
    .first()
  )

  if not purchased:

    flash(
      "You can review this product only after your order has been delivered.",
      "warning"
    )

    return redirect(
      url_for(
        "shop.product_detail",
        slug=product.slug
      )
    )

  # ==========================================
  # PREVENT DUPLICATE REVIEW
  # ==========================================

  existing_review = Review.query.filter_by(
    user_id=current_user.id,
    product_id=product.id
  ).first()

  if existing_review:

    flash(
      "You have already reviewed this product.",
      "info"
    )

    return redirect(
      url_for(
        "shop.product_detail",
        slug=product.slug
      )
    )

  # ==========================================
  # CREATE REVIEW
  # ==========================================

  review = Review(
    user_id=current_user.id,
    product_id=product.id,
    rating=int(form.rating.data),
    comment=form.comment.data.strip()
  )

  db.session.add(review)
  db.session.commit()

  flash(
    "Your review has been added successfully.",
    "success"
  )

  return redirect(
    url_for(
      "shop.product_detail",
      slug=product.slug
    )
  )


@shop.route("/checkout", methods=["GET","POST"])
@login_required
def checkout():
  form=CheckoutF()
  items =Cart.query.filter_by(user_id=current_user.id).all()
  if not items:
    flash("you cart is empty","danger")
    return redirect(url_for("cart.view_cart"))
  total = sum(
        item.product.price * item.quantity
        for item in items
    )
  if form.validate_on_submit():
    order =Order(user_id=current_user.id,
    full_name=form.full_name.data.strip(),
    phone=form.phone.data.strip(),
    address=form.address.data.strip(),
    total=total,
    status="pending")
    db.session.add(order)
    db.session.flush()

    # ==========================================
    # ADMIN NOTIFICATION - NEW ORDER
    # ==========================================

    notification = AdminNotification(
        title="New Order",
        message=f"Order #{order.id} has been placed by {current_user.name}.",
        notification_type="order"
    )

    db.session.add(notification)
    for item in items:
      order_item=OrderItem(order_id=order.id,product_id =item.product.id,
      price=item.product.price,
      quantity=item.quantity)
      db.session.add(order_item)
    for item in items:
      db.session.delete(item)
    db.session.commit()
    flash("order placed succesfuly","success")
    return redirect(url_for("shop.confirm_order",
    order_id=order.id))
  
  return render_template("shop/checkout.html",form=form,
  items=items,
  total=total)
@shop.route("/order/<int:order_id>/confirmation")
@login_required
def confirm_order(order_id):
  order = Order.query.filter_by(
        id=order_id,
        user_id=current_user.id
    ).first_or_404()

  return render_template(
        "shop/Confirm_order.html",
        order=order
    )
@shop.route("/orders")
@login_required
def my_order():
  print("currente id",current_user.id)
  orders=Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
  return render_template("shop/my_order.html" , orders=orders)
@shop.route("/orders/<int:order_id>")
@login_required
def order_details(order_id):

    order = Order.query.filter_by(
        id=order_id,
        user_id=current_user.id
    ).first_or_404()

    return render_template(
        "shop/order_details.html",
        order=order
    )
@shop.route("/sitemap.xml")
def sitemap():

    products = Product.query.filter_by(active=True).all()

    pages = []

    # Homepage
    pages.append({
        "loc": url_for("shop.home", _external=True),
        "priority": "1.0"
    })

    # Products
    for product in products:

        pages.append({
            "loc": url_for(
                "shop.product_detail",
                slug=product.slug,
                _external=True
            ),
            "priority": "0.8"
        })

    sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

    for page in pages:

        sitemap_xml += f"""
    <url>
        <loc>{page["loc"]}</loc>
        <priority>{page["priority"]}</priority>
    </url>
"""

    sitemap_xml += """
</urlset>
"""

    return Response(
        sitemap_xml,
        mimetype="application/xml"
    )