"""
Run with python3 aiming_test.py -v
"""
import unittest
from aiming import *

# Since not in package, include parent dir in path to import
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

"""
TODO:
    * test when it goes past 90 degrees up, does it rotate around?
"""

from detect import Object, BBox

class AimingUnitTest(unittest.TestCase):
    def test_rotate(self):
        current_camera_angles = GunAngles(pan=90, tilt=0)
        point_in_camera_ref = Point3D(x=0,y=0,z=1)
        expected_point_in_base = Point3D(x=1,y=0,z=0)

    # TODO: switch these tests to use aiming pipeline instead of
    # each function individually.
    def test_target_in_right_of_camera_moves_gun_clockwise(self):
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
            point_in_base = world_coordinate_camera_to_world_coordinate_base(point_in_camera_ref, angles)
            new_angles = world_coordinate_gun_to_gun_angles(point_in_base)
            self.assertGreater(new_angles.pan, angles.pan)
            angles = new_angles
            print ("resulting angles", angles)


    def test_target_in_left_of_camera_moves_gun_counterclockwise(self):
        """
        Test x=-1 (angles should decrease)
        x=1, angles should increase
        x=0, angles hold steady.
        """
        point_in_camera_ref = Point3D(x=-1,y=0,z=2)
        angles = GunAngles(pan=45, tilt=20) # TODO: test wrap around
        for i in range(5):
            point_in_base = world_coordinate_camera_to_world_coordinate_base(point_in_camera_ref, angles)
            # print ("point_in_base", point_in_base)
            new_angles = world_coordinate_gun_to_gun_angles(point_in_base)
            self.assertLess(new_angles.pan, angles.pan)
            angles = new_angles
            print ("resulting angles", angles)


    def test_target_in_center_gun_doesnt_move(self):
        point_in_camera_ref = Point3D(x=0,y=0,z=2)
        angles = GunAngles(pan=90, tilt=20)
        for i in range(5):
            point_in_base = world_coordinate_camera_to_world_coordinate_base(point_in_camera_ref, angles)
            #print ("point_in_base", point_in_base)
            angles = world_coordinate_gun_to_gun_angles(point_in_base)
            print ("resulting angles", angles)
        self.assertEqual(angles.pan, 90)
        self.assertEqual(angles.tilt, 20)

    def helper_test_aiming_pipeline(self, image_x, image_y):
        print("Testing with image coord", image_x, image_y)
        objs = [Object(id=1, label=1, score=1,
            bbox=BBox(x=image_x, y=image_y, w=0, h=0))]
        angles = GunAngles(pan=0, tilt=0)
        for i in range(5):
            new_angles = run_aiming_pipeline(objs, angles)
            print ("resulting angles", new_angles)

            if image_x < 0.5:
                self.assertLess(new_angles.pan, angles.pan)
            elif image_x > 0.5:
                self.assertGreater(new_angles.pan, angles.pan)
            else:
                self.assertEqual(new_angles.pan, angles.pan)
            if image_y < 0.5: # goes up
                self.assertGreater(new_angles.tilt, angles.tilt)
            elif image_y > 0.5:
                self.assertLess(new_angles.tilt, angles.tilt)
            else:
                self.assertEqual(new_angles.tilt, angles.tilt)
            angles = new_angles

    def test_center(self):
        self.helper_test_aiming_pipeline(0.5, 0.5)
    def test_up(self):
        self.helper_test_aiming_pipeline(0.5, 0.4)
    def test_down(self):
        self.helper_test_aiming_pipeline(0.5, 0.6)
    def test_left(self):
        self.helper_test_aiming_pipeline(0.4, 0.5)
    def test_right(self):
        self.helper_test_aiming_pipeline(0.6, 0.5)
    
    def test_left_up(self):
        self.helper_test_aiming_pipeline(0.4, 0.4)
    def test_left_down(self):
        self.helper_test_aiming_pipeline(0.4, 0.6)
    def test_right_up(self):
        self.helper_test_aiming_pipeline(0.6, 0.4)
    def test_right_down(self):
        self.helper_test_aiming_pipeline(0.6, 0.6)
    """
    #TODO: Hmm can I test a series of movements? Ie have motor in the loop?
    # 
    # Ok so without tilt, looks ok. 
    # There's the overflow problem from -170 to 160.
    
    test_left_down (__main__.AimingUnitTest) ... Testing with image coord 0.4 0.6
    Current gun angle pan: 0.00, tilt: 0.00
    Coordinate frame of ref of camera Point3D(x=-0.3601616177191359, y=-0.3601616177191359, z=2)
    Coordinate frame of ref of base Point3D(x=-0.3601616177191359, y=-0.3601616177191359, z=2.0)
    resulting angles pan: -10.21, tilt: -10.05
    Current gun angle pan: -10.21, tilt: -10.05
    Coordinate frame of ref of camera Point3D(x=-0.3601616177191359, y=-0.3601616177191359, z=2)
    Coordinate frame of ref of base Point3D(x=-0.6351899882325995, y=-0.47834905113958903, z=1.904507454928716)
    resulting angles pan: -16.99, tilt: -11.17
    Current gun angle pan: -16.99, tilt: -11.17

    this sequence is weird. Tilt should move in angles as much as pan.

    found testing test_left_down works well.
    RHS vs LHS.
    https://www.evl.uic.edu/ralph/508S98/coordinates.html
    rotation is swapped ()
    wait huh. it looks like only z is negated.?
    try that.
    """

    def helper_test_fine_tune(self, src, target):
        new_angles = fine_tune_aiming(src, target)
        pan_delta = new_angles.pan - src.pan
        tilt_delta = new_angles.tilt - src.tilt
        max_expected_pan = (target.pan - src.pan) / 2
        max_expected_tilt = (target.tilt - src.tilt) / 2

        if pan_delta < 0:
            self.assertGreaterEqual(new_angles.pan, max_expected_pan)
        elif pan_delta > 0:
            self.assertLessEqual(new_angles.pan, max_expected_pan)
        else:
            self.assertEqual(new_angles.pan, 0)
        if tilt_delta < 0:
            self.assertGreaterEqual(new_angles.tilt, max_expected_tilt)
        elif tilt_delta > 0:
            self.assertLessEqual(new_angles.tilt, max_expected_tilt)
        else:
            self.assertEqual(new_angles.tilt, 0)

    def test_fine_tune(self):
        self.helper_test_fine_tune(
            GunAngles(pan=10,tilt=0),
            GunAngles(pan=0,tilt=5))
        self.helper_test_fine_tune(
            GunAngles(pan=5,tilt=10),
            GunAngles(pan=0,tilt=0))
        self.helper_test_fine_tune(
            GunAngles(pan=0,tilt=0),
            GunAngles(pan=5,tilt=10))
        self.helper_test_fine_tune(
            GunAngles(pan=0,tilt=5),
            GunAngles(pan=10,tilt=0))
        

    #TODO src/target arg swapped
    def old_test_fine_tune(self):
        self.assertGreater(
            fine_tune_aiming(
                GunAngles(pan=10,tilt=0),
                GunAngles(pan=0,tilt=0)
            ).pan, 5)
        self.assertGreater(
            fine_tune_aiming(
                GunAngles(pan=5,tilt=0),
                GunAngles(pan=0,tilt=0)
            ).pan, 3)
        self.assertGreater(
            fine_tune_aiming(
                GunAngles(pan=2,tilt=0),
                GunAngles(pan=0,tilt=0)
            ).pan, 1.7)
        self.assertGreater(
            fine_tune_aiming(
                GunAngles(pan=20,tilt=0), 
                GunAngles(pan=0,tilt=0)
            ).pan, 15)
        self.assertLess(
            fine_tune_aiming(
                GunAngles(pan=0,tilt=0),
                GunAngles(pan=10,tilt=0)
            ).pan, 5)
        self.assertLess(
            fine_tune_aiming(
                GunAngles(pan=0,tilt=0),
                GunAngles(pan=5,tilt=0) 
            ).pan, 2)
        self.assertLess(
            fine_tune_aiming(
                GunAngles(pan=0,tilt=0),
                GunAngles(pan=2,tilt=0) 
            ).pan, 0.5)


if __name__ == "__main__":
    unittest.main()