from app.models import Tag, TagSchema
from app.extensions import db

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


def create_tag(body):
    new_tag = Tag(body['tag_name'])
    db.session.add(new_tag)
    db.session.commit()
    return tag_schema.dump(new_tag)


def update_tag(tag_id, body):
    tag = Tag.query.get(tag_id)
    if tag:
        tag.tag_name = body['tag_name']
        db.session.commit()
        return tag_schema.dump(tag)
    return None


def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    if tag:
        db.session.delete(tag)
        db.session.commit()
        return tag_schema.dump(tag)
    return None
