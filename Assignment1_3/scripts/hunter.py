#!/usr/bin/env python3

import rospy
import math
import random
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import GetPose

# Callback function for the hunter turtle's pose
def hunter_pose_callback(pose_message):
    global hunter_x, hunter_y, hunter_theta
    hunter_x = pose_message.x
    hunter_y = pose_message.y
    hunter_theta = pose_message.theta

# Function to move the hunter turtle towards the runner
def move_towards_runner(runner_x, runner_y):
    global hunter_x, hunter_y
    velocity_publisher = rospy.Publisher('hunter/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    # Calculate the distance to the runner
    distance = math.sqrt((runner_x - hunter_x)**2 + (runner_y - hunter_y)**2)

    # Limit the hunter's maximum linear velocity
    if distance > 1:
        vel_msg.linear.x = 1
    else:
        vel_msg.linear.x = distance

    # Set the hunter's angular velocity to a random value between -1 and 1
    vel_msg.angular.z = random.uniform(-1, 1)
    velocity_publisher.publish(vel_msg)

if __name__ == '__main__':
    # Initialize the ROS node for the hunter
    rospy.init_node('hunter_controller')

    # Subscribe to the hunter turtle's pose
    hunter_pose_subscriber = rospy.Subscriber('hunter/pose', Pose, hunter_pose_callback)

    # Loop to continuously follow the runner turtle
    while not rospy.is_shutdown():
        try:
            # Get the runner turtle's position using the /turtle1/pose service
            rospy.wait_for_service('/turtle1/get_pose')
            get_pose = rospy.ServiceProxy('/turtle1/get_pose', GetPose)
            runner_pose = get_pose()
            runner_x = runner_pose.x
            runner_y = runner_pose.y

            move_towards_runner(runner_x, runner_y)

        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)
        except rospy.exceptions.ROSInterruptException:
            pass
