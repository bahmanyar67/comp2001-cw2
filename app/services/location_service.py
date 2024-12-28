from app.models import Location, LocationSchema
from app.extensions import db

location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)


def get_all_locations():
    locations = Location.query.all()
    return locations_schema.dump(locations)


def get_location_by_id(location_id):
    location = Location.query.get(location_id)
    if location:
        return location_schema.dump(location)
    return None


def create_location(body):
    new_location = Location(body['location_name'])
    db.session.add(new_location)
    db.session.commit()
    return location_schema.dump(new_location)


def update_location(location_id, body):
    location = Location.query.get(location_id)
    if location:
        location.location_name = body['location_name']
        db.session.commit()
        return location_schema.dump(location)
    return None


def delete_location(location_id):
    location = Location.query.get(location_id)
    if location:
        db.session.delete(location)
        db.session.commit()
        return location_schema.dump(location)
    return None
