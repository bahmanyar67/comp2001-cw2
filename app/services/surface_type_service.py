from app.models import SurfaceType, SurfaceTypeSchema
from app.extensions import db

surface_type_schema = SurfaceTypeSchema()
surface_types_schema = SurfaceTypeSchema(many=True)


def get_all_surface_types():
    surface_types = SurfaceType.query.all()
    return surface_types_schema.dump(surface_types)


def get_surface_type_by_id(surface_type_id):
    surface_type = SurfaceType.query.get(surface_type_id)
    if surface_type:
        return surface_type_schema.dump(surface_type)
    return None


def create_surface_type(body):
    new_surface_type = SurfaceType(body['surface_type_name'])
    db.session.add(new_surface_type)
    db.session.commit()
    return surface_type_schema.dump(new_surface_type)


def update_surface_type(surface_type_id, body):
    surface_type = SurfaceType.query.get(surface_type_id)
    if surface_type:
        surface_type.surface_type_name = body['surface_type_name']
        db.session.commit()
        return surface_type_schema.dump(surface_type)
    return None


def delete_surface_type(surface_type_id):
    surface_type = SurfaceType.query.get(surface_type_id)
    if surface_type:
        db.session.delete(surface_type)
        db.session.commit()
        return surface_type_schema.dump(surface_type)
    return None
