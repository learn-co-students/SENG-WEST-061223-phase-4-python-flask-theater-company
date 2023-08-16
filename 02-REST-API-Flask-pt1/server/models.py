from flask_sqlalchemy import SQLAlchemy

# 6. ✅ Import `SerializerMixin` from `sqlalchemy_serializer`
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()


# 7. ✅ Pass `SerializerMixin` to `Productions`
class Production(db.Model, SerializerMixin):
    __tablename__ = "productions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    genre = db.Column(db.String)
    budget = db.Column(db.Float)
    image = db.Column(db.String)
    director = db.Column(db.String)
    description = db.Column(db.String)
    ongoing = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    cast_members = db.relationship("CastMember", back_populates="production")

    # 7.1 ✅ Create a serialize rule that will prevent circular embedding through our relationship  and remove created_at and updated_at from the response
    # 7.2 Demo serialize_only by only allowing title to be included in the response
    #    once done remove or comment the serialize_only line.

    serialize_rules = (
        "-cast_members.production",
        "-created_at",
        "-updated_at",
    )

    def __repr__(self):
        return f"<Production Title:{self.title}, Genre:{self.genre}, Budget:{self.budget}, Image:{self.image}, Director:{self.director},ongoing:{self.ongoing}>"


# 8. ✅ Pass `SerializerMixin` to `CastMember`
class CastMember(db.Model, SerializerMixin):
    __tablename__ = "cast_members"  # optional, but default to snake_case singular

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    role = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    production_id = db.Column(db.Integer, db.ForeignKey("productions.id"))
    production = db.relationship("Production", back_populates="cast_members")

    # 8.1 ✅ Create a serialize rule that will prevent circular recursion
    # N.B. Rules must be a tuple, so even if you only have one rule string, don't forget the trailing comma!
    serialize_rules = ("-production.cast_members",)
    # You can use serialize_only to define response content inclusively rather than exclusively.
    # serialize_only = (
    #     "name",
    #     "role",
    # )

    def __repr__(self):
        return f"<Production Name:{self.name}, Role:{self.role}"


# 9. ✅ Navigate back to `app.py` for further steps.
