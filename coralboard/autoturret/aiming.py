"""
Coordinate Systems:
    1. Image coordinates.
        Top-left is 0,0, increases to right and down.
    2. World coordinate camera (forward is z, up is y, right is x). 
       Physical camera is origin. Directly in front of camera is forward.

    3. World coordinate gun (same handedness convention as above).
       Physical gun's axis of rotation is origin. Forward and up unit vector
       match with above unit vector. Ie, same as above, with a translation.
"""

# __all__ = ('run_aiming_pipeline', 'GunAngles')

import math
import collections
# from detect import *
from copy import copy

Point2D = collections.namedtuple('Point2D', ('x', 'y'))
Point3D = collections.namedtuple('Point3D', ('x', 'y', 'z'))
Point3D.__add__ = lambda self, other: Point3D(self.x + other.x, self.y + other.y, self.z + other.z)
Point3D.__sub__ = lambda self, other: Point3D(self.x - other.x, self.y - other.y, self.z - other.z)
# GunAngles = collections.namedtuple('GunAngles', ('pan', 'tilt'))

class GunAngles:
    def __init__(self, pan, tilt):
        self.pan = pan
        self.tilt = tilt
    def __str__(self):
        return "pan: %.2f, tilt: %.2f" % (self.pan, self.tilt)


def select_target(objects):
    """
    This functions takes a list of objects, and returns
    a point to target (reference frame image coordinates).
    Returns:
        None, or a Point2D
    """
    if len(objects) == 0:
        return None

    # For now, just hit middle of face, and one head below.
    target_object = objects[0]
    return Point2D(
        x = target_object.bbox.x + target_object.bbox.w / 2.0,
        y = target_object.bbox.y + target_object.bbox.h * 1.5
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
    #fov_y = 87.6
    fov_y = 84
    depth = 1 # TODO change to 2
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
    world_coordinate_point = Point3D(
        x=normalized_point.x * camera_view_physical_size.x,
        y=normalized_point.y * camera_view_physical_size.y,
        z=depth
    )
    return world_coordinate_point

def convert_to_rhs(point, angles):
    """
        We follow a LHS for coordinates, however for rotations
        we're a bit odd.
        Rotations are clockwise when axis pointed towards you
        We follow this convention for pan, ie positive turns right.
        However we don't follow this for tilt.
        TODO: make tilt LHS as well.

        To convert LHS to RHS, we negate the z axis, and negate
        the angles of rotation.
    """
    return (Point3D(x=point.x, y=point.y, z=-point.z),
            GunAngles(pan=-angles.pan, tilt=angles.tilt))

def convert_from_rhs(point, angles):
    return (Point3D(x=point.x, y=point.y, z=-point.z),
            GunAngles(pan=-angles.pan, tilt=angles.tilt))

def world_coordinate_camera_to_world_coordinate_base(point, current_camera_angles):
    """
    Note: rotations are currently not supported between the
    two reference frames 
    """
    gun_in_world_coordinate_camera = Point3D(
        x=0, y=0, z=0
    )

    point = point - gun_in_world_coordinate_camera

    point, current_camera_angles = convert_to_rhs(point, current_camera_angles)

    pan = math.radians(current_camera_angles.pan)
    tilt = math.radians(current_camera_angles.tilt)

    """
        General Rotation About X-Axis, RHS.
        1       0   0
        0   cos(b)  -sin(b)  
        0   sin(b) cos(b)  
        Source of original: 
        https://en.wikipedia.org/wiki/Rotation_matrix#General_rotations

        Comment this section out if camera tilt is stationary
    """
    point = Point3D(
        x = point.x,
        y = point.y * math.cos(tilt) + point.z * -math.sin(tilt),
        z = point.y * math.sin(tilt) + point.z * math.cos(tilt)
    )
    
    """
        Pan Calc:
        General Rotation about Y-Axis, RHS.
        cos(a)  0       sin(a)
        0       1       0
        -sin(a)  0       cos(a)
    """
    point = Point3D(
        x = point.x * math.cos(pan) + point.z * math.sin(pan),
        y = point.y,
        z = point.x * -math.sin(pan) + point.z * math.cos(pan)
    )

    point, _ = convert_from_rhs(point, current_camera_angles)

    return point

def world_coordinate_gun_to_gun_angles(point):
    """
        pan=atan2(z,x); tilt=atan2(y, hypot(x,z))

    """
    return GunAngles(
        pan=math.degrees(math.atan2(point.x, point.z)),
        tilt=math.degrees(math.atan2(point.y, math.hypot(point.x, point.z)))
    )

def fine_tune(src, target, amt):
    """
    delta = 10 * math.pow((target - src) / 10, 2)
    delta = math.copysign(delta, target - src)
    max_step = abs(target-src) / 2
    clamped_delta = max(min(delta, max_step), -max_step)
    return src + clamped_delta
    """
    return src + (target - src) / amt


def fine_tune_aiming(current_angles, target_angles):
    tuned_angles = copy(current_angles)
    tuned_angles.pan = fine_tune(current_angles.pan, target_angles.pan, 4)
    tuned_angles.tilt = fine_tune(current_angles.tilt, target_angles.tilt, 15)
    return tuned_angles 

    """
    if (abs(target_angles-current_angles%360) > 180): # wrap around
        if target_angles < 0: # eg, 150->-150, needs+60 instead.
            add = 360 - current_angles + target_angles
        if target_angles > 0: # eg, -150->150, need-60 instead.
            add = -(360 + current_angles - target_angles)
    """


def run_aiming_pipeline(objects, current_gun_angles):
    # print (objects)
    target = select_target(objects)
    if target == None:
        return None

    # Camera angles currently are gun pan, but not tilt.
    current_camera_angles = copy(current_gun_angles)
    # current_camera_angles.tilt += 20
    # current_camera_angles.pan = 90

    point = image_coordinate_to_world_coordinate_camera(target)

    print ("Current gun angle", current_gun_angles)
    print ("Coordinate frame of ref of camera", point)
    point = world_coordinate_camera_to_world_coordinate_base(point, current_camera_angles)
    print ("Coordinate frame of ref of base", point)
    angles = world_coordinate_gun_to_gun_angles(point)
    angles = fine_tune_aiming(current_gun_angles, angles)
    # angles.tilt -= 20

    return angles



