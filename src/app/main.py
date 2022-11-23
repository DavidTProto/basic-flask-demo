"""Flask app for displaying frontend and adding new entries

SHORTCUTS:
    - Should have set up gunicorn to make this production app
    - Would like to add jsonschema validation of post request
      to handle validation (ints, required fields, etc).
    - Running app across all addresses.
"""
import logging

from sqlalchemy.sql import func
from flask import (
    Flask, render_template, url_for, request, Response
)

from app.model.items import Items
from app.db_utils import init_db, session_scope


app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)


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

    app.logger.debug(f"Displaying data from database: {data}")

    return render_template("landing.html", data=data)


@app.route("/summary", methods=["GET"])
def summary():
    """ Page displaying the total sum of items in the database."""
    with session_scope() as ss:
        total = ss.query(func.sum(Items.price)).one()[0]

    total = total or 0
    app.logger.debug(f"Total sum of all items: {total}")

    return render_template("summary.html", total=total)


@app.route("/add", methods=["POST"])
def add():
    """ Create a new item and store it in the database."""
    request_json = request.get_json()
    app.logger.debug(f"Incoming request: {request_json}")

    item_name = request_json.get("item")
    price = request_json.get("price")

    # Check for presence would usually be in jsonschema checking
    # SHORTCUT: price being an integer would be a JSONSchema item, so aware this would
    # fail of price = 0 (in production wouldn't be an issue)
    if (not item_name) or (not price ):
        app.logger.debug(
                "We can't add an item without both 'item' and 'price' attributes."
            )
        return Response(
            "We can't add an item without both 'item' and 'price' attributes.",
            status=400
        )

    with session_scope() as session:
        # Making item_name case insensitive to check for duplication
        item_name = item_name.lower()

        existing_items = session.query(Items).filter(
            Items.item_name == item_name
        ).all()

        if len(existing_items) > 0:
            app.logger.debug(
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
            app.logger.debug(
                f"An exception occured when adding items to the database: {e}")
            return Response(
                f"An exception occured when adding items to the database: {e}",
                status=400
            )

    app.logger.debug(f"The items were successfully added.")

    return Response(
        "New item: () created succeddfully",
        status=201
    )


if __name__ == "__main__":
    # Initialise / rebuilding SQLite database
    # Optional: wouldn't need if using hosted db
    init_db()

    # Note: Running across all addresses. Wouldn't do this for production app.
    app.run(host="0.0.0.0", port=5000)
