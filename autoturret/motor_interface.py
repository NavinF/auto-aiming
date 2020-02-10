import serial
import time

UPDATE_FREQUENCY = 50.0

last_update_time = time.monotonic()
ser = None

def set_pan_tilt(angles):
    """Takes a gun angles. Drops updates that happen faster
        than UPDATE_FREQUENCY.
    """
    global last_update_time
    global ser

    # TTY failed, don't retry.
    if ser == -1:
        return

    try:
        if ser is None:
            ser = serial.Serial('/dev/ttyACM0')

        if (time.monotonic() - last_update_time > 1/UPDATE_FREQUENCY):
            ser.write('sp{0:.2f}\n'.format(angles.pan).encode())
            ser.write('st{0:.2f}\n'.format(max(0, angles.tilt)).encode())
            last_update_time = time.monotonic()
            print("Updating motor controller")
    except:
        print("Unable to open TTY")
        ser = -1
        pass