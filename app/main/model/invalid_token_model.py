from app.main import db


class InvalidToken(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
