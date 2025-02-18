from .county_service import get_all_counties, get_county_by_id, create_county, update_county, delete_county
from .location_service import get_all_locations, get_location_by_id, create_location, update_location, delete_location
from .surface_type_service import get_all_surface_types, get_surface_type_by_id, create_surface_type, update_surface_type, delete_surface_type
from .route_type_service import get_all_route_types, get_route_type_by_id, create_route_type, update_route_type, delete_route_type
from .tag_service import get_all_tags, get_tag_by_id, create_tag, update_tag, delete_tag
from .user_service import get_all_users, get_user_by_id, create_user, update_user, delete_user
from .trail_service import get_all_trails, get_trail_by_id, create_trail, update_trail, delete_trail
from .auth_service import basic_auth, basic_auth_wrapper


def health():
    return {"message": "The server is working!"}, 200
