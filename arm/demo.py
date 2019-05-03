import numpy as np

from arm.arm_directions import ArmDirections
from arm.move_arm import move_arm
import arm.Arm

default_arm_positions = [np.pi/2, np.pi/2, 0]

## create the robot arm
arm = Arm.Arm3Link(q=default_arm_positions, L=np.array([90, 60, 48]))

print('the old angles are:')
print(arm.q)
print(arm.get_xy())

old_angles = default_arm_positions

# x, y = -100, 80

x, y = -70, 0

arm.q = arm.inv_kin([x, y])

new_angles = arm.q

print('new angle is:')
print(arm.q)
print(arm.get_xy())


move_arm(old_angles[0] - new_angles[0], ArmDirections.up(), ArmDirections.down())
move_arm(old_angles[1] - new_angles[1], ArmDirections.elbow_up(), ArmDirections.elbow_down())
move_arm(old_angles[2] - new_angles[2], ArmDirections.wrist_up(), ArmDirections.wrist_down())

move_arm(old_angles[0] - new_angles[0], ArmDirections.down(), ArmDirections.up())
move_arm(old_angles[1] - new_angles[1], ArmDirections.elbow_down(), ArmDirections.elbow_up())
move_arm(old_angles[2] - new_angles[2], ArmDirections.wrist_down(), ArmDirections.wrist_up())



# rad_angle = math.acos((18**2 - ArmDirections.bicep_length**2 - ArmDirections.simple_arm_len**2)/(-1 * ArmDirections.bicep_length * ArmDirections.simple_arm_len))
# print(rad_angle)