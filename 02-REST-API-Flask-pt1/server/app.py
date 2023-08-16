#!/usr/bin/env python3

# 📚 Review With Students:
# API Fundamentals
# MVC Architecture and Patterns / Best Practices
# RESTful Routing
# | HTTP Verb 	|       Path       	| Description        	|
# |-----------	|:----------------:	|--------------------	|
# | GET       	|   /productions   	| READ all resources 	|
# | GET       	| /productions/:id 	| READ one resource   	|
# | POST      	|   /productions   	| CREATE one resource 	|
# | PATCH/PUT 	| /productions/:id 	| UPDATE one resource	|
# | DELETE    	| /productions/:id 	| DESTROY one resource 	|

# Serialization
# Postman

# Set Up:
# In Terminal, `cd` into `server` and run the following:
# export FLASK_APP=app.py
# export FLASK_RUN_PORT=5000
# flask db init
# flask db revision --autogenerate -m 'Create tables'
# flask db upgrade
# python seed.py

from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import CastMember, Production, db

# 1. ✅ Import `Api` and `Resource` from `flask_restful`
# ❓ What do these two classes do at a higher level?


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Note: `app.json.compact = False` configures JSON responses to print on indented lines
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# 2. ✅ Initialize the Api
api = Api(app)

# 3. ✅ Create a Production class that inherits from Resource


class Productions(Resource):
    # def get(self):
    #     # import ipdb

    #     # ipdb.set_trace()
    #     productions_list = [
    #         {
    #             "title": production.title,
    #             "genre": production.genre,
    #             "budget": production.budget,
    #             "image": production.image,
    #             "director": production.director,
    #             "ongoing": production.ongoing,
    #         }
    #         for production in Production.query.all()
    #     ]  # like JS map
    #     return make_response(jsonify(productions_list), 200)

    # 4. ✅ Create a GET (All) Route
    # 4.1 Make a `get` method that takes `self` as a param.
    # 4.2 Create a `productions` array.
    # 4.3 Make a query for all productions. For each `production`, create a dictionary
    # containing all attributes before appending to the `productions` array.
    # 4.4 Create a `response` variable and set it to:
    #  #make_response(
    #       jsonify(productions),
    #       200
    #  )
    # 4.5 Return `response`.
    # 4.6 After building the route, run the server and test in the browser.

    # 5. ✅ Serialization
    # This is great, but there's a cleaner way to do this! Serialization will allow us to easily
    # convert our model objects to dictionairies as well as define their contents.
    # Navigate to `models.py` for Steps 6 - 9.

    # 10. ✅ Use our serializer to format our response to be cleaner
    # 10.1 Query all of the productions, convert them to a dictionary with `to_dict` before setting them to a list.
    # 10.2 Invoke `make_response`, pass it the production list along with a status of 200. Set `make_response` to a
    # `response` variable.
    # 10.3 Return the `response` variable.
    # 10.4 After building the route, run the server and test your results in the browser.
    def get(self):
        # import ipdb

        # ipdb.set_trace()
        productions_list = [
            production.to_dict() for production in Production.query.all()
        ]  # like JS map
        return make_response(jsonify(productions_list), 200)

    # 11. ✅ Create a POST Route
    # Prepare a POST request in Postman. Under the `Body` tab, select `form-data` and fill out the body
    # of a production request.

    # Create the POST route
    # 📚 Review With Students: request object

    # 11.1 Create a `post` method and pass it `self`.
    # 11.2 Create a new production from the `request.form` object.
    # 11.3 Add and commit the new production.
    # 11.4 Convert the new production to a dictionary with `to_dict`
    # 11.5 Set `make_response` to a `response` variable and pass it the new production along with a status of 201.
    # 11.6 Test the route in Postman.
    def post(self):
        request_json = request.get_json()
        # import ipdb

        # ipdb.set_trace()
        new_production = Production(
            title=request_json["title"],
            genre=request_json["genre"],
            budget=request_json["budget"],
            image=request_json["image"],
            director=request_json["director"],
            description=request_json["description"],
            ongoing=request_json["ongoing"],
        )
        db.session.add(new_production)
        db.session.commit()

        response_dict = new_production.to_dict()

        return make_response(
            response_dict,
            201,
        )


# 12. ✅ Add the new route to our api with `api.add_resource`
api.add_resource(Productions, "/productions")

# 13. ✅ Create a GET (One) route
# 13.1 Build a class called `ProductionByID` that inherits from `Resource`.
# 13.2 Create a `get` method and pass it the id along with `self`. (This is how we will gain access to
# the id from our request)
# 13.3 Make a query for our production by the `id` and build a `response` to send to the browser.


# 14. ✅ Add the new route to our api with `api.add_resource`

# the below is for if you prefer to run your Flask app as a script instead of from the Python shell. At the command line: python app.py
if __name__ == "__main__":
    app.run(port=5000, debug=True)
