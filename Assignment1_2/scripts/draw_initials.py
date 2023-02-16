#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute
 
 
def turtle_draw():
    rospy.init_node('turtlesim', anonymous=True)
     # Draw the letter "R"
    pub = rospy.Publisher('/turtle1/cmd_vel',
                          Twist, queue_size=10)
    rate = rospy.Rate(10)
    vel = Twist()
    for i in range(30):
        vel.linear.x = 2
        vel.linear.y = 0
        vel.linear.z = 0
        vel.angular.x = 0
        vel.angular.y = 0
        vel.angular.z = 2
        pub.publish(vel)
        rate.sleep()

    for i in range(30):
        vel.linear.x = 1
        vel.linear.y = 0
        vel.linear.z = 0
        vel.angular.x = 0
        vel.angular.y = 0
        vel.angular.z = 0
        pub.publish(vel)
        rate.sleep()

    for i in range(20):
        vel.linear.x = -1
        vel.linear.y = 0
        vel.linear.z = 0
        vel.angular.x = 0
        vel.angular.y = 0
        vel.angular.z = 0
        pub.publish(vel)
        rate.sleep()
    
    for i in range(5):
        vel.angular.z = 1
        pub.publish(vel)
        rate.sleep()

    for i in range(25):
        vel.linear.x = 1
        vel.linear.y = 0
        vel.linear.z = 0
        vel.angular.x = 0
        vel.angular.y = 0
        vel.angular.z = 0
        pub.publish(vel)
        rate.sleep()
        
    ## draw H
    for i in range(25):
        vel.angular.z = 1
        pub.publish(vel)
        rate.sleep()

    for i in range(24):
        vel.linear.x = 1
        vel.linear.y = 0
        vel.linear.z = 0
        vel.angular.x = 0
        vel.angular.y = 0
        vel.angular.z = 0
        pub.publish(vel)
        rate.sleep()

    for i in range(13):
        vel.linear.x = -1
        vel.linear.y = 0
        vel.linear.z = 0
        vel.angular.x = 0
        vel.angular.y = 0
        vel.angular.z = 0
        pub.publish(vel)
        rate.sleep()
    
    for i in range(15):
        vel.linear.x = -2
        vel.angular.z = 2
        pub.publish(vel)
        rate.sleep()

    for i in range(15):
        vel.linear.x = 1
        vel.linear.y = 0
        vel.linear.z = 0
        vel.angular.x = 0
        vel.angular.y = 0
        vel.angular.z = 0
        pub.publish(vel)
        rate.sleep()

    for i in range(24):
        vel.linear.x = -1
        vel.linear.y = 0
        vel.linear.z = 0
        vel.angular.x = 0
        vel.angular.y = 0
        vel.angular.z = 0
        pub.publish(vel)
        rate.sleep()
    
if __name__ == '__main__':
    try:
        turtle_draw()
    except rospy.ROSInterruptException:
        pass