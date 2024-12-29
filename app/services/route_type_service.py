from app.models import RouteType, RouteTypeSchema
from app.extensions import db

route_type_schema = RouteTypeSchema()
route_types_schema = RouteTypeSchema(many=True)


def get_all_route_types():
    route_types = RouteType.query.all()
    return route_types_schema.dump(route_types)


def get_route_type_by_id(route_type_id):
    route_type = RouteType.query.get(route_type_id)
    if route_type:
        return route_type_schema.dump(route_type)
    return None


def create_route_type(body):
    new_route_type = RouteType(body['route_type_name'])
    db.session.add(new_route_type)
    db.session.commit()
    return route_type_schema.dump(new_route_type)


def update_route_type(route_type_id, body):
    route_type = RouteType.query.get(route_type_id)
    if route_type:
        route_type.route_type_name = body['route_type_name']
        db.session.commit()
        return route_type_schema.dump(route_type)
    return None


def delete_route_type(route_type_id):
    route_type = RouteType.query.get(route_type_id)
    if route_type:
        db.session.delete(route_type)
        db.session.commit()
        return route_type_schema.dump(route_type)
    return None
