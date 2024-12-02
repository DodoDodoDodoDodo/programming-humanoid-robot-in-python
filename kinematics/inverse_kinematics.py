"""In this exercise you need to implement inverse kinematics for NAO's legs

* Tasks:
    1. solve inverse kinematics for NAO's legs by using analytical or numerical method.
       You may need documentation of NAO's leg:
       http://doc.aldebaran.com/2-1/family/nao_h21/joints_h21.html
       http://doc.aldebaran.com/2-1/family/nao_h21/links_h21.html
    2. use the results of inverse kinematics to control NAO's legs (in InverseKinematicsAgent.set_transforms)
       and test your inverse kinematics implementation.
"""

from forward_kinematics import ForwardKinematicsAgent
from numpy.matlib import identity


class InverseKinematicsAgent(ForwardKinematicsAgent):
    def inverse_kinematics(self, effector_name, transform):
        """solve the inverse kinematics

        :param str effector_name: name of end effector, e.g. LLeg, RLeg
        :param transform: 4x4 transform matrix
        :return: list of joint angles
        """
        joint_angles = []
        # YOUR CODE HERE
        from math import atan2, acos, sin, cos, sqrt

        pos = transform[:3, 3]
        is_left = effector_name == "LLeg"
        certify_is_left = effector_name == "RLeg"  # fixed typo
        if is_left and certify_is_left:
            print("effector_name is both")
        elif is_left and not certify_is_left:
            print("effector_name is left")
        elif not is_left and certify_is_left:
            print("effector_name is right")
        elif not is_left and not certify_is_left:
            print("effector_name  is neither")
        else:
            print(
                f"effector_name is cursed, {effector_name=}, {certify_is_left=}, {is_left=}"
            )
        sign = 1 if is_left else -1

        # roll left/right. the easy one.
        # pitch up/down. The one that kills your pilot.
        # yaw left/right. The one you don't technically need in a plane.
        # HipYawPitch, HipRoll, HipPitch, KneePitch, AnklePitch, AnkleRoll

        target = pos.copy()
        target[1] -= sign * 0.050  # HipOffsetY
        target[2] += 0.085  # HipOffsetZ

        # Angles
        q1 = 0  # HipYawPitch
        q2 = atan2(target[1], -target[2])  # HipRoll

        leg_length = sqrt(sum(target**2))
        cos_knee = (leg_length**2 - 0.1**2 - 0.1029**2) / (2 * 0.100 * 0.1029)
        q4 = acos(min(1, max(-1, cos_knee)))  # KneePitch

        q3 = -atan2(target[0], sqrt(target[1] ** 2 + target[2] ** 2)) - atan2(
            0.1029 * sin(q4), 0.100 + 0.1029 * cos(q4)
        )  # HipPitch

        q5 = -q3 - q4  # AnklePitch
        q6 = -q2  # AnkleRoll

        if is_left:
            prefic = "L"
        else:
            prefix = "R"

        joint_angles = [
            (f"{prefix}HipYawPitch", q1),
            (f"{prefix}HipRoll", sign * q2),
            (f"{prefix}HipPitch", q3),
            (f"{prefix}KneePitch", q4),
            (f"{prefix}AnklePitch", q5),
            (f"{prefix}AnkleRoll", sign * q6),
        ]
        return joint_angles

    def set_transforms(self, effector_name, transform):
        """solve the inverse kinematics and control joints use the results"""
        # YOUR CODE HERE
        angles = self.inverse_kinematics(effector_name, transform)
        self.keyframes = (
            [1.0] * len(angles),  # times
            [angle[0] for angle in angles],  # names
            [angle[1] for angle in angles],  # values
        )
        self.keyframes = ([], [], [])  # the result joint angles have to fill in


if __name__ == "__main__":
    agent = InverseKinematicsAgent()
    # test inverse kinematics
    T = identity(4)
    T[-1, 1] = 0.05
    T[-1, 2] = -0.26
    agent.set_transforms("LLeg", T)
    agent.run()
