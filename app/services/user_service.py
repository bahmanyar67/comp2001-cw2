from app.models import User, UserSchema
from app.extensions import db

user_schema = UserSchema()
users_schema = UserSchema(many=True)


def get_all_users():
    users = User.query.all()
    return users_schema.dump(users)


def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        return user_schema.dump(user)
    return None


def create_user(body):
    new_user = User(body['user_email'], body['user_role'])
    db.session.add(new_user)
    db.session.commit()
    return user_schema.dump(new_user)


def update_user(user_id, body):
    user = User.query.get(user_id)
    if user:
        user.user_email = body['user_email']
        user.user_role = body['user_role']
        db.session.commit()
        return user_schema.dump(user)
    return None


def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return user_schema.dump(user)
    return None
