from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    current_app,request
)

from flask_login import login_required

from werkzeug.utils import secure_filename

import os

from slugify import slugify

from app.extension import db
from app.models import Product, ProductSpecification
from . import admin
from . form import ProductForm,DeleteForm


@admin.route(
    "/products/edit/<int:product_id>",
    methods=["GET", "POST"]
)
@login_required
def edit_product(product_id):

  product = Product.query.get_or_404(product_id)

  form = ProductForm()
  if request.method == "GET":
    form.name.data = product.name
    form.description.data = product.description
    form.price.data = product.price
    form.stock.data = product.stock
    form.active.data = product.active

    for spec in product.specifications:
      form.specifications.append_entry({
        "name": spec.name,
        "value": spec.value
      })


  if form.validate_on_submit():

    product.name = form.name.data
    product.description = form.description.data
    product.price = form.price.data
    product.stock = form.stock.data
    product.active = form.active.data

    # Update product specifications
    existing_specs = {spec.id: spec for spec in product.specifications}
    submitted_ids = set()

    for spec_form in form.specifications.entries:
        spec_id = spec_form.form.id.data
        name = spec_form.form.name.data.strip()
        value = spec_form.form.value.data.strip()

        if not name or not value:
            continue

        if spec_id:
            spec_id = int(spec_id)
            spec = existing_specs.get(spec_id)

            if spec:
                spec.name = name
                spec.value = value
                submitted_ids.add(spec_id)
        else:
            product.specifications.append(
                ProductSpecification(
                    name=name,
                    value=value
                )
            )

    for spec_id, spec in existing_specs.items():
        if spec_id not in submitted_ids:
            db.session.delete(spec)

    # Update image only if a new image is selected
    if form.image.data:

      filename = secure_filename(
                form.image.data.filename
            )

      if filename:

        upload_folder = current_app.config["UPLOAD_FOLDER"]

        os.makedirs(
            upload_folder,
            exist_ok=True
          )

        form.image.data.save(
           os.path.join(
           upload_folder,filename
            )
        )

        product.image = filename

        # Update slug
    base_slug = slugify(form.name.data)

    slug = base_slug
    count = 1

    while Product.query.filter(Product.slug == slug,Product.id != product.id
        ).first():

      slug = f"{base_slug}-{count}"
      count += 1

    product.slug = slug

    db.session.commit()

    flash(
      "Product updated successfully.","success"
        )

    return redirect(
      url_for("admin.products")
    )

  return render_template("admin/products/edit.html",
    form=form,
    product=product
  )


@admin.route(
    "/products/delete/<int:product_id>",
    methods=["POST"]
)
@login_required
def delete_product(product_id):

  product = Product.query.get_or_404(product_id)

  product.active=False

  db.session.commit()

  flash(
    "Product deleted successfully.",
    "success"
    )

  return redirect(
    url_for("admin.products")
  )
@admin.route(
    "/products/restore/<int:product_id>",
    methods=["POST"]
)
@login_required
def restore_product(product_id):

    product = Product.query.get_or_404(product_id)

    product.active = True

    db.session.commit()

    flash(
        "Product restored successfully.",
        "success"
    )

    return redirect(
        url_for("admin.deleted_products")
    )
@admin.route("/products/deleted")
@login_required
def deleted_products():

    products = Product.query.filter_by(
        active=False
    ).order_by(
        Product.create_at.desc()
    ).all()

    return render_template(
        "admin/products/deleted.html",
        products=products
    )