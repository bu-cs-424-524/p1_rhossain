#!/usr/bin/env python3

import rospy
from turtlesim.srv import *
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import random


class Runner:
    def __init__(self):
        ## initialising the turtle
        rospy.wait_for_service('/spawn')
        self.spnRunner = rospy.ServiceProxy('/spawn', Spawn)
        self.spnRunner(5, 2, 0, "runner_turtle")
        
        ## subscribing to the pose topic for the both turtle
        self.huntPoseSub = rospy.Subscriber('/hunter_turtle/pose', Pose, self.update_huntPose)
        self.runPoseSub = rospy.Subscriber('/runner_turtle/pose', Pose, self.update_runPose)

        self.huntPose = Pose(2, 2, 0, 0, 0)
        self.runPose = Pose(8, 6, 0, 0, 0)

        ## publishing to the cmd_vel topic for runner tutrtle
        self.linVel = 1
        self.velPub = rospy.Publisher('/runner_turtle/cmd_vel', Twist, queue_size=10)
        self.velMsg = Twist()

        rospy.wait_for_service('/kill')
        self.killRunner = rospy.ServiceProxy('/kill', Kill)

    def update_huntPose(self, pos):
        self.huntPose = pos

    def update_runPose(self, pos):
        self.runPose = pos

    def runner_hunter_distance(self):
        return math.sqrt((self.huntPose.x - self.runPose.x) ** 2 + (self.huntPose.y - self.runPose.y) ** 2)
    
    def kill(self):
        self.killRunner('runner_turtle')
        self.spnRunner(random.random() * 9, random.random() * 9, 0, "runner_turtle")

    def main(self):
        self.killRunner('turtle1')
        self.velMsg.linear.x = self.linVel

        while True:
            angVel = random.random() * 2 - 1
            self.velMsg.angular.z = angVel

            t0 = rospy.Time.now().to_sec()
            t1 = rospy.Time.now().to_sec()

            while t1 - t0 < 2:
                t1 = rospy.Time.now().to_sec()
                self.velPub.publish(self.velMsg)

                if self.runner_hunter_distance() < 1:
                    self.kill()
                    self.runPose.y = 100000

    

if __name__ == "__main__":
    rospy.init_node('runner')
    rospy.loginfo("Hunter node initialised")
    runner = Runner()
    runner.main()
    rospy.spin()