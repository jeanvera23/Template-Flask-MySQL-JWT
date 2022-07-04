from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    firstName = db.Column(db.String(80), nullable=False)
    lastName = db.Column(db.String(80))
    updatedAt = db.Column(db.DateTime, onupdate=datetime.now())
    createdAt = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return 'User>>> {self.username}'
