from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class CheckoutF(FlaskForm):

    full_name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(min=3, max=255)
        ]
    )

    phone = StringField(
        "Phone",
        validators=[
            DataRequired(),
            Length(min=10, max=20)
        ]
    )

    address = TextAreaField(
        "Address",
        validators=[
            DataRequired(),
            Length(min=3, max=255)
        ]
    )

    submit = SubmitField("Place Order")