import os

from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from helpers import date_helpers
from helpers import errors


DEBUG = True

# Init App
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app) # don't forget to go into shell and db.create_all()

# Init ma
ma = Marshmallow(app)

# Powerball Drawing Model
class PowerballDrawing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    draw_date = db.Column(db.DateTime)
    number_1 = db.Column(db.Integer)
    number_2 = db.Column(db.Integer)
    number_3 = db.Column(db.Integer)
    number_4 = db.Column(db.Integer)
    number_5 = db.Column(db.Integer)
    powerball_number = db.Column(db.Integer)

    def __init__(self, draw_date, n1, n2, n3, n4, n5, pb):
        self.draw_date = draw_date
        self.number_1 = n1
        self.number_2 = n2
        self.number_3 = n3
        self.number_4 = n4
        self.number_5 = n5
        self.powerball_number = pb

class PowerballDrawingSchema(ma.Schema):
    class Meta:
        fields = ['draw_date', 'number_1', 'number_2', 'number_3', 'number_4', 'number_5', 'powerball_number']

# Mega Million Drawing Model
class MegaMillionDrawing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    draw_date = db.Column(db.DateTime)
    number_1 = db.Column(db.Integer)
    number_2 = db.Column(db.Integer)
    number_3 = db.Column(db.Integer)
    number_4 = db.Column(db.Integer)
    number_5 = db.Column(db.Integer)
    megaball_number = db.Column(db.Integer)

    def __init__(self, draw_date, n1, n2, n3, n4, n5, mb):
        self.draw_date = date
        self.number_1 = n1
        self.number_2 = n2
        self.number_3 = n3
        self.number_4 = n4
        self.number_5 = n5
        self.megaball_number = pb

class MegaMillionDrawingSchema(ma.Schema):
    class Meta:
        fields = ['date', 'number_1', 'number_2', 'number_3', 'number_4', 'number_5', 'megaball_number']

powerball_drawing_schema = PowerballDrawingSchema(strict=True)
powerball_drawings_schema = PowerballDrawingSchema(many=True, strict=True)

megamillions_drawing_schema = MegaMillionDrawingSchema(strict=True)
megamillions_drawings_schema = MegaMillionDrawingSchema(many=True, strict=True)

# Get all Powerball Drawings
@app.route('/powerball', methods=['GET'])
def get_all_powerball_drawings():
    all_drawings = PowerballDrawing.query.all()
    result = powerball_drawings_schema.dump(all_drawings)
    return jsonify(result.data)

@app.route('/powerball/<id>', methods=['GET'])
def get_powerball_drawings(id):
    drawing = PowerballDrawing.query.get(id)
    return powerball_drawing_schema.jsonify(drawing)

@app.route('/powerball', methods=['POST'])
def add_powerball_drawing():
    dt = request.json['draw_date']
    n1 = request.json['number_1']
    n2 = request.json['number_2']
    n3 = request.json['number_3']
    n4 = request.json['number_4']
    n5 = request.json['number_5']
    pb = request.json['powerball_number']

    try:
        dt = date_helpers.validate_date(dt)
    except DataValidationError as e:
        raise

    new_drawing = PowerballDrawing(dt, n1, n2, n3, n4, n5, pb)
    db.session.add(new_drawing)
    db.session.commit()

    return powerball_drawing_schema.jsonify(new_drawing)

@app.route('/powerball/<id>', methods=['DELETE'])
def delete_powerball_drawing(id):
    drawing = PowerballDrawing.query.get(id)

    db.session.delete(drawing)
    db.session.commit()

    return powerball_drawing_schema.jsonify(drawing)

@app.route('/powerball/by_id/<id>', methods=['GET'])
def get_drawing_by_id(id):
    pass

@app.route('/powerball/by_date/<dt>', methods=['GET'])
def get_drawing_by_date(dt):
    pass

@app.route('/powerball/by_powerball_number/<pb>', methods=['GET'])
def get_drawing_by_powerball_number(pb):
    pass

if __name__ == '__main__':
    app.run(debug=DEBUG)