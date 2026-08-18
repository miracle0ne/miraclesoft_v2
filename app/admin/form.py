from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    DecimalField,
    IntegerField,
    BooleanField,
    SubmitField,
    SelectField
  
)
from flask_wtf.file import FileField, FileAllowed

from wtforms.validators import DataRequired


class ProductForm(FlaskForm):

    name = StringField(
        "Product Name",
        validators=[DataRequired()]
    )

    

    description = TextAreaField(
        "Description"
    )

    price = DecimalField(
        "Price",
        validators=[DataRequired()]
    )

    stock = IntegerField(
        "Stock",
        validators=[DataRequired()]
    )

    active = BooleanField(
        "Active",
        default=True
    )
    image =FileField(
      "product_image",validators=[
        FileAllowed(["jpg","jpeg","png"],"image only")])

    submit = SubmitField(
        "Save Product"
    )
class StatusForm(FlaskForm):
  status =SelectField(
    "order_status",
    choices=[
      ("pending","pending"),
      ("processing","processing"),
      ("shipping","shipping"),
      ("delivered","delivered"),
      ("canceled","canceled")
      ],
      validators=[DataRequired()]
      )
  submit =SubmitField("status_update")
  
class PaymentStatus(FlaskForm):

  payment_status = SelectField(
      "Payment Status",
      choices=[
          ("unpaid", "Unpaid"),
          ("pending", "Pending"),
          ("paid", "Paid"),
          ("failed", "Failed"),
        ],
      validators=[DataRequired()]
    )

  submit = SubmitField("Update Payment")

class DeleteForm(FlaskForm):
  pass
  
  