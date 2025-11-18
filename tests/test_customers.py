import unittest
from app import create_app
from app.extensions import db
from app.models import Customer, ServiceTicket


class TestCustomers(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.app.config["WTF_CSRF_ENABLED"] = False

        with self.app.app_context():
            db.drop_all()
            db.create_all()

        self.client = self.app.test_client()

    # Creates a customer directly in DB
    def _create_customer_in_db(self, name="Test User", email="test@example.com", password="password"):
        with self.app.app_context():
            customer = Customer(name=name, email=email, password=password)
            db.session.add(customer)
            db.session.commit()
            return customer

    # Get token via login endpoint
    def _get_token_for_customer(self, email="test@example.com", password="password"):
        # Ensure customer exists
        self._create_customer_in_db(email=email, password=password)

        credentials = {
            "email": email,
            "password": password,
        }
        response = self.client.post("/customers/login", json=credentials)
        self.assertEqual(response.status_code, 200)
        return response.json["token"]

    def test_create_customer_success(self):
        payload = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "secret123",
        }

        response = self.client.post("/customers/", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "John Doe")
        self.assertEqual(response.json["email"], "john@example.com")

    def test_create_customer_missing_email(self):
        payload = {
            "name": "No Email",
            "password": "secret123",
        }

        response = self.client.post("/customers/", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)
        self.assertIn("name, email, and password are required", response.json["error"])

    def test_get_customers_paginated(self):
        # Seed a few customers
        with self.app.app_context():
            for i in range(7):
                c = Customer(name=f"User{i}", email=f"user{i}@example.com", password="pw")
                db.session.add(c)
            db.session.commit()

        response = self.client.get("/customers/?page=1&per_page=5")
        self.assertEqual(response.status_code, 200)
        self.assertIn("items", response.json)
        self.assertLessEqual(len(response.json["items"]), 5)

    def test_login_success(self):
        # Create user in DB
        self._create_customer_in_db(email="login@example.com", password="mypw")

        credentials = {
            "email": "login@example.com",
            "password": "mypw",
        }
        response = self.client.post("/customers/login", json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json)

    def test_login_invalid_credentials(self):
        # No user yet
        credentials = {
            "email": "nope@example.com",
            "password": "wrong",
        }
        response = self.client.post("/customers/login", json=credentials)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json["error"], "Invalid email or password")

    def test_my_tickets_requires_token(self):
        response = self.client.get("/customers/my-tickets")
        self.assertEqual(response.status_code, 401)
        self.assertIn("error", response.json)

    def test_my_tickets_success(self):
        # Create customer + ticket
        with self.app.app_context():
            customer = Customer(name="Ticket Owner", email="owner@example.com", password="pw")
            db.session.add(customer)
            db.session.commit()

            ticket = ServiceTicket(
                description="Oil change",
                vehicle="Honda",
                status="open",
                customer_id=customer.id,
            )
            db.session.add(ticket)
            db.session.commit()

        # Login to get token
        credentials = {
            "email": "owner@example.com",
            "password": "pw",
        }
        login_resp = self.client.post("/customers/login", json=credentials)
        self.assertEqual(login_resp.status_code, 200)
        token = login_resp.json["token"]

        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.get("/customers/my-tickets", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)


if __name__ == "__main__":
    unittest.main()
