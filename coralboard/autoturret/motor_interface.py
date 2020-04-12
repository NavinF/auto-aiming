import serial
from . aiming import GunAngles
import time

UPDATE_FREQUENCY = 50.0

last_update_time = time.monotonic()
ser = None

current_gun_angles = GunAngles(pan=0,tilt=0)

def get_serial():
    global ser
    # return None #TODO remove

    # TTY failed, don't retry
    if ser == -1:
        return None

    # Try opening ACM0 or ACM1
    if ser is None:
        try:
            ser = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=0.02, write_timeout=0.1)
            print("Opening ACM0")
        except:
            try:
                ser = serial.Serial('/dev/ttyACM1', baudrate=115200, timeout=0.02, write_timeout=0.1)
                print("Opening ACM1")
            except:
                print("Unable to open TTY")
                ser = -1
                raise Exception()
                return None

    # Ser is valid, return it.
    return ser


def update():
    global current_gun_angles
    ser = get_serial()
    if ser is None:
        return

    while ser.in_waiting > 0:
        start = time.time()
        s = ser.readline().decode().split(" ")
        if len(s) != 2:
            continue

        key = s[0]
        value = s[1]
        if key == "pan_angle":
            current_gun_angles.pan = float(value)
            # print ("setting pan to", float(value), "string is", value)
        elif key == "tilt_angle":
            current_gun_angles.tilt = float(value)

def get_current_gun_angles():
    global current_gun_angles
    return current_gun_angles


def set_pan_tilt(angles):
    """Takes a gun angles. Drops updates that happen faster
        than UPDATE_FREQUENCY.
    """
    global last_update_time
    ser = get_serial()

    # No tty.
    if ser is None:
        return

    try:
        if (time.monotonic() - last_update_time > 1/UPDATE_FREQUENCY):
            ser.write('sp{0:.2f}\n'.format(angles.pan).encode())
            ser.write('st{0:.2f}\n'.format(max(0, angles.tilt)).encode())
            last_update_time = time.monotonic()
    except:
        print('Warning: write timeout to motor, skipping')