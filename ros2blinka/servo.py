# ROS2Blinka Servo Actor Node Library
# Apache License 2.0, following ROS2 Lyrical




from adafruit_servokit import ServoKit




#Servo HAT, Bonnet, and other Adafruit Servo Modules
class NodeServoModule(object):
    def __init__(self, isFW=False, addr=0x40):
        self.address = addr
        self.module = ServoKit(address=self.address, channels=(isFW if 8 else 16))
        self.active = [None]*(isFW if 8 else 16)

    def enableChannel(self, ch, device):
        if self.active[ch] == None:
            self.active[ch] = device
        else:
            raise Exception(f"[WARN] Cannot directly reassign Channel {ch} on Servo Module {self.address}, safe remove it first with keyword 'del'!")

    def disableChannel(self, ch):
        if self.active[ch] != None:
            self.active[ch] = None
        else:
            raise Exception(f"[WARN] Attempted to clear Channel {ch} on Servo Module {self.address}, but it was already null.")



#Generic Constrained Servo
class ConstrainedServo(object):
    def __init__(self, parent, ch, mn=0, mx=180, ctr=90):
        self.parent = parent
        self.ch = ch
        self.parent.enableChannel(self.ch, self)
        self.reference = parent.module.servo[ch]
        

        self.ctr = ctr
        self.mn = mn
        self.mx = mx
        pass

    def __del__(self):
        self.parent.disableChannel(self.ch)

    def setAngle(self, angle):
        self.reference.angle = angle
        
    def getAngle(self):
        return self.reference.angle

    def resetAngle(self):
        self.setAngle(self.ctr)
    

#Continuous Rotation Servo
class ConRotServo(object):
    def __init__(self, parent, ch):
        self.reference = parent.module.continuous_servo[ch]
        parent.enableChannel(ch, self)

    def setThrottle(self, factor):
        self.reference.throttle = factor
    def brake(self):
        self.setThrottle(0)
