from flask import Blueprint, redirect, url_for, flash
from flask_login import current_user, login_required

admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


@admin.before_request
def admin_required():
  if not current_user.is_authenticated:
    return redirect(
        url_for("auth.login")
        )

  if not current_user.role:
    flash(
            "Access denied.",
            "danger"
        )
    return redirect(
        url_for("shop.home")
        )

  if current_user.role.name.lower() != "admin":
    flash(
            "You do not have permission to access the admin area.",
            "danger"
    )
    return redirect(
            url_for("shop.home")
    )


from . import routes
from . import product_r