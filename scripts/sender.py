#!/usr/bin/env python

"""
    ros_tcp_comm Sender Node

    Authors: Nicholas McCullough and Joseph Neidigh

    Faculty Advisor: Dr. Nathan Sprague

    Version 1.0

    This node sends messages across a wireless network via a TCP connection.
    It is intended to send these messages to the corresponding 'Receiver' node
    in this package. Instructions for how to customize this node to subscribe to
    and send a particular topic are as follows:
"""

import socket
import pickle
import sys
import struct
import zlib
import rospy
import rostopic

class Sender():
    def __init__(self):
        rospy.init_node('sender')

        package = rospy.get_param('~package')
        name = rospy.get_param('~message_type')
        topic = rospy.get_param('~topic_name')
        RECEIVER_IP = rospy.get_param('~ip')
        PORT = rospy.get_param('~port_number')

        imported = getattr(__import__(package, fromlist=[name]), name)
        rospy.Subscriber(topic, imported, self.callback, queue_size=1)

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((RECEIVER_IP, PORT))
        except Exception as e:
            self.sock.close()
            rospy.loginfo("SENDER ERROR")
            rospy.loginfo(e)
            sys.exit()
        
        rospy.spin()

    def callback(self, topic_message):
        message = pickle.dumps(topic_message)
        compressed_message = zlib.compress(message)
        self.send_msg(compressed_message)

    def send_msg(self, msg):
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg
        try:
            self.sock.sendall(msg)
        except Exception as e:
            self.sock.close()
            rospy.loginfo("SENDER ERROR")
            rospy.loginfo(e)
            sys.exit()

if __name__ == "__main__":
    Sender()
