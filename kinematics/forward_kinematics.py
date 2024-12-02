"""In this exercise you need to implement forward kinematics for NAO robot

* Tasks:
    1. complete the kinematics chain definition (self.chains in class ForwardKinematicsAgent)
       The documentation from Aldebaran is here:
       http://doc.aldebaran.com/2-1/family/robots/bodyparts.html#effector-chain
    2. implement the calculation of local transformation for one joint in function
       ForwardKinematicsAgent.local_trans. The necessary documentation are:
       http://doc.aldebaran.com/2-1/family/nao_h21/joints_h21.html
       http://doc.aldebaran.com/2-1/family/nao_h21/links_h21.html
    3. complete function ForwardKinematicsAgent.forward_kinematics, save the transforms of all body parts in torso
       coordinate into self.transforms of class ForwardKinematicsAgent

* Hints:
    1. the local_trans has to consider different joint axes and link parameters for different joints
    2. Please use radians and meters as unit.
"""

# add PYTHONPATH
import os
import sys

sys.path.append(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "joint_control")
)

from numpy.matlib import matrix, identity

from recognize_posture import PostureRecognitionAgent


class ForwardKinematicsAgent(PostureRecognitionAgent):
    def __init__(
        self,
        simspark_ip="localhost",
        simspark_port=3100,
        teamname="DAInamite",
        player_id=0,
        sync_mode=True,
    ):
        super(ForwardKinematicsAgent, self).__init__(
            simspark_ip, simspark_port, teamname, player_id, sync_mode
        )
        self.transforms = {n: identity(4) for n in self.joint_names}

        # chains defines the name of chain and joints of the chain
        self.chains = {
            "Head": ["HeadYaw", "HeadPitch"]
            # YOUR CODE HERE
        }

    def think(self, perception):
        self.forward_kinematics(perception.joint)
        return super(ForwardKinematicsAgent, self).think(perception)

    def local_trans(self, joint_name, joint_angle):
        """calculate local transformation of one joint

        :param str joint_name: the name of joint
        :param float joint_angle: the angle of joint in radians
        :return: transformation
        :rtype: 4x4 matrix
        """
        T = identity(4)
        # YOUR CODE HERE
        if "Hip" in joint_name:
            T[0:3, 3] = matrix([0, 0.050 if "L" in joint_name else -0.050, -0.085]).T
        elif "Shoulder" in joint_name:
            T[0:3, 3] = matrix([0, 0.098 if "L" in joint_name else -0.098, 0.100]).T

        ca, sa = cos(joint_angle), sin(joint_angle)
        if "Roll" in joint_name:
            T[0:3, 0:3] = matrix([[1, 0, 0], [0, ca, -sa], [0, sa, ca]])
        elif "Pitch" in joint_name:
            T[0:3, 0:3] = matrix([[ca, 0, sa], [0, 1, 0], [-sa, 0, ca]])
        elif "Yaw" in joint_name:
            T[0:3, 0:3] = matrix([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]])
        return T

    def forward_kinematics(self, joints):
        """forward kinematics

        :param joints: {joint_name: joint_angle}
        """
        for chain_joints in self.chains.values():
            T = identity(4)
            for joint in chain_joints:
                angle = joints[joint]
                Tl = self.local_trans(joint, angle)
                # YOUR CODE HERE
                T = T * Tl  # honestly not confident about this at all.
                self.transforms[joint] = T


if __name__ == "__main__":
    agent = ForwardKinematicsAgent()
    agent.run()
