from app.models import County, CountySchema
from app.extensions import db
from flask import abort

county_schema = CountySchema()
counties_schema = CountySchema(many=True)


def get_all_counties():
    counties = County.query.all()
    return counties_schema.dump(counties)


def get_county_by_id(county_id):
    county = County.query.get(county_id)
    if county:
        return county_schema.dump(county)
    return None


def create_county(token_info, body):
    if token_info['role'] != 'admin':
        abort(401, 'Unauthorized')

    new_county = County(body['county_name'])
    db.session.add(new_county)
    db.session.commit()
    return county_schema.dump(new_county)


def update_county(token_info, county_id, body):
    if token_info['role'] != 'admin':
        abort(401, 'Unauthorized')

    county = County.query.get(county_id)
    if county:
        county.county_name = body['county_name']
        db.session.commit()
        return county_schema.dump(county)
    return None


def delete_county(token_info, county_id):
    if token_info['role'] != 'admin':
        abort(401, 'Unauthorized')

    county = County.query.get(county_id)
    if county:
        db.session.delete(county)
        db.session.commit()
        return county_schema.dump(county)
    return None
