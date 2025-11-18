import unittest
from app import create_app
from app.extensions import db
from app.models import Mechanic, ServiceTicket, Customer


class TestMechanics(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")

        with self.app.app_context():
            db.drop_all()
            db.create_all()

        self.client = self.app.test_client()

    def test_create_mechanic(self):
        payload = {
            "name": "Alex Wrench",
            "specialization": "Engine",
        }

        response = self.client.post("/mechanics/", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "Alex Wrench")

    def test_get_mechanics(self):
        # Seed a mechanic
        with self.app.app_context():
            m = Mechanic(name="Mech1", specialization="Brakes")
            db.session.add(m)
            db.session.commit()

        response = self.client.get("/mechanics/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)

    def test_update_mechanic(self):
        with self.app.app_context():
            m = Mechanic(name="Old Name", specialization="General")
            db.session.add(m)
            db.session.commit()
            mid = m.id

        payload = {
            "name": "New Name",
        }
        response = self.client.put(f"/mechanics/{mid}", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "New Name")

    def test_delete_mechanic(self):
        with self.app.app_context():
            m = Mechanic(name="Delete Me", specialization="None")
            db.session.add(m)
            db.session.commit()
            mid = m.id

        response = self.client.delete(f"/mechanics/{mid}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json)

    def test_mechanics_by_ticket_count(self):
        with self.app.app_context():
            c = Customer(name="Cust", email="cust@example.com", password="pw")
            db.session.add(c)
            db.session.commit()

            m1 = Mechanic(name="Busy Mech", specialization="Engine")
            m2 = Mechanic(name="Free Mech", specialization="Brakes")
            db.session.add_all([m1, m2])
            db.session.commit()

            t1 = ServiceTicket(
                description="Job 1", vehicle="Car", status="open", customer_id=c.id
            )
            t2 = ServiceTicket(
                description="Job 2", vehicle="Car", status="open", customer_id=c.id
            )
            db.session.add_all([t1, t2])
            db.session.commit()

            # Associate mechanic m1 with both tickets
            t1.mechanics.append(m1)
            t2.mechanics.append(m1)
            db.session.commit()

        response = self.client.get("/mechanics/by-ticket-count")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        # Busy Mech should be first
        self.assertGreaterEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["name"], "Busy Mech")


if __name__ == "__main__":
    unittest.main()
