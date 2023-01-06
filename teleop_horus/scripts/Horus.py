#!/usr/bin/env python3
""" Librairie ROS & JSON"""
import rospy
from std_msgs.msg import String
import json
import roslib
import time
from geometry_msgs.msg import Twist

"""Librairie UDP"""
import socket

"""Démarrage roslib"""
roslib.load_manifest('teleop_horus')

class UdpServer:
    def __init__(self, a_host, a_port):
        printer.print_info("Lancement du serveur UDP")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = a_port
        self.socket.bind((a_host, a_port))
        self.socket.settimeout(0.3)
        t = threading.Thread(target=self.get_data)
        t.start()
		        
    def get_data(self):
        """Configuration ROS"""
        rate = rospy.Rate(10) # 10hz
        pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        twist = Twist()
        speed = 0.4
		
        while True:
            try:
                data, (ip, port) = self.socket.recvfrom(4096)

            except:
                printer.print_error("ERROR Socket timeout UDP")
                pub.sendMessage("UDP_TIMEOUT", port=self.port)
                continue

            if not data:
                printer.print_error("UDP Problem")
                pub.sendMessage("UDP_TIMEOUT", gps=self.port)
                continue

            try:
                data_decoded = data.decode("UTF-8")
                json_information = json.loads(data_decoded)
                Horus(json_information)

            except json.decoder.JSONDecodeError:
                printer.print_error("ERROR : JSON WRONG")
                continue


def Horus(data):

	
    #Controle selon la trame Json
    while not rospy.is_shutdown():
        for control in data["controls"] :
            if control["name"]=="Avant":
                print("on avance de", control["amplitude"][0])
                twist.linear.x = control["amplitude"][0];
                rospy.loginfo("checking for cmd \n" + str(twist.linear)) 
                pub.publish(twist)
            if control["name"]=="Droite":
                print("on tourne de", control["amplitude"][0])
                twist.angular.z = control["amplitude"][0];
                rospy.loginfo("checking for cmd \n" + str(twist.angular)) 
                pub.publish(twist)

            rate.sleep()



if __name__ == '__main__':
    try:
        rospy.init_node('horus', anonymous=True)
        
    except rospy.ROSInterruptException:
        pass
