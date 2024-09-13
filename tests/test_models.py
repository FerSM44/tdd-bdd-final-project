# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Product Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_models.py:TestProductModel

"""
import os
import logging
import unittest
from decimal import Decimal
from service.models import Product, Category, db
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        self.assertEqual(str(product), "<Product Fedora id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Fedora")
        self.assertEqual(product.description, "A red hat")
        self.assertEqual(product.available, True)
        self.assertEqual(product.price, 12.50)
        self.assertEqual(product.category, Category.CLOTHS)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = ProductFactory()
        product.id = None
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)
        # Check that it matches the original product
        new_product = products[0]
        self.assertEqual(new_product.name, product.name)
        self.assertEqual(new_product.description, product.description)
        self.assertEqual(Decimal(new_product.price), product.price)
        self.assertEqual(new_product.available, product.available)
        self.assertEqual(new_product.category, product.category)

    #
    # ADD YOUR TEST CASES HERE
    #
    
    def test_read_product(self):
        #Create a Product object using the ProductFactory
        product = ProductFactory()
        #Add a log message displaying the product for debugging errors
        logger.info(f"Created {product}")
        #Set the ID of the product object to None and then create the product
        product.id = None
        product.create()
        #Assert that the product ID is not None
        self.assertIsNotNone(product.id)
        #Fetch the product back from the database
        fproduct = Product.find(product.id)
        #Assert the properties of the found product are correct
        self.assertEqual(fproduct.name, product.name)
        self.assertEqual(fproduct.description, product.description)
        self.assertEqual(fproduct.id, product.id)
        self.assertEqual(Decimal(fproduct.price), product.price)
        
    def test_update_product(self):
        #Create a Product object using the ProductFactory and save it to the database
        product = ProductFactory()
        product.create()
        #Assert that after creating a product and saving it to the database, there is only one product in the system
        self.assertEqual(len(Product.all()), 1)
        #Remove the product from the database
        product.delete()
        #Assert if the product has been successfully deleted from the database
        self.assertEqual(len(Product.all()), 0)
        
    def test_list_all_products(self):
        #Retrieve all products from the database and assign them to the products variable
        products = Product.all()
        #Assert there are no products in the database at the beginning of the test case
        self.assertEqual(len(Product.all()), 0)
        #Create five products and save them to the database
        products = [ProductFactory() for i in range(5)]
        logger.info(products)
        #Fetching all products from the database again and assert the count is 5
        products = Product.all()
        self.assertEqual(len(products), 5)
        
    def test_find_by_name(self):
        #Create a batch of 5 Product objects using the ProductFactory and save them to the database
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()
        #Retrieve the name of the first product in the products list
        name = products[0].name
        #Count the number of occurrences of the product name in the list
        count = len([product for product in products if product.name == name])
        #Retrieve products from the database that have the specified name
        found = Product.find_by_name(name)
        #Assert if the count of the found products matches the expected count
        self.assertEqual(found.count(), count)
        #Assert that each product’s name matches the expected name
        for product in found:
            self.assertEqual(product.name, name)
            
    def test_find_by_availability(self):
        #Create a batch of 10 Product objects using the ProductFactory and save them to the database
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        #Retrieve the availability of the first product in the products list
        available = products[0].available
        #Count the number of occurrences of the product availability in the list
        count = len([product for product in products if product.available == available])
        #Retrieve products from the database that have the specified availability
        found = Product.find_by_availability(available)
        #Assert if the count of the found products matches the expected count
        self.assertEqual(found.count(), count)
        #Assert that each product's availability matches the expected availability
        for product in found:
            self.assertEqual(product.available, available)
            
     def test_find_by_category
        #Create a batch of 10 Product objects using the ProductFactory and save them to the database
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        #Retrieve the availability of the first product in the products list
        category = products[0].category
        #Count the number of occurrences of the product that have the same category in the list
        count = len([product for product in products if product.category == category])
        #Retrieve products from the database that have the specified category
        found = Product.find_by_category(category)
        #Assert if the count of the found products matches the expected count
        self.assertEqual(found.count(), count)
        #Assert that each product's category matches the expected category
        for product in found:
            self.assertEqual(product.category, category)