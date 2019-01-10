# import the USB and Time librarys into Python
import usb.core, usb.util, time

# Allocate the name 'RoboArm' to the USB device
RoboArm = usb.core.find(idVendor=0x1267, idProduct=0x1)

# Check if the arm is detected and warn if not
if RoboArm is None:
    raise ValueError("Arm not found")

# Create a variable for duration
Duration = 0.5


# Define a procedure to execute each movement
def MoveArm(Duration, ArmCmd):
    # Start the movement
    RoboArm.ctrl_transfer(0x40, 6, 0x100, 0, ArmCmd, 3)
    # Stop the movement after waiting a specified duration
    time.sleep(Duration)
    ArmCmd = [0, 0, 0]
    RoboArm.ctrl_transfer(0x40, 6, 0x100, 0, ArmCmd, 3)


def StartArm(ArmCmd):
    RoboArm.ctrl_transfer(0x40, 6, 0x100, 0, ArmCmd, 3)


def StopArm():
    ArmCmd = [0, 0, 0]
    RoboArm.ctrl_transfer(0x40, 6, 0x100, 0, ArmCmd, 3)