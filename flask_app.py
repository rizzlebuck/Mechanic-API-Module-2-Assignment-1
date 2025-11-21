from app import create_app

# For Render / gunicorn: this is the WSGI app object
app = create_app("ProductionConfig")

# Allows running locally with `python flask_app.py`
if __name__ == "__main__":
    app.run(debug=True)
