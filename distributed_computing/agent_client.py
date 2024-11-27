"""In this file you need to implement remote procedure call (RPC) client

* The agent_server.py has to be implemented first (at least one function is implemented and exported)
* Please implement functions in ClientAgent first, which should request remote call directly
* The PostHandler can be implement in the last step, it provides non-blocking functions, e.g. agent.post.execute_keyframes
 * Hints: [threading](https://docs.python.org/2/library/threading.html) may be needed for monitoring if the task is done
"""

import weakref
import threading


class PostHandler:
    ###"""the post hander wraps function to be excuted in paralle"""
    def __init__(self, obj):
        self.proxy = weakref.proxy(obj)
        self.threads = {}
        print(f"{self.proxy}")
        print(f"{self.threads=}")

    def execute_keyframes(self, keyframes):
        """non-blocking call of ClientAgent.execute_keyframes"""
        # YOUR CODE HERE
        key_thread = threading.Thread(
            target=self.proxy.execute_keyframes,
            args=(keyframes,),  # args kwargs please work.
        )
        print(f"{key_thread=}")
        key_thread.start()
        print(f"started key_thread ")
        self.threads["keyframes"] = key_thread
        return True

    def set_transform(self, effector_name, transform):
        thread = threading.Thread(
            target=self.proxy.set_transform, args=(effector_name, transform)
        )
        thread.start()
        self.threads["transform"] = thread
        print(f"{self.threads=}")
        return True


from xmlrpc.client import ServerProxy


class ClientAgent(object):
    """ClientAgent request RPC service from remote server"""

    # YOUR CODE HERE
    def __init__(self):
        self.proxy = ServerProxy("http://localhost:8000")
        self.post = PostHandler(self)

    def get_angle(self, joint_name):
        return self.proxy.get_angle(joint_name)

    def set_angle(self, joint_name, angle):
        return self.proxy.set_angle(joint_name, angle)

    def get_posture(self):
        """return current posture of robot"""
        return self.proxy.get_posture()

    def execute_keyframes(self, keyframes):
        """excute keyframes, note this function is blocking call,
        e.g. return until keyframes are executed
        """
        return self.proxy.execute_keyframes(keyframes)

    def get_transform(self, name):
        # """get transform with given name"""
        return self.proxy.get_transform(name)

    def set_transform(self, effector_name, transform):
        ###"""solve the inverse kinematics and control joints use the results"""
        return self.proxy.set_transform(effector_name, transform)


if __name__ == "__main__":
    agent = ClientAgent()
    # Test get/set angle
    print("Setting HeadYaw to 0.5...")
    agent.set_angle("HeadYaw", 0.5)
    print("HeadYaw angle:", agent.get_angle("HeadYaw"))
