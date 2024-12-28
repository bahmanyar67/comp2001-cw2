from app.models import County, CountySchema
from app.extensions import db

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


def create_county(body):
    new_county = County(body['county_name'])
    db.session.add(new_county)
    db.session.commit()
    return county_schema.dump(new_county)


def update_county(county_id, body):
    county = County.query.get(county_id)
    if county:
        county.county_name = body['county_name']
        db.session.commit()
        return county_schema.dump(county)
    return None


def delete_county(county_id):
    county = County.query.get(county_id)
    if county:
        db.session.delete(county)
        db.session.commit()
        return county_schema.dump(county)
    return None
