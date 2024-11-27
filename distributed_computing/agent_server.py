"""In this file you need to implement remote procedure call (RPC) server

* There are different RPC libraries for python, such as xmlrpclib, json-rpc. You are free to choose.
* The following functions have to be implemented and exported:
 * get_angle
 * set_angle
 * get_posture
 * execute_keyframes
 * get_transform
 * set_transform
* You can test RPC server with ipython before implementing agent_client.py
"""

# add PYTHONPATH
import os
import sys
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer

sys.path.append(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "kinematics")
)

# from kinematics.inverse_kinematics import InverseKinematicsAgent
from inverse_kinematics import InverseKinematicsAgent  # but why?


class ServerAgent(InverseKinematicsAgent):
    """ServerAgent provides RPC service"""

    def __init__(
        self,
        simspark_ip="localhost",
        simspark_port=3100,
        teamname="DAInamite",
        player_id=0,
        sync_mode=True,
    ):
        try:
            super().__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        except ConnectionRefusedError:
            print("no simspark connection")
            self.perception = type("obj", (), {"joint": {}, "transform": {}})()
            self.action = type("obj", (), {"joint": {}, "transform": {}})()

        self.server = SimpleXMLRPCServer(("localhost", 8000))
        for func in [
            self.get_angle,
            self.set_angle,
            self.get_posture,
            self.execute_keyframes,
            self.get_transform,
            self.set_transform,
        ]:
            self.server.register_function(func)

    def get_angle(self, joint_name):
        return self.perception.joint.get(joint_name, 0.0)

    def set_angle(self, joint_name, angle):
        self.action.joint[joint_name] = angle
        return True

    def get_posture(self):
        """return current posture of robot"""
        # YOUR CODE HERE
        print(f"{self.perception.joint=}")
        return list(self.perception.joint.items())

    def execute_keyframes(self, keyframes):
        """excute keyframes, note this function is blocking call,
        e.g. return until keyframes are executed
        """
        # YOUR CODE HERE
        for frameframe in keyframes:
            time, joints = frameframe
            for joint, angle in joints.items():
                self.set_angle(joint, angle)
        return True

    def get_transform(self, name):
        """get transform with given name"""
        # YOUR CODE HERE
        x = self.perception.transform.get(name, [0.0, 0.0, 0.0])
        y = self.perception.transform.get(name, [0.1, 0.1, 0.1])

        print(f"{self.perception.transform=}")
        print(f"{(x==y)=}")
        return y

    def set_transform(self, effector_name, transform):
        """solve the inverse kinematics and control joints use the results"""
        # YOUR CODE HERE
        return self.inverse_kinematics(effector_name, transform)


if __name__ == "__main__":
    agent = ServerAgent()
    agent.run()
