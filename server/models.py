# server/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()


class BaseModel(db.Model, SerializerMixin):
    __abstract__ = True
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


class Game(BaseModel):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    genre = db.Column(db.String)
    platform = db.Column(db.String)
    price = db.Column(db.Integer)

    reviews = db.relationship('Review', backref='game', cascade='all, delete-orphan')

    serialize_rules = ('-reviews.game',)

    def __repr__(self):
        return f'<Game {self.title} for {self.platform}>'


class Review(BaseModel):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    comment = db.Column(db.String)

    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    serialize_rules = ('-game.reviews', '-user.reviews',)

    def __repr__(self):
        return f'<Review ({self.id}) of {self.game}: {self.score}/10>'


class User(BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    reviews = db.relationship('Review', backref='user', cascade='all, delete-orphan')

    serialize_rules = ('-reviews.user',)
