from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
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

class ReviewForm(FlaskForm):

    rating = SelectField(
        "Rating",
        choices=[
            ("5", "★★★★★ - Excellent"),
            ("4", "★★★★☆ - Very Good"),
            ("3", "★★★☆☆ - Good"),
            ("2", "★★☆☆☆ - Fair"),
            ("1", "★☆☆☆☆ - Poor")
        ],
        validators=[
            DataRequired()
        ]
    )

    comment = TextAreaField(
        "Comment",
        validators=[
            DataRequired(),
            Length(min=3, max=1000)
        ]
    )

    submit = SubmitField("Submit Review")
