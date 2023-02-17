#!/usr/bin/env python3

import rospy
from turtlesim.srv import Spawn, Kill
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from turtlesim.msg import Pose
import math


class Hunter:
    def __init__(self):
        ## initialising the turtle
        rospy.wait_for_service('/spawn')
        spnHunt = rospy.ServiceProxy('/spawn', Spawn)
        spnHunt(3, 2, 0, "hunter_turtle")

        # a service to kill the turtle
        rospy.wait_for_service('/kill')
        self.killHunter = rospy.ServiceProxy('/kill', Kill)

        ## subscribing to the pose topic for the both turtle
        self.huntPoseSub = rospy.Subscriber('/hunter_turtle/pose', Pose, self.update_huntPose)
        self.runPoseSub = rospy.Subscriber('/runner_turtle/pose', Pose, self.update_runPose)

        self.huntPose = Pose(2, 2, 0, 0, 0)
        self.runPose = Pose(1, 1, 0, 0, 0)

        ## publishing to the cmd_vel topic for both tutrtle
        self.linVel = 2
        self.velPub = rospy.Publisher('/hunter_turtle/cmd_vel', Twist, queue_size=10)
        self.killPub = rospy.Publisher('/hunter_turtle/kill_runner', Bool, queue_size=1)
        self.velMsg = Twist()
        self.velMsg.linear.x = self.linVel

        self.angVelMax = 2

    def update_huntPose(self, pos):
        self.huntPose = pos

    def update_runPose(self, pos):
        self.runPose = pos
        
        
    def hunting(self):
        while True:
            curntAng = self.huntPose.theta

            x = self.huntPose.x - self.runPose.x
            y = self.huntPose.y - self.runPose.y
            reqAng = math.atan2(y, x)

            direction = 0
            if reqAng - curntAng != 0:
                direction = -1 * (reqAng - curntAng)/abs(reqAng - curntAng)

            ang_vel = abs(reqAng - curntAng)/math.pi
            if ang_vel > 1:
                ang_vel -= 2

            self.velMsg.angular.z = direction * ang_vel * self.angVelMax
            self.velPub.publish(self.velMsg)


if __name__ == "__main__":
    rospy.init_node('hunter')
    rospy.loginfo("Hunter node initialised")
    hunter = Hunter()
    hunter.hunting()
    rospy.spin()