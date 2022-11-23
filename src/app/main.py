"""Flask app for displaying frontend and adding new entries

SHORTCUTS:
    - Should have set up gunicorn to make this production app
    - Would like to add jsonschema validation of post request
      to handle validation (ints, required fields, etc).
"""
import logging

from sqlalchemy.sql import func
from flask import (
    Flask, render_template, url_for, request, Response
)

from model.items import Items
from db_utils import init_db, session_scope


app = Flask(__name__)
app.logger.setLevel(logging.INFO)


@app.route("/")
@app.route("/home", methods=["GET"])
def home():
    """ Landing page displaying all current items in the database."""
    with session_scope() as ss:
        records = ss.query(Items).all()

        data = [
            {"item": record.item_name, "price": record.price}
            for record in records
        ]

    app.logger.info(f"Displaying data from database: {data}")

    return render_template("landing.html", data=data)


@app.route("/summary", methods=["GET"])
def summary():
    """ Page displaying the total sum of items in the database."""
    with session_scope() as ss:
        total = ss.query(func.sum(Items.price)).one()[0]

    total = total or 0
    app.logger.info(f"Total sum of all items: {total}")

    return render_template("summary.html", total=total)


@app.route("/add", methods=["POST"])
def add():
    """ Create a new item and store it in the database."""
    request_json = request.get_json()
    app.logger.info(f"Incoming request: {request_json}")

    item_name = request_json.get("item").lower()
    price = request_json.get("price")

    if (item_name is None) or (price is None):
        return Response(
            "We can't add an item without both 'item' and 'price' attributes.",
            status=400
        )

    with session_scope() as session:
        existing_items = session.query(Items).filter(
            Items.item_name == item_name
        ).all()

        if len(existing_items) > 0:
            app.logger.exception(
                f"Item ({item_name}) already exists in the database."
            )
            return Response(
                f"Item ({item_name}) already exists in the database.",
                status=400
            )

        try:
            session.add(
                Items(
                    item_name=item_name,
                    price=price
                )
            )
            session.commit()
        except Exception as e:
            session.rollback()
            app.logger.exception(
                f"An exception occured when adding items to the database: {e}")
            return Response(
                f"An exception occured when adding items to the database: {e}",
                status=400
            )

    app.logger.info(f"The items were successfully added.")

    return Response(
        "New item: () created succeddfully",
        status=201
    )


if __name__ == "__main__":
    # Initialise / rebuilding SQLite database
    # Optional: wouldn't need if using hosted db
    init_db()
    app.run(port=5000)
