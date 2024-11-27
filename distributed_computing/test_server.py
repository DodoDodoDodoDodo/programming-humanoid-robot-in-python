# test server
from thefuzz import fuzz, process
from xmlrpc.server import SimpleXMLRPCServer

ANGLE = 0.5


class TestServer:
    def __init__(self):
        print("Test server init")

        self.angle_data = {}
        self.server = SimpleXMLRPCServer(("localhost", 8000))
        self.server.register_function(self.get_angle)
        self.server.register_function(self.set_angle)

    def get_angle(self, joint_name):
        print(f"Getting {joint_name=}")
        print(self.angle_data.get(joint_name, ANGLE))
        return self.angle_data.get(joint_name, ANGLE)

    def set_angle(self, joint_name, set_angle):
        self.angle_data[joint_name] = set_angle
        print(f"Setting {joint_name=} to {set_angle=}")
        return True

    def run(self):
        print("Test server running...")
        self.server.serve_forever()  # honestly not sure why/what this does.

    def get_posture(self):
        print("Getting posture")
        return list(self.angle_data.items())


if __name__ == "__main__":
    # TestServer().get_angle("HeadYaw")
    # print("Test server get angle HeadYaw done")
    # TestServer().set_angle("HeadYaw", 0.5)
    # print("Test server set angle HeadYaw done")
    TestServer().run()
    print("Test server run done")
