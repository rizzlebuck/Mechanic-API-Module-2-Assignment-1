import unittest
from app import create_app
from app.extensions import db
from app.models import Customer, Inventory


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")

        with self.app.app_context():
            db.drop_all()
            db.create_all()

        self.client = self.app.test_client()

        # Create a default customer + token so we can hit token-protected inventory routes
        with self.app.app_context():
            self.customer = Customer(
                name="Inv User",
                email="inv@example.com",
                password="pw",
            )
            db.session.add(self.customer)
            db.session.commit()

        login_resp = self.client.post(
            "/customers/login",
            json={"email": "inv@example.com", "password": "pw"},
        )
        self.assertEqual(login_resp.status_code, 200)
        self.token = login_resp.json["token"]
        self.auth_header = {"Authorization": f"Bearer {self.token}"}

    def test_create_inventory_item(self):
        payload = {
            "name": "Oil Filter",
            "price": 19.99,
        }

        response = self.client.post(
            "/inventory/",
            json=payload,
            headers=self.auth_header,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "Oil Filter")

    def test_get_inventory_list(self):
        with self.app.app_context():
            part = Inventory(name="Spark Plug", price=9.99)
            db.session.add(part)
            db.session.commit()

        response = self.client.get("/inventory/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)

    def test_get_single_inventory_item(self):
        with self.app.app_context():
            part = Inventory(name="Alternator", price=199.99)
            db.session.add(part)
            db.session.commit()
            pid = part.id

        response = self.client.get(f"/inventory/{pid}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Alternator")

    def test_update_inventory_item(self):
        with self.app.app_context():
            part = Inventory(name="Air Filter", price=25.0)
            db.session.add(part)
            db.session.commit()
            pid = part.id

        payload = {
            "price": 20.0,
        }

        response = self.client.put(
            f"/inventory/{pid}",
            json=payload,
            headers=self.auth_header,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["price"], 20.0)

    def test_delete_inventory_item(self):
        with self.app.app_context():
            part = Inventory(name="To Delete", price=5.0)
            db.session.add(part)
            db.session.commit()
            pid = part.id

        response = self.client.delete(
            f"/inventory/{pid}",
            headers=self.auth_header,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json)


if __name__ == "__main__":
    unittest.main()
