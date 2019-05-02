# import the USB and Time librarys into Python

import time
import usb.core
import usb.util

# Allocate the name 'RoboArm' to the USB device
from methods import degrees_to_seconds


def get_robot_arm():
    return usb.core.find(idVendor=0x1267, idProduct=0x1)


RoboArm = get_robot_arm()

# Check if the arm is detected and warn if not
if RoboArm is None:
    raise ValueError("Arm not found")

# Create a variable for duration
Duration = 1


# Define a procedure to execute each movement
def move_arm(angle, arm_cmd, reverse_arm_cmd):
    # Start the movement
    return __control_arm(angle, arm_cmd) if degrees_to_seconds(angle) >= 0 else __control_arm(angle, reverse_arm_cmd)


def __control_arm(angle, arm_cmd):
    RoboArm.ctrl_transfer(0x40, 6, 0x100, 0, arm_cmd, 3)
    # Stop the movement after waiting a specified duration
    time.sleep(abs(degrees_to_seconds(angle)))
    arm_cmd = [0, 0, 0]
    RoboArm.ctrl_transfer(0x40, 6, 0x100, 0, arm_cmd, 3)
