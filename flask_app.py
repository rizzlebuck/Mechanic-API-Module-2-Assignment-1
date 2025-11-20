from app import create_app
from app.extensions import db

app = create_app("ProductionConfig")

if __name__ == "__main__":
    with app.app_context():
        #db.drop_all() <-- Take the "#" away when you need a fresh DB
        db.create_all()
