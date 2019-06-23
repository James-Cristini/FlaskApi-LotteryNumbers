import os

from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from helpers import date_helpers
from helpers import errors

### TODO Add logging
### TODO Separate module (models, routes, etc.)
### TODO use id=<id> in url routes

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

###### Models ######
class PowerballDrawing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    draw_date = db.Column(db.String(25)) # Expecting to use format: 20190522
    number_1 = db.Column(db.Integer)
    number_2 = db.Column(db.Integer)
    number_3 = db.Column(db.Integer)
    number_4 = db.Column(db.Integer)
    number_5 = db.Column(db.Integer)
    powerball_number = db.Column(db.Integer)
    multiplier = db.Column(db.Integer)

    def __init__(self, draw_date, n1, n2, n3, n4, n5, pb, multiplier):
        self.draw_date = draw_date
        self.number_1 = n1
        self.number_2 = n2
        self.number_3 = n3
        self.number_4 = n4
        self.number_5 = n5
        self.powerball_number = pb
        self.multiplier = multiplier


class PowerballDrawingSchema(ma.Schema):
    class Meta:
        fields = ['draw_date', 'number_1', 'number_2', 'number_3', 'number_4', 'number_5', 'powerball_number', 'multiplier']


class MegaMillionDrawing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    draw_date = db.Column(db.String(25))
    number_1 = db.Column(db.Integer)
    number_2 = db.Column(db.Integer)
    number_3 = db.Column(db.Integer)
    number_4 = db.Column(db.Integer)
    number_5 = db.Column(db.Integer)
    megaball_number = db.Column(db.Integer)
    multiplier = db.Column(db.Integer)

    def __init__(self, draw_date, n1, n2, n3, n4, n5, mb, multiplier):
        self.draw_date = draw_date
        self.number_1 = n1
        self.number_2 = n2
        self.number_3 = n3
        self.number_4 = n4
        self.number_5 = n5
        self.megaball_number = mb
        self.multiplier = multiplier


class MegaMillionDrawingSchema(ma.Schema):
    class Meta:
        fields = ['draw_date', 'number_1', 'number_2', 'number_3', 'number_4', 'number_5', 'megaball_number', 'multiplier']


powerball_drawing_schema = PowerballDrawingSchema(strict=True)
powerball_drawings_schema = PowerballDrawingSchema(many=True, strict=True)

megamillions_drawing_schema = MegaMillionDrawingSchema(strict=True)
megamillions_drawings_schema = MegaMillionDrawingSchema(many=True, strict=True)


###### POWERBALL ROUTES ######
@app.route('/powerball', methods=['GET'])
def get_all_powerball_drawings():
    """ Get and return query of all powerball drawings. """

    all_drawings = PowerballDrawing.query.all()
    result = powerball_drawings_schema.dump(all_drawings)
    return jsonify(result.data)


@app.route('/powerball/id=<id>', methods=['GET'])
def get_powerball_drawing(id):
    """ Get and return query for a single powerball drawing by id. """

    drawing = PowerballDrawing.query.get(id)
    return powerball_drawing_schema.jsonify(drawing)


@app.route('/powerball', methods=['POST'])
def add_powerball_drawing():
    """ Add a new powerball drawing to the db. """

    dt = request.json['draw_date']
    n1 = request.json['number_1']
    n2 = request.json['number_2']
    n3 = request.json['number_3']
    n4 = request.json['number_4']
    n5 = request.json['number_5']
    pb = request.json['powerball_number']
    mult = request.json['multiplier']

    try:
        dt = date_helpers.validate_date(dt)
    except errors.DataValidationError as e:
        raise

    new_drawing = PowerballDrawing(dt, n1, n2, n3, n4, n5, pb, mult)
    db.session.add(new_drawing)
    db.session.commit()

    return powerball_drawing_schema.jsonify(new_drawing)


@app.route('/powerball/<id>', methods=['DELETE'])
def delete_powerball_drawing(id):
    """ Remove a powerball drawing from the db by id. """

    drawing = PowerballDrawing.query.get(id)

    db.session.delete(drawing)
    db.session.commit()

    return powerball_drawing_schema.jsonify(drawing)


@app.route('/powerball/last_drawing', methods=['GET'])
def get_most_recent_powerball_drawing():
    """ Gets and returns the most recent powerball drawing in the db. """

    last_draw = PowerballDrawing.query.order_by(PowerballDrawing.draw_date.desc()).first()
    result = powerball_drawing_schema.dump(last_draw)
    return jsonify(result)


###### MEGAMILLIONS ROUTES ######
@app.route('/megamillions', methods=['GET'])
def get_all_megamillions_drawings():
    """ Get and return query of all megamillions drawings. """

    all_drawings = MegaMillionDrawing.query.all()
    result = megamillions_drawings_schema.dump(all_drawings)
    return jsonify(result.data)


@app.route('/megamillions/<id>', methods=['GET']) # make id=<id>
def get_megamillions_drawing(id):
    """ Get and return query for a single megamillions drawing by id. """

    drawing = MegaMillionDrawing.query.get(id)
    return megamillions_drawing_schema.jsonify(drawing)


@app.route('/megamillions', methods=['POST'])
def add_megamillions_drawing():
    """ Add a new megamillions drawing to the db. """

    dt = request.json['draw_date']
    n1 = request.json['number_1']
    n2 = request.json['number_2']
    n3 = request.json['number_3']
    n4 = request.json['number_4']
    n5 = request.json['number_5']
    mb = request.json['megaball_number']
    mult = request.json['multiplier']

    try:
        dt = date_helpers.validate_date(dt)
    except errors.DataValidationError as e:
        raise

    new_drawing = MegaMillionDrawing(dt, n1, n2, n3, n4, n5, mb, mult)
    db.session.add(new_drawing)
    db.session.commit()

    return megamillions_drawing_schema.jsonify(new_drawing)


@app.route('/megamillions/<id>', methods=['DELETE'])
def delete_megamillions_drawing(id):
    """ Remove a megamillions drawing from the db by id. """

    drawing = MegaMillionDrawing.query.get(id)

    db.session.delete(drawing)
    db.session.commit()

    return megamillions_drawing_schema.jsonify(drawing)

@app.route('/megamillions/last_drawing', methods=['GET'])
def get_most_recent_megamillion_drawing():
    """ Gets and returns the most recent megamillion drawing in the db. """

    last_draw = MegaMillionDrawing.query.order_by(MegaMillionDrawing.draw_date.desc()).first()
    result = megamillions_drawing_schema.dump(last_draw)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=DEBUG)