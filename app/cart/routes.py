from flask import (
    render_template,
    redirect,
    url_for,
    request,
    flash
)

from flask_login import current_user, login_required

from app.extension import db
from app.models import Cart, Product

from . import cart


@cart.route("/cart")
@login_required
def view_cart():

    items = Cart.query.filter_by(
        user_id=current_user.id
    ).all()

    total = sum(
        item.total_price()
        for item in items
    )

    return render_template(
        "cart/cart.html",
        items=items,
        total=total
    )


@cart.route("/cart/add/<int:product_id>", methods=["POST","GET"])
@login_required
def add_to_cart(product_id):

  product = Product.query.get_or_404(product_id)

  item = Cart.query.filter_by(
      user_id=current_user.id,
      product_id=product.id
    ).first()


  quantity = int(
      request.form.get("quantity", 1)
    )


  if item:

      item.quantity += quantity

  else:

      item = Cart(
          user_id=current_user.id,
          product_id=product.id,
          quantity=quantity
        )

      db.session.add(item)
      db.session.commit()
      flash(
        "Product added to cart",
        "success"
    )
  return redirect(
        url_for("cart.view_cart")
    )



@cart.route("/cart/remove/<int:id>")
@login_required
def remove_from_cart(id):

    item = Cart.query.get_or_404(id)


    if item.user_id != current_user.id:

        return redirect(
            url_for("cart.view_cart")
        )


    db.session.delete(item)

    db.session.commit()


    flash(
        "Product removed",
        "success"
    )


    return redirect(
        url_for("cart.view_cart")
    )
@cart.route("/cart/increase/<int:id>")
@login_required
def increase_q(id):
  item = Cart.query.get_or_404(id)
  if item.user_id  != current_user.id:
    flash("unautholize action","danger")
    return redirect(url_for("cart.view_cart"))
  if item.quantity >= item.product.stock:
    flash("maximum sock reached","warning")
    return redirect(url_for("cart.view_cart"))
  item.quantity += 1
  db.session.commit()
  return redirect(url_for("cart.view_cart"))
@cart.route("/cart/decrease/<int:id>")
def decrease_q(id):
  item =Cart.query.get_or_404(id)
  if item.user_id != current_user.id:
    flash("unautholize action","denger")
    return redirect(url_for("cart.view_cart"))
  if item.quantity >1:
    item.quantity -= 1
  else:
    db.session.delete(item)
  db.session.commit()
  return redirect(url_for("cart.view_cart"))
  