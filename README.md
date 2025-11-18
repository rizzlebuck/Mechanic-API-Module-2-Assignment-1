# Mechanic API – Module 2 Assignment 1

This project is a Flask-based REST API for a mechanic shop.  
It demonstrates:

- Application Factory Pattern
- Blueprints for modular routing
- SQLAlchemy models and relationships
- Marshmallow schemas for validation/serialization
- JWT authentication
- Rate limiting and caching
- Swagger documentation
- Unit tests for every route

---

## 🛠 Setup

1. Clone the repository:
git clone https://github.com/rizzlebuck/Mechanic-API-Module-2-Assignment-1.git
cd Mechanic-API-Module-2-Assignment-1

3. Create and activate a virtual environment:
- python -m venv venv
# Mac / Linux: source venv/bin/activate
# On Windows: venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Configure environment (if needed):
- The default configs are in config.py.
- DevelopmentConfig – uses your MySQL DB (update URI if needed)
- TestingConfig – uses sqlite:///testing.db

🚀 Running the API: 
python app.py


By default the app will be available at:
http://127.0.0.1:5000/

📚 Swagger API Docs

Swagger UI is available at:
http://127.0.0.1:5000/api/docs/


From there you can:
- View all endpoints
- See request/response shapes
- Try out requests directly in the browser

🧪 Running Tests

All routes have unit tests using unittest.

Run them with:
python -m unittest discover tests

📬 Postman Collection

A Postman collection is included:
Mechanic - Advanced.postman_collection.json

You can import it into Postman to try all endpoints easily.
