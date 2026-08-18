from datetime import datetime, timedelta
import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from flask import render_template, current_app
from flask_login import login_required

from app.extension import db
from app.models import Order

from . import admin
from .Decorator import admin_requred


def create_weekly_sales_chart():

    now = datetime.now()

    today = datetime(
        now.year,
        now.month,
        now.day
    )

    week_start = today - timedelta(
        days=today.weekday()
    )

    labels = []
    sales = []

    for i in range(7):

        day_start = week_start + timedelta(days=i)
        day_end = day_start + timedelta(days=1)

        total = db.session.query(
            db.func.coalesce(
                db.func.sum(Order.total),
                0
            )
        ).filter(
            Order.payment_status == "paid",
            Order.created_at >= day_start,
            Order.created_at < day_end
        ).scalar()

        labels.append(
            day_start.strftime("%a")
        )

        sales.append(
            float(total or 0)
        )


    # Create chart

    plt.figure(figsize=(10, 4.5))

    plt.plot(
        labels,
        sales,
        marker="o",
        linewidth=2
    )

    plt.title(
        "Weekly Sales"
    )

    plt.xlabel(
        "Day"
    )

    plt.ylabel(
        "Sales (TSh)"
    )

    plt.grid(
        True,
        alpha=0.25
    )

    plt.tight_layout()


    # Save chart

    chart_folder = os.path.join(
        current_app.static_folder,
        "reports"
    )

    os.makedirs(
        chart_folder,
        exist_ok=True
    )

    chart_path = os.path.join(
        chart_folder,
        "weekly_sales.png"
    )

    plt.savefig(
        chart_path,
        dpi=120
    )

    plt.close()

    return "reports/weekly_sales.png"


@admin.route("/reports")
@login_required
@admin_requred
def reports():

    now = datetime.now()

    today_start = datetime(
        now.year,
        now.month,
        now.day
    )

    tomorrow_start = today_start + timedelta(
        days=1
    )


    # TODAY

    today_sales = db.session.query(
        db.func.coalesce(
            db.func.sum(Order.total),
            0
        )
    ).filter(
        Order.payment_status == "paid",
        Order.created_at >= today_start,
        Order.created_at < tomorrow_start
    ).scalar()


    # WEEK

    week_start = today_start - timedelta(
        days=today_start.weekday()
    )

    week_sales = db.session.query(
        db.func.coalesce(
            db.func.sum(Order.total),
            0
        )
    ).filter(
        Order.payment_status == "paid",
        Order.created_at >= week_start,
        Order.created_at < tomorrow_start
    ).scalar()


    # MONTH

    month_start = datetime(
        now.year,
        now.month,
        1
    )

    month_sales = db.session.query(
        db.func.coalesce(
            db.func.sum(Order.total),
            0
        )
    ).filter(
        Order.payment_status == "paid",
        Order.created_at >= month_start,
        Order.created_at < tomorrow_start
    ).scalar()


    # YEAR

    year_start = datetime(
        now.year,
        1,
        1
    )

    year_sales = db.session.query(
        db.func.coalesce(
            db.func.sum(Order.total),
            0
        )
    ).filter(
        Order.payment_status == "paid",
        Order.created_at >= year_start,
        Order.created_at < tomorrow_start
    ).scalar()


    # ORDERS

    paid_orders = Order.query.filter_by(
        payment_status="paid"
    ).count()

    unpaid_orders = Order.query.filter_by(
        payment_status="unpaid"
    ).count()


    # CREATE CHART

    weekly_chart = create_weekly_sales_chart()


    return render_template(
        "admin/reports.html",

        today_sales=today_sales,

        week_sales=week_sales,

        month_sales=month_sales,

        year_sales=year_sales,

        paid_orders=paid_orders,

        unpaid_orders=unpaid_orders,

        weekly_chart=weekly_chart
    )