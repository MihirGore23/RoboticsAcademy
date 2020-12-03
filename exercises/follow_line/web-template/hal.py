import rospy
import cv2
import threading
import time
from datetime import datetime

from interfaces.camera import ListenerCamera
from interfaces.motors import PublisherMotors

# Hardware Abstraction Layer
class HAL:
    IMG_WIDTH = 320
    IMG_HEIGHT = 240
    
    def __init__(self):
    	rospy.init_node("HAL")
    
    	self.image = None
    	self.camera = ListenerCamera("/F1ROS/cameraL/image_raw")
    	self.motors = PublisherMotors("/F1ROS/cmd_vel", 4, 0.3)
    	
    	self.image_lock = threading.Lock()
    	
    	t = threading.Thread(target=self.update_readings)
    	t.start()
    	
    # Explicit initialization functions
    # Class method, so user can call it without instantiation
    @classmethod
    def initRobot(cls):
        new_instance = cls()
        return new_instance
    
    # Get Image from ROS Driver Camera
    def getImage(self):
        self.image_lock.acquire()
        image = self.image
        self.image_lock.release()
        
        return image
        
    # Threading Function to keep the sensor readings updated
    def update_readings(self):
    	while True:
			self.image_lock.acquire()
			self.image = self.camera.getImage().data
			self.image_lock.release()
