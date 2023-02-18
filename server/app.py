#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
import pdb

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        plant_dicts = [plant.to_dict() for plant in plants]
        response = make_response(plant_dicts, 200)
        return response

    def post(self):
        data = request.get_json()
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price']
        )
        # pdb.set_trace()
        db.session.add(new_plant)
        db.session.commit()
        response = make_response(new_plant.to_dict(), 201)
        return response

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        # pdb.set_trace()
        plant = Plant.query.filter_by(id=id).first()
        response = make_response(plant.to_dict(), 200)
        # pdb.set_trace()
        return response
        
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
