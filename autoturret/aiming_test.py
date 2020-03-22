from aiming import *

def test_rotate():
    current_camera_angles = GunAngles(pan=90, tilt=0)
    point_in_camera_ref = Point3D(x=0,y=0,z=1)
    expected_point_in_base = Point3D(x=1,y=0,z=0)

def test_target_in_right_of_camera_moves_gun_clockwise():
    # expected_point_in_base = Point(x=2,y=0,z=1)
    # x = z,
    # z = -x
    """
    Test x=-1 (angles should decrease)
    x=1, angles should increase
    x=0, angles hold steady.
    """
    point_in_camera_ref = Point3D(x=1,y=0,z=2)
    angles = GunAngles(pan=45, tilt=20) # TODO: test wrap around
    for i in range(5):
        # print ("starting point:", point_in_camera_ref)
        # print ("starting angles", angles)

        point_in_base = world_coordinate_camera_to_world_coordinate_base(point_in_camera_ref, angles)
        # print ("point_in_base", point_in_base)
        new_angles = world_coordinate_gun_to_gun_angles(point_in_base)
        assert_ge(new_angles.pan, angles.pan)
        angles = new_angles
        print ("resulting angles", angles)
        

def test_target_in_center_gun_doesnt_move():
    point_in_camera_ref = Point3D(x=0,y=0,z=2)
    angles = GunAngles(pan=90, tilt=20)
    for i in range(5):
        #print ("starting point:", point_in_camera_ref)
        #print ("starting angles", angles)

        point_in_base = world_coordinate_camera_to_world_coordinate_base(point_in_camera_ref, angles)
        #print ("point_in_base", point_in_base)
        angles = world_coordinate_gun_to_gun_angles(point_in_base)
        print ("resulting angles", angles)
    assert_eq(angles.pan, 90)
    assert_eq(angles.tilt, 0)

#TODO src/target arg swapped
def test_fine_tune():
    assert_eq(
        fine_tune_aiming(
            GunAngles(pan=0,tilt=0),
            GunAngles(pan=20,tilt=0)
        ).pan,
        0)
    assert_ge(
        fine_tune_aiming(
            GunAngles(pan=0,tilt=0),
            GunAngles(pan=10,tilt=0)
        ).pan,
        5)
    assert_ge(
        fine_tune_aiming(
            GunAngles(pan=0,tilt=0),
            GunAngles(pan=5,tilt=0)
        ).pan,
        3)
    assert_ge(
        fine_tune_aiming(
            GunAngles(pan=0,tilt=0),
            GunAngles(pan=2,tilt=0)
        ).pan,
        1.7)
    assert_ge(
        fine_tune_aiming(
            GunAngles(pan=20,tilt=0), 
            GunAngles(pan=0,tilt=0)
        ).pan,
        15)
    assert_le(
        fine_tune_aiming(
            GunAngles(pan=10,tilt=0), 
            GunAngles(pan=0,tilt=0)
        ).pan,
        9)
    assert_le(
        fine_tune_aiming(
            GunAngles(pan=5,tilt=0), 
            GunAngles(pan=0,tilt=0)
        ).pan,
        2)
    assert_le(
        fine_tune_aiming(
            GunAngles(pan=2,tilt=0), 
            GunAngles(pan=0,tilt=0)
        ).pan,
        0.5)


def assert_eq(a, b):
    if not abs(a-b)<0.001:
        print("ASSERT_EQ FAILED: {0}=={1}".format(a,b))
        assert False

def assert_ge(a, b):
    if not a>b:
        print("ASSERT_GE FAILED: {0}>{1}".format(a,b))
        assert False

def assert_le(a, b):
    if not a<b:
        print("ASSERT_GE FAILED: {0}<{1}".format(a,b))
        assert False

def main():
    test_target_in_right_of_camera_moves_gun_clockwise()
    test_target_in_center_gun_doesnt_move()
    test_fine_tune()


if __name__ == "__main__":
    main()