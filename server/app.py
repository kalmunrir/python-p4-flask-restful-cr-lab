#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

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
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(plants, 200)
    
    def post(self):
        new_plant = Plant(
            image = request.get_json()["image"],
            name = request.get_json()["name"],
            price = request.get_json()["price"]
        )
        db.session.add(new_plant)
        db.session.commit()
        return make_response(new_plant.to_dict(), 201)
api.add_resource(Plants, "/plants")

class PlantByID(Resource):
    def get(self, id):
        if plant := Plant.query.filter_by(id=id).first():
            body = plant.to_dict()
            status = 200
        else:
            body = {"message": "Plant ID not found"}
            status = 404
        return make_response(body, status)
api.add_resource(PlantByID, "/plants/<int:id>") 

if __name__ == '__main__':
    app.run(port=5555, debug=True)
