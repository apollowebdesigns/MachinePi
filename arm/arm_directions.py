class ArmDirections(object):
    bicep_length = 90
    fore_arm_len = 60
    wrist_len = 48
    hand_len = 105

    simple_arm_len = fore_arm_len + wrist_len + hand_len

    height_sum_angles_deg = 540

    @staticmethod
    def start_base_clockwise():
        return [0, 1, 0]  # Rotate base anti-clockwise

    @staticmethod
    def start_base_anticlockwise():
        return [0, 2, 0]  # Rotate base anti-clockwise

    @staticmethod
    def base_clockwise():
        return [0, 1, 0]  # Rotate base anti-clockwise

    @staticmethod
    def base_anticlockwise():
        return [0, 2, 0]  # Rotate base clockwise

    @staticmethod
    def up():
        return [64, 0, 0]  # Shoulder up

    @staticmethod
    def down():
        return [128, 0, 0]  # Shoulder down

    @staticmethod
    def elbow_up():
        return [16, 0, 0]  # Elbow up

    @staticmethod
    def elbow_down():
        return [32, 0, 0]  # Elbow down

    @staticmethod
    def wrist_up():
        return [4, 0, 0]  # Wrist up

    @staticmethod
    def wrist_down():
        return [8, 0, 0]  # Wrist down

    @staticmethod
    def gripopen():
        return [2, 0, 0]  # Grip open

    @staticmethod
    def grip_close():
        return [1, 0, 0]  # Grip close

    @staticmethod
    def light_on():
        return [0, 0, 1]  # Light on

    @staticmethod
    def light_off():
        return [0, 0, 0]  # Light off
