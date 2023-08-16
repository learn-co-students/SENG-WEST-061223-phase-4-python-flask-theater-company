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
from werkzeug.exceptions import NotFound

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# monkey-patching flask-restful's error_router to substitute Flask's native app.errorhandler
Api.error_router = lambda self, handler, e: handler(e)
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


class ProductionById(Resource):
    def get(self, id):
        production = Production.query.filter(Production.id == id).first()
        if not production:
            abort(404, "The Production you were trying to retrieve was not found")
        # prod_dict = production.to_dict()
        # res = make_response(prod_dict, 200)
        # return res
        return make_response(production.to_dict(), 200)

    def patch(self, id):
        production = Production.query.filter(Production.id == id).first()
        if not production:
            abort(404, "The Production you were trying to update was not found")
        form_json = request.get_json()
        for key in form_json:
            setattr(production, key, form_json[key])

        db.session.add(production)
        db.session.commit()

        return make_response(production.to_dict(), 202)

    def delete(self, id):
        production = Production.query.filter(Production.id == id).first()
        if not production:
            abort(404, "The Production you were trying to delete was not found")

        db.session.delete(production)
        db.session.commit()

        return make_response("", 204)


api.add_resource(ProductionById, "/productions/<int:id>")


class CastMembers(Resource):
    def get(self):
        members = [member.to_dict() for member in CastMember.query.all()]
        return make_response(
            members,
            200,
        )

    def post(self):
        # new_member = CastMember(
        #     name=request.get_json()["name"],
        #     role=request.get_json()["role"],
        #     production_id=request.get_json()["production_id"],
        # )
        new_member = CastMember()
        form_json = request.get_json()
        # we can do mass assignment with a post request
        # with mass assignment, it is crucial that the keys of the request body json all match exactly with properties of the model object
        for key in form_json:
            setattr(new_member, key, form_json[key])

        db.session.add(new_member)
        db.session.commit()

        return make_response(
            new_member.to_dict(),
            201,
        )


api.add_resource(CastMembers, "/cast_members")


# if you want this to work with flask-restful, see the monkey-patching line just before api = Api(app)
@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        "Not Found: Sorry the resource you are looking for doesn't exist", 404
    )
    return response


if __name__ == "__main__":
    app.run(port=5000, debug=True)
