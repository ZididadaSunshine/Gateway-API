from sqlalchemy import Column, String, DateTime, Integer

from app.main import database


class InvalidToken(database.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    creation_date = Column(DateTime, nullable=False)
    token = Column(String(255), unique=True, nullable=False)
