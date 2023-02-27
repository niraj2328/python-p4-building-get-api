# server/app.py

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    genre = db.Column(db.String)
    platform = db.Column(db.String)
    price = db.Column(db.Float)

    def to_dict(self):
        return {
            'title': self.title,
            'genre': self.genre,
            'platform': self.platform,
            'price': self.price,
        }

@app.route('/')
def index():
    return "Index for Game/Review/User API"

@app.route('/games')
def games():
    games = [game.to_dict() for game in Game.query.all()]
    return make_response(jsonify(games), 200)

@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.get_or_404(id)
    return make_response(jsonify(game.to_dict()), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
