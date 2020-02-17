from aiming import *

def test_rotate():
    current_camera_angles = GunAngles(pan=90, tilt=0)
    point_in_camera_ref = Point3D(x=0,y=0,z=1)
    expected_point_in_base = Point3D(x=1,y=0,z=0)

def test_rotate_2():
    # expected_point_in_base = Point(x=2,y=0,z=1)
    # x = z,
    # z = -x
    """
    Test x=-1 (angles should decrease)
    x=1, angles should increase
    x=0, angles hold steady.
    """
    point_in_camera_ref = Point3D(x=0,y=0,z=2)
    angles = GunAngles(pan=90, tilt=0)
    for i in range(5):
        print ("starting point:", point_in_camera_ref)
        print ("starting angles", angles)

        point_in_base = world_coordinate_camera_to_world_coordinate_base(point_in_camera_ref, angles)
        print ("point_in_base", point_in_base)
        angles = world_coordinate_gun_to_gun_angles(point_in_base)
        print ("resulting angles", angles)

def main():
    test_rotate_2()


if __name__ == "__main__":
    main()