"""In this exercise you need to implement an angle interploation function which makes NAO executes keyframe motion

* Tasks:
    1. complete the code in `AngleInterpolationAgent.angle_interpolation`,
       you are free to use splines interploation or Bezier interploation,
       but the keyframes provided are for Bezier curves, you can simply ignore some data for splines interploation,
       please refer data format below for details.
    2. try different keyframes from `keyframes` folder

* Keyframe data format:
    keyframe := (names, times, keys)
    names := [str, ...]  # list of joint names
    times := [[float, float, ...], [float, float, ...], ...]
    # times is a matrix of floats: Each line corresponding to a joint, and column element to a key.
    keys := [[float, [int, float, float], [int, float, float]], ...]
    # keys is a list of angles in radians or an array of arrays each containing [float angle, Handle1, Handle2],
    # where Handle is [int InterpolationType, float dTime, float dAngle] describing the handle offsets relative
    # to the angle and time of the point. The first Bezier param describes the handle that controls the curve
    # preceding the point, the second describes the curve following the point.
"""

from pid import PIDAgent
from keyframes import hello


class AngleInterpolationAgent(PIDAgent):
    def __init__(
        self,
        simspark_ip="localhost",
        simspark_port=3100,
        teamname="DAInamite",
        player_id=0,
        sync_mode=True,
    ):
        super(AngleInterpolationAgent, self).__init__(
            simspark_ip, simspark_port, teamname, player_id, sync_mode
        )
        self.keyframes = ([], [], [])

    def think(self, perception):
        target_joints = self.angle_interpolation(self.keyframes, perception)
        target_joints["RHipYawPitch"] = target_joints[
            "LHipYawPitch"
        ]  # copy missing joint in keyframes
        self.target_joints.update(target_joints)
        return super(AngleInterpolationAgent, self).think(perception)

    def angle_interpolation(self, keyframes, perception):
        target_joints = {}
        # YOUR CODE HERE
        names, times, keys = keyframes

        current_time = perception.time
        for name, joint_times, joint_keys in zip(names, times, keys):
            #  current  segment
            for i in range(len(joint_times) - 1):
                if joint_times[i] <= current_time <= joint_times[i + 1]:
                    t = (current_time - joint_times[i]) / (
                        joint_times[i + 1] - joint_times[i]
                    )
                    if t <= 0:
                        t = 1  # can't have division by zero.
                    p0 = joint_keys[i][0]
                    p3 = joint_keys[i + 1][0]
                    if len(joint_keys[i]) > 1:
                        p1 = p0 + joint_keys[i][1][2]  # first
                        p2 = (
                            p3 - joint_keys[i + 1][0][2]
                        )  # 2nd. If it exist, if it doesn't:
                    else:
                        p1, p2 = p0, p3

                    # Cubic Bezier interpolation
                    angle = (
                        (1 - t) ** 3 * p0
                        + 3 * (1 - t) ** 2 * t * p1
                        + 3 * (1 - t) * t**2 * p2
                        + t**3 * p3
                    )
                    target_joints[name] = angle
                    break

        return target_joints


if __name__ == "__main__":
    agent = AngleInterpolationAgent()
    agent.keyframes = hello()
    agent.run()
