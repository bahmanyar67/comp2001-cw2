from app.models import Trail, TrailSchema, Tag
from app.extensions import db

trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)


def get_all_trails():
    trails = Trail.query.all()
    return trails_schema.dump(trails)


def get_trail_by_id(trail_id):
    trail = Trail.query.get(trail_id)
    if trail:
        return trail_schema.dump(trail)
    return None


def create_trail(body):
    new_trail = Trail(
        trail_name=body.get('trail_name'),
        trail_summary=body.get('trail_summary'),
        trail_description=body.get('trail_description'),
        trail_owner_id=body.get('trail_owner_id'),
        trail_route_type_id=body.get('trail_route_type_id'),
        trail_surface_type_id=body.get('trail_surface_type_id'),
        trail_location_id=body.get('trail_location_id'),
        trail_street=body.get('trail_street'),
        trail_postal_code=body.get('trail_postal_code'),
        trail_county_id=body.get('trail_county_id'),
        trail_length=body.get('trail_length'),
        trail_length_unit=body.get('trail_length_unit'),
        trail_elevation_gain=body.get('trail_elevation_gain'),
        trail_elevation_gain_unit=body.get('trail_elevation_gain_unit'),
        trail_starting_point_lat=body.get('trail_starting_point_lat'),
        trail_starting_point_long=body.get('trail_starting_point_long'),
        trail_ending_point_lat=body.get('trail_ending_point_lat'),
        trail_ending_point_long=body.get('trail_ending_point_long'),
        trail_difficulty=body.get('trail_difficulty'),
        tags=Tag.query.filter(Tag.tag_id.in_(body.get('tag_ids', []))).all()
    )

    db.session.add(new_trail)
    db.session.commit()
    return trail_schema.dump(new_trail)


def update_trail(trail_id, body):
    trail = Trail.query.get(trail_id)
    if trail:
        trail.trail_name = body.get('trail_name', trail.trail_name)
        trail.trail_summary = body.get('trail_summary', trail.trail_summary)
        trail.trail_description = body.get('trail_description', trail.trail_description)
        trail.trail_owner_id = body.get('trail_owner_id', trail.trail_owner_id)
        trail.trail_route_type_id = body.get('trail_route_type_id', trail.trail_route_type_id)
        trail.trail_surface_type_id = body.get('trail_surface_type_id', trail.trail_surface_type_id)
        trail.trail_location_id = body.get('trail_location_id', trail.trail_location_id)
        trail.trail_street = body.get('trail_street', trail.trail_street)
        trail.trail_postal_code = body.get('trail_postal_code', trail.trail_postal_code)
        trail.trail_county_id = body.get('trail_county_id', trail.trail_county_id)
        trail.trail_length = body.get('trail_length', trail.trail_length)
        trail.trail_length_unit = body.get('trail_length_unit', trail.trail_length_unit)
        trail.trail_elevation_gain = body.get('trail_elevation_gain', trail.trail_elevation_gain)
        trail.trail_elevation_gain_unit = body.get('trail_elevation_gain_unit', trail.trail_elevation_gain_unit)
        trail.trail_starting_point_lat = body.get('trail_starting_point_lat', trail.trail_starting_point_lat)
        trail.trail_starting_point_long = body.get('trail_starting_point_long', trail.trail_starting_point_long)
        trail.trail_ending_point_lat = body.get('trail_ending_point_lat', trail.trail_ending_point_lat)
        trail.trail_ending_point_long = body.get('trail_ending_point_long', trail.trail_ending_point_long)
        trail.trail_difficulty = body.get('trail_difficulty', trail.trail_difficulty)
        trail.tags = Tag.query.filter(Tag.tag_id.in_(body.get('tag_ids', []))).all()

        db.session.commit()
        return trail_schema.dump(trail)
    return None


def delete_trail(trail_id):
    trail = Trail.query.get(trail_id)
    if trail:
        db.session.delete(trail)
        db.session.commit()
        return trail_schema.dump(trail)
    return None
