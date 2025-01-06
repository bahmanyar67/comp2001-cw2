from app.models import Trail, TrailSchema, Tag, Coordinate
from app.extensions import db
from flask import abort
from connexion.context import context, operation, receive, request, scope


def get_all_trails(token_info):
    trails = Trail.query.all()
    trails_schema = TrailSchema(many=True, context={'user_role': token_info['role']})
    return trails_schema.dump(trails)


def get_trail_by_id(token_info, trail_id):
    trail = Trail.query.get(trail_id)
    if trail:
        trail_schema = TrailSchema(context={'user_role': token_info['role'] if token_info else 'user'})
        return trail_schema.dump(trail)
    return None


def create_trail(token_info, body):
    if token_info['role'] != 'admin':
        abort(401, 'Unauthorized')

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

    coordinates = body.get('coordinates', [])
    for coord in coordinates:
        new_coordinate = Coordinate(
            trail_id=new_trail.trail_id,
            latitude=coord['latitude'],
            longitude=coord['longitude']
        )
        db.session.add(new_coordinate)

    db.session.add(new_trail)
    db.session.commit()
    trail_schema = TrailSchema(context={'user_role': token_info['role'] if token_info else 'user'})
    return trail_schema.dump(new_trail)


def update_trail(token_info, trail_id, body):
    if token_info['role'] != 'admin':
        abort(401, 'Unauthorized')

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

        # Update coordinates
        db.session.query(Coordinate).filter(Coordinate.trail_id == trail_id).delete()
        coordinates = body.get('coordinates', [])
        for coord in coordinates:
            new_coordinate = Coordinate(
                trail_id=trail.trail_id,
                latitude=coord['latitude'],
                longitude=coord['longitude']
            )
            db.session.add(new_coordinate)

        db.session.commit()
        trail_schema = TrailSchema(context={'user_role': token_info['role'] if token_info else 'user'})
        return trail_schema.dump(trail)
    return None


def delete_trail(token_info, trail_id):
    if token_info['role'] != 'admin':
        abort(401, 'Unauthorized')

    trail = Trail.query.get(trail_id)
    if trail:
        db.session.delete(trail)
        db.session.commit()
        trail_schema = TrailSchema(context={'user_role': token_info['role'] if token_info else 'user'})
        return trail_schema.dump(trail)
    return None
