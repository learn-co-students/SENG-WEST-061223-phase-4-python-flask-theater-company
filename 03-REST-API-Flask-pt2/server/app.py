#!/usr/bin/env python3

# 📚 Review With Students:
# REST
# Status codes
# Error handling

# Set up:
# cd into server and run the following in the terminal
# export FLASK_APP=app.py
# export FLASK_RUN_PORT=5000
# flask db init
# flask db revision --autogenerate -m'Create tables'
# flask db upgrade
# python seed.py

from flask import Flask, abort, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import CastMember, Production, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


api = Api(app)


class Productions(Resource):
    def get(self):
        production_list = [p.to_dict() for p in Production.query.all()]
        response = make_response(
            production_list,
            200,
        )

        return response

    def post(self):
        request_json = request.get_json()
        new_production = Production(
            title=request_json["title"],
            genre=request_json["genre"],
            budget=int(request_json["budget"]),
            image=request_json["image"],
            director=request_json["director"],
            description=request_json["description"],
            ongoing=bool(request_json["ongoing"]),
        )

        db.session.add(new_production)
        db.session.commit()

        response_dict = new_production.to_dict()

        response = make_response(
            response_dict,
            201,
        )
        return response


api.add_resource(Productions, "/productions")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
