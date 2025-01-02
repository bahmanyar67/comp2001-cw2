from app.models import Tag, TagSchema
from app.extensions import db
from flask import abort

tag_schema = TagSchema()
tags_schema = TagSchema(many=True)


def get_all_tags():
    tags = Tag.query.all()
    return tags_schema.dump(tags)


def get_tag_by_id(tag_id):
    tag = Tag.query.get(tag_id)
    if tag:
        return tag_schema.dump(tag)
    return None


def create_tag(token_info, body):
    if token_info['role'] != 'admin':
        abort(401, 'Unauthorized')
    new_tag = Tag(body['tag_name'])
    db.session.add(new_tag)
    db.session.commit()
    return tag_schema.dump(new_tag)


def update_tag(token_info, tag_id, body):
    if token_info['role'] != 'admin':
        abort(401, 'Unauthorized')
    tag = Tag.query.get(tag_id)
    if tag:
        tag.tag_name = body['tag_name']
        db.session.commit()
        return tag_schema.dump(tag)
    return None


def delete_tag(token_info, tag_id):
    if token_info['role'] != 'admin':
        abort(401, 'Unauthorized')
    tag = Tag.query.get(tag_id)
    if tag:
        db.session.delete(tag)
        db.session.commit()
        return tag_schema.dump(tag)
    return None
