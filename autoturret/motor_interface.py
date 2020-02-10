import serial
import time

UPDATE_FREQUENCY = 50.0

last_update_time = time.monotonic()

def set_pan_tilt(angles, ser=serial.Serial('/dev/ttyACM0')):
    """Takes a gun angles. Drops updates that happen faster
        than UPDATE_FREQUENCY.
    """
    global last_update_time

    if (time.monotonic() - last_update_time > 1/UPDATE_FREQUENCY):
        ser.write('sp{0:.2f}\n'.format(angles.pan).encode())
        ser.write('st{0:.2f}\n'.format(max(0, angles.tilt)).encode())
        last_update_time = time.monotonic()
        print("Updating motor controller")