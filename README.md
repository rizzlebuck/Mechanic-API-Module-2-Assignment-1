# 🚗 Mechanic Shop Advanced API  
### Fully Deployed on Render • CI/CD Enabled • Swagger Documentation Included

Live API:  
👉 **https://mechanic-api-module-2-assignment-1.onrender.com**

GitHub Repo:  
👉 **https://github.com/rizzlebuck/Mechanic-API-Module-2-Assignment-1**

---

## 📌 Overview  
The **Mechanic Shop Advanced API** is a full-featured Flask REST API supporting:

- Customer Management  
- Mechanic Management  
- Inventory System  
- Service Ticket Workflow  
- JWT Authentication  
- Rate Limiting  
- Caching  
- Pagination  
- Swagger Documentation  
- Render Deployment  
- CI/CD Pipeline with GitHub Actions

This project completes **Backend Module 2**, demonstrating full API development, documentation, testing, deployment, and automated redeploy through Render.

---

# 🚀 Features  
### 🔐 Authentication  
- Customer registration & login  
- JWT token generation  
- Token-protected routes  

### 🧰 Mechanic & Inventory Management  
- Add/edit/delete mechanics  
- Add parts to service tickets  
- Track inventory quantity  

### 🧾 Service Tickets  
- Create service tickets  
- Assign mechanics  
- Attach parts to a ticket  
- Update statuses  

### ⚡ Performance  
- Global rate limiting  
- Request caching  

### 🧪 Testing  
- `unittest` test suite for all routes  
- Automated tests run on every push via GitHub Actions  

### 📚 Documentation  
- Full Swagger UI  
- Hosted at:  
👉 **https://mechanic-api-module-2-assignment-1.onrender.com/api/docs**

---

# 📁 Project File Structure  

---

# 🛠 Local Setup Instructions  

1️⃣ Clone the repo:  
git clone https://github.com/rizzlebuck/Mechanic-API-Module-2-Assignment-1
cd Mechanic-API-Module-2-Assignment-1

2️⃣ Create a virtual environment:
python3 -m venv venv
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

🔐 Environment Variables

Create a .env file (ignored by Git):
SQLALCHEMY_DATABASE_URI=postgresql://<user>:<password>@<host>/<dbname>
SECRET_KEY=your_random_secret_here
JWT_SECRET=another_random_secret_here

▶️ Running Locally:
python flask_app.py

📘 Swagger Documentation:
Production:
👉 https://mechanic-api-module-2-assignment-1.onrender.com/api/docs

🧪 Running Unit Tests
Run full test suite:
python -m unittest discover tests

☁️ Deployment (Render)
-This project is deployed on Render with:
-Managed PostgreSQL database
-Gunicorn web server
-ProductionConfig
-Environment variables set in dashboard
-Auto-deploy disabled
-CI/CD-controlled deployments

🤖 CI/CD Pipeline (GitHub Actions)

Workflow file:
.github/workflows/main.yaml

Includes three jobs:
✔ Build:
-Setup Python
-Install dependencies

✔ Test:
-Run unittest suite
-Depends on build job

✔ Deploy:
-Uses Render deploy action
-Only runs after tests pass
-Requires GitHub Secrets:
RENDER_API_KEY
SERVICE_ID

This ensures no broken code ever gets deployed.