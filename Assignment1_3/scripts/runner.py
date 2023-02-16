#!/usr/bin/env python3

import rospy
import random
import math
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Spawn, SpawnRequest

# Callback function for the runner turtle's pose
def runner_pose_callback(pose_message):
    global runner_x, runner_y, runner_theta
    runner_x = pose_message.x
    runner_y = pose_message.y
    runner_theta = pose_message.theta

# Function to move the runner turtle with linear velocity [1, 0, 0]
def move_runner():
    velocity_publisher = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    vel_msg.linear.x = 1
    velocity_publisher.publish(vel_msg)

# Function to spawn the hunter turtle
def spawn_hunter():
    rospy.wait_for_service('spawn')
    try:
        spawn_turtle = rospy.ServiceProxy('spawn', Spawn)
        turtle_name = 'hunter'
        x = random.uniform(0, 11)
        y = random.uniform(0, 11)
        theta = random.uniform(0, 2 * math.pi)
        spawn_request = SpawnRequest(x=x, y=y, theta=theta, name=turtle_name)
        spawn_turtle(spawn_request)
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

if __name__ == '__main__':
    # Initialize the ROS node for the runner
    rospy.init_node('runner_controller')

    # Subscribe to the runner turtle's pose
    runner_pose_subscriber = rospy.Subscriber('turtle1/pose', Pose, runner_pose_callback)

    # Spawn the hunter turtle
    spawn_hunter()

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        move_runner()
        rate.sleep()
