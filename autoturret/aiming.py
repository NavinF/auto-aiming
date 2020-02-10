"""
Coordinate Systems:
    1. Image coordinates.
    2. World coordinate camera (forward is z, up is y, right is x). 
       Physical camera is origin. Directly in front of camera is forward.

    3. World coordinate gun (same handedness convention as above).
       Physical gun's axis of rotation is origin. Forward and up unit vector
       match with above unit vector. Ie, same as above, with a translation.
"""

__all__ = ('run_aiming_pipeline', 'GunAngles')

import math
import collections
from detect import *

Point2D = collections.namedtuple('Point2D', ('x', 'y'))
Point3D = collections.namedtuple('Point3D', ('x', 'y', 'z'))
Point3D.__add__ = lambda self, other: Point3D(self.x + other.x, self.y + other.y, self.z + other.z)
GunAngles = collections.namedtuple('GunAngles', ('pan', 'tilt'))

def select_target(objects):
    """
    This functions takes a list of objects, and returns
    a point to target (reference frame image coordinates).
    Returns:
        None, or a Point2D
    """
    if len(objects) == 0:
        return None

    # For now, just hit middle of face.
    target_object = objects[0]
    return Point2D(
        x = target_object.bbox.x + target_object.bbox.w / 2.0,
        y = target_object.bbox.y + target_object.bbox.h / 2.0
    )


def image_coordinate_to_world_coordinate_camera(point):
    """
    These specs are for the coral camera.
    https://coral.ai/docs/camera/datasheet/
    FOV: 84, 87.6.
    opposite/distance = tan(84/2)
    opposite = distance * tan(84/2)
    camera_width = 2 * opposite
    For us, we get 2.7 opposite at 3m, for total of 5.4
    Returns:
        Point3D in reference frame of physical camera.
    """
    fov_x = 84
    fov_y = 87.6
    depth = 3
    camera_view_physical_size = Point2D(
        x = 2 * depth * math.tan(math.radians(fov_x / 2.0)),
        y = 2 * depth * math.tan(math.radians(fov_y / 2.0))
    )

    # TODO: parse the image/width from somewhere.
    # Right now it's in apps.py, 640x480
    """
    image_resolution = Point2D(x=640, y=480)
    normalized_point = Point2D(
        x=point.x / image_resolution.x,
        y=point.y / image_resolution.y
    )
    """
    # Apparently we already get normalized point.
    # Just shift origin to center of image.
    # Also shift y to point up.
    normalized_point = Point2D(
        x=point.x - 0.5,
        y=(1-point.y) - 0.5
    )
    print("normalized_point: {0}".format(normalized_point))
    world_coordinate_point = Point3D(
        x=normalized_point.x * camera_view_physical_size.x,
        y=normalized_point.y * camera_view_physical_size.y,
        z=depth
    )
    return world_coordinate_point

def world_coordinate_camera_to_world_coordinate_gun(point):
    """
    Note: rotations are currently not supported between the
    two reference frames 
    """
    gun_coordinate_in_world_coordinate_camera = Point3D(
        x=0, y=0, z=0
    )
    return point + gun_coordinate_in_world_coordinate_camera

def world_coordinate_gun_to_gun_angles(point):
    """
        pan=atan2(z,x); tilt=atan2(y, hypot(x,z))

    """
    return GunAngles(
        pan=math.degrees(math.atan2(point.x, point.z)),
        tilt=math.degrees(math.atan2(point.y, math.hypot(point.x, point.z)))
    )

def run_aiming_pipeline(objects):
    print (objects)
    target = select_target(objects)
    if target == None:
        return None

    point = image_coordinate_to_world_coordinate_camera(target)
    point = world_coordinate_camera_to_world_coordinate_gun(point)
    angles = world_coordinate_gun_to_gun_angles(point)

    print (point)
    print (angles)
    return angles



