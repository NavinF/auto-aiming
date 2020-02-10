auto turret read me.

function 1.
* takes image, returns estimated 3d coordinate in reference frame of camera (camera is at origin). can change to any other fixed point later if we decide to make camera move.
* to start, will use fixed depth=3m.

another function, takes 3d coordinate in reference frame of camera, transforms to reference frame of gun nozzle (should be just a position delta) and returns pan tilt.

another function takes pan tilt and sends to servo controller.




sudo sshfs -o allow_other mendel@10.0.0.87:/ /mnt/coral
(note it's using root's ssh keys. can copy my keys to root. or add self to fuse group).

pushd /usr/lib/python3/dist-packages/edgetpuvision

export TEST_DATA=${HOME}/demo_files
python3 -m edgetpuvision.detect_server \
  --model ${TEST_DATA}/mobilenet_ssd_v2_face_quant_postprocess_edgetpu.tflite

18 cm behind. 10cm below.
