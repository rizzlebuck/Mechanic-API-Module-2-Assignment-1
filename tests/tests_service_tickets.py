import unittest
from app import create_app
from app.extensions import db
from app.models import Customer, ServiceTicket, Mechanic, Inventory


class TestServiceTickets(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            # Create a default customer in the test DB
            customer = Customer(
                name="Ticket Owner",
                email="owner@example.com",
                password="pw",
            )
            db.session.add(customer)
            db.session.commit()

            # Store the integer ID so we don't depend on a live session
            self.customer_id = customer.id

        self.client = self.app.test_client()

        # Login to get token using the login endpoint
        login_resp = self.client.post(
            "/customers/login",
            json={"email": "owner@example.com", "password": "pw"},
        )
        self.assertEqual(login_resp.status_code, 200)
        self.token = login_resp.json["token"]
        self.auth_header = {"Authorization": f"Bearer {self.token}"}

    def test_create_ticket(self):
        payload = {
            "description": "Brake job",
            "vehicle": "Toyota Camry",
            "status": "open",
        }
        response = self.client.post(
            "/service-tickets/",
            json=payload,
            headers=self.auth_header,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["description"], "Brake job")

    def test_get_tickets(self):
        # Seed a ticket
        with self.app.app_context():
            t = ServiceTicket(
                description="Seed ticket",
                vehicle="Honda",
                status="open",
                customer_id=self.customer_id,
            )
            db.session.add(t)
            db.session.commit()

        response = self.client.get("/service-tickets/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)

    def test_edit_ticket_mechanics(self):
        with self.app.app_context():
            # Create mechanic + ticket
            mech1 = Mechanic(name="Mech1", specialization="Engine")
            mech2 = Mechanic(name="Mech2", specialization="Brakes")
            db.session.add_all([mech1, mech2])
            db.session.commit()

            ticket = ServiceTicket(
                description="Job",
                vehicle="Car",
                status="open",
                customer_id=self.customer_id,
            )
            db.session.add(ticket)
            db.session.commit()
            tid = ticket.id
            m1_id = mech1.id
            m2_id = mech2.id

        payload = {
            "add_ids": [m1_id, m2_id],
            "remove_ids": [],
        }

        response = self.client.put(
            f"/service-tickets/{tid}/edit",
            json=payload,
            headers=self.auth_header,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("mechanics", response.json)
        self.assertEqual(len(response.json["mechanics"]), 2)

    def test_add_part_to_ticket(self):
        with self.app.app_context():
            ticket = ServiceTicket(
                description="Job with parts",
                vehicle="Car",
                status="open",
                customer_id=self.customer_id,
            )
            part = Inventory(name="Brake Pad Set", price=89.99)
            db.session.add_all([ticket, part])
            db.session.commit()
            tid = ticket.id
            part_id = part.id

        response = self.client.put(
            f"/service-tickets/{tid}/add-part/{part_id}",
            headers=self.auth_header,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("parts", response.json)
        self.assertEqual(len(response.json["parts"]), 1)


if __name__ == "__main__":
    unittest.main()
