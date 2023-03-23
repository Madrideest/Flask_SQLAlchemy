import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"


db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))

    group = relationship("Group", back_populates="users")


class Group(db.Model):
    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    users = relationship("User", back_populates="group")


with app.app_context():
    db.drop_all()
    db.create_all()

    group_01 = Group(id=1, name="Group 1")
    user_john = User(id=1, name='john', age=31, group=group_01)

    with db.session.begin():
        db.session.add(user_john)

    user_sergio = User(id=2, name='sergio', age=26)
    group_02 = Group(id=2, name="Group 2", users=[user_sergio])

    with db.session.begin():
        db.session.add(user_sergio)


users_group = User.query.get(1)
print(users_group.group.name)


@app.route('/users/first')
def get_users_first():
    user = User.query.first()

    return json.dumps(
        {
            "id": user.id,
            "name": user.name,
            "age": user.age
        }
    )


@app.route('/users/count')
def get_users_count():
    users_count = User.query.count()

    return json.dumps(users_count)


@app.route('/users')
def get_users():
    users_list = User.query.all()

    users_resp = []

    for user in users_list:
        users_resp.append(
            {
                "id": user.id,
                "name": user.name,
                "age": user.age
            }
        )
    return json.dumps(users_resp)


@app.route('/users/<int:sid>')
def get_user(sid: int):
    user = User.query.get(sid)

    if user is None:
        return "user not found"

    return json.dumps({
                "id": user.id,
                "name": user.name,
                "age": user.age
            })


if __name__ == '__main__':
    app.run(debug=True)
