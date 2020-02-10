from . import aiming
from . import motor_interface

def run(objects):
    gun_angles = aiming.run_aiming_pipeline(objects)
    if not gun_angles:
        return None

    motor_interface.set_pan_tilt(gun_angles)

    return {'gun_angles': gun_angles}

def render(render_artifacts, lines):
    if render_artifacts:
        if 'gun_angles' in render_artifacts:
            gun_angles = render_artifacts['gun_angles']
            lines.append(
                'Gun Angles: pan: %.2f, tilt: %.2f' % (gun_angles.pan, gun_angles.tilt)
            )