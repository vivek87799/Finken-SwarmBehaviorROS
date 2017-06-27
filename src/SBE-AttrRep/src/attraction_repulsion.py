#!/usr/bin/env python
import rospy
import geometry_msgs.msg
import math
import roslib; roslib.load_manifest('visualization_marker_tutorials')
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray

publisher = rospy.Publisher('copter_1_Marker_array' , MarkerArray, queue_size=10)



copterPos0 = geometry_msgs.msg.Pose2D(0,0,0)
copterPos1 = geometry_msgs.msg.Pose2D(0,0,0)

def marker_calc(copterPos, force, namespace):
    
    
    markerArray = MarkerArray()


    #marker for copter
    marker = Marker()
    marker.header.frame_id = "/neck"
    marker.ns = namespace
    marker.type = marker.SPHERE
    marker.action = marker.ADD
    marker.id = 0
    marker.scale.x = 0.2
    marker.scale.y = 0.2
    marker.scale.z = 0.2
    marker.color.a = 1.0
    marker.color.r = 1.0
    marker.color.g = 1.0
    marker.color.b = 0.0
    marker.pose.orientation.w = 1.0
    marker.pose.position.x = copterPos.x
    marker.pose.position.y = copterPos.y
    marker.pose.position.z = 0.0
    markerArray.markers.append(marker)
    
    #marker for force
    markerArrow = Marker()
    markerArrow.header.frame_id = "/neck"  
    markerArrow.ns = namespace
    markerArrow.type = marker.ARROW
    markerArrow.action = marker.ADD
    markerArrow.id = 1
    #marker.scale.x = 1
    markerArrow.scale.x = 0.1
    markerArrow.scale.y = 0.2
    markerArrow.scale.z = 0.2
    markerArrow.color.a = 1.0
    markerArrow.color.r = 1.0
    markerArrow.color.g = 1.0
    markerArrow.color.b = 0.0
    #marker.pose.orientation.w = 1.0
    #marker.pose.position.x = copterPos.x
    #marker.pose.position.y = copterPos.y
    #marker.pose.position.z = 0.0
    start = geometry_msgs.msg.Point()
    start.x = copterPos.x
    start.y = copterPos.y
    start.z = 0.0
    end = geometry_msgs.msg.Point()
    rospy.loginfo("copterPos.x %f  f0 %f",copterPos.x,force[0])
    rospy.loginfo("copterPos.y %f  f1 %f",copterPos.y,force[1])
    end.x = copterPos.x + ( force[0] ) * 0.5
    end.y = copterPos.y + ( force[1] ) * 0.5
    end.z = 0.0
    markerArrow.points.append(start)
    markerArrow.points.append(end)
    markerArray.markers.append(markerArrow)

    publisher.publish(markerArray)

def calcForce(copterPos0, copterPos1):
    cons = 1
    d=2.5
    diff_x = copterPos1.x - copterPos0.x
    rospy.loginfo("copter0PoseX %f   - copter1PoseX %f   = diff_x %f", copterPos0.x, copterPos1.x, diff_x)
    diff_y = copterPos1.y - copterPos0.y
    rospy.loginfo("copter0PoseY %f   - copter1PoseY %f   = diff_y %f", copterPos0.y, copterPos1.y, diff_y)
    dist = math.sqrt((diff_x*diff_x) + (diff_y*diff_y))

    rospy.loginfo("distance %f  ", dist)

    Fx = -cons*(dist-d) * diff_x
    Fy = -cons*(dist-d) * diff_y
    rospy.loginfo("Fx= %f , Fy= %f", Fx, Fy)

    return [Fx,Fy]
    

def copter0(data):
    global copterPos0
    global copterPos1
    copterPos0 = data
    force = calcForce(copterPos1, copterPos0)
    marker_calc(copterPos0, force, 'copter0')
    rospy.loginfo("Copter0")

def copter1(data):
    global copterPos0
    global copterPos1
    copterPos1 = data
    force = calcForce(copterPos0, copterPos1)
    marker_calc(copterPos1, force, 'copter1')
    rospy.loginfo("Copter1")
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('AttrRep', anonymous=True)

    rospy.Subscriber("copters/0/pose", geometry_msgs.msg.Pose2D, copter0)
    rospy.Subscriber("copters/1/pose", geometry_msgs.msg.Pose2D, copter1)
    #time.sleep(0.5)
	
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


    
    

if __name__ == '__main__':
    listener()
