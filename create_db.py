# create_db.py
from app import db, app

app = app()

with app.app_context():
    db.create_all()
