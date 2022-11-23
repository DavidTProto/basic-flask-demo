"""
Testing for main.py

Shortcut:
    - Only testing add in main.py, this is more of a demo of
    testing which would be usually done throughout for each .py file
    
"""

import pytest

from app.main import app
from app.db_utils import init_db, session_scope
from app.model.items import Items

init_db()

class TestAddEndpoint:
    """ Collection for functionality of ADD endpoint"""

    URL = '/add'

    @pytest.fixture(scope="function", autouse=True)
    def setup_db(self):
        """ Makes blank DB for each unit test"""
        init_db()

    def test_add_simple(self):
        """ Check we can add items to the database"""
        with session_scope() as session:
            # Adds a new element to the database via POST request
            app.test_client().post(
                TestAddEndpoint.URL,
                json={
                    'item': 'Apples', 
                    'price': 1
                }
            )

            # Checking element was added
            items = session.query(Items).all()
            assert len(items) == 1
            assert items[0].item_name == "apples"
            assert items[0].price == 1

            # Adding a second element to the database
            app.test_client().post(
                TestAddEndpoint.URL,
                json={
                    'item': 'Banana', 
                    'price': 5
                }
            )

            # Checking element was added
            updated_items = session.query(Items).all()
            assert len(updated_items) == 2
            assert updated_items[1].item_name == "banana"
            assert updated_items[1].price == 5

    def test_add_missing_data(self):
        """ Check we raise an exception if we don't have a valid payload"""
        with session_scope() as session:
            # Send request with missing item name
            response = app.test_client().post(
                TestAddEndpoint.URL,
                json={
                    #'item': 'Apples', 
                    'price': 1
                }
            )

            assert response.status_code == 400
            assert response.text == "We can't add an item without both 'item' and 'price' attributes."

            # Send request with missing price
            response = app.test_client().post(
                TestAddEndpoint.URL,
                json={
                    'item': 'Apples', 
                    #'price': 1
                }
            )

            assert response.status_code == 400
            assert response.text == "We can't add an item without both 'item' and 'price' attributes."

            # Send request with empty item_name
            response = app.test_client().post(
                TestAddEndpoint.URL,
                json={
                    'item': '', 
                    'price': 1
                }
            )

            assert response.status_code == 400
            assert response.text == "We can't add an item without both 'item' and 'price' attributes."

            # Send request with empty price
            response = app.test_client().post(
                TestAddEndpoint.URL,
                json={
                    'item': 'Apples', 
                    'price': ''
                }
            )

            assert response.status_code == 400
            assert response.text == "We can't add an item without both 'item' and 'price' attributes."

            # Send request with empty payload
            response = app.test_client().post(
                TestAddEndpoint.URL,
                json={}
            )

            assert response.status_code == 400
            assert response.text == "We can't add an item without both 'item' and 'price' attributes."

    def test_add_duplicate_data(self):
        """ Check we raise an error if duplicate data has been sent."""
        with session_scope() as session:
            # Adds a new element to the database via POST request
            app.test_client().post(
                TestAddEndpoint.URL,
                json={
                    'item': 'Apples', 
                    'price': 1
                }
            )

            # Checking element was added
            items = session.query(Items).all()
            assert len(items) == 1
            assert items[0].item_name == "apples"
            assert items[0].price == 1 

            # Adds the new element again
            response = app.test_client().post(
                TestAddEndpoint.URL,
                json={
                    'item': 'Apples', 
                    'price': 1
                }
            )

            assert response.status_code == 400
            assert response.text == "Item (apples) already exists in the database."

            # Checking number of elements haven't changed
            items = session.query(Items).all()
            assert len(items) == 1

    def test_add_payload_types(self):
        # SHORTCUT: Placeholder test for failing request if price wasn't an integer
        #           This would be implemented as part of json_schema
        pass