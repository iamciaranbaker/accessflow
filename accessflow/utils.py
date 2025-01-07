from accessflow.models.permission_type import PermissionType
from accessflow.models.permission import Permission

def get_permission_type_by_id(id):
    """
    Retrieve a PermissionType object by its ID.

    Parameters:
      id (int): The unique identifier of the PermissionType to retrieve.

    Returns:
      PermissionType: A PermissionType object, or None if one was not found.
    """
    return PermissionType.query.filter_by(id = id).first()

def get_permission_type_by_name(name):
    """
    Retrieve a PermissionType object by its name.

    Parameters:
      name (str): The unique name of the PermissionType to retrieve.

    Returns:
      PermissionType: A PermissionType object, or None if one was not found.
    """
    return PermissionType.query.filter_by(name = name).first()

def get_permission_by_id(id):
    """
    Retrieve a Permission object by its ID.

    Parameters:
      id (int): The unique identifier of the Permission to retrieve.

    Returns:
      Permission: A Permission object, or None if one was not found.
    """
    return Permission.query.filter_by(id = id).first()

def get_permission_by_name(name):
    """
    Retrieve a Permission object by its name.

    Parameters:
      name (str): The unique name of the Permission to retrieve.

    Returns:
      Permission: A Permission object, or None if one was not found.
    """
    return Permission.query.filter_by(name = name).first()