from importlib.util import spec_from_file_location
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    DecimalField,
    IntegerField,
    BooleanField,
    SubmitField,
    SelectField,
    FieldList,
    FormField,
    HiddenField
    
  
)
from flask_wtf.file import FileField, FileAllowed

from wtforms.validators import DataRequired

class SpecificationForm(FlaskForm):

    id = HiddenField()

    name = StringField(
        "Specification Name"
    )

    value = StringField(
        "Specification Value"
    ) 

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
    specifications=FieldList(
      FormField(SpecificationForm),
      min_entries=0
    )

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

