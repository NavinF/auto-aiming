from . import aiming
from . import motor_interface
import time

last_update_time = time.monotonic()

def run(objects):
    motor_interface.update()

    current_gun_angles = motor_interface.get_current_gun_angles()

    gun_angles = aiming.run_aiming_pipeline(objects, current_gun_angles)
    if not gun_angles:
        return None

    motor_interface.set_pan_tilt(gun_angles)

    return {
        'gun_angles': gun_angles,
        'fps': update_fps()
    }

def update_fps():
    global last_update_time

    current_time = time.monotonic()
    elapsed_time = current_time - last_update_time
    last_update_time = current_time

    return 1.0 / elapsed_time


def render(render_artifacts, lines):
    if render_artifacts is None:
        return

    if 'gun_angles' in render_artifacts:
        gun_angles = render_artifacts['gun_angles']
        lines.append(
            'Gun Angles: pan: %.2f, tilt: %.2f' % (gun_angles.pan, gun_angles.tilt)
        )
    if 'fps' in render_artifacts:
        fps = render_artifacts['fps']
        lines.append(
            'E2E FPS: %.2f' % (fps)
        )