from connector import *
import json

class input_mav:
    __wanted_dist = 0
    __wanted_rot = 0
    __wated_calculated = False
    __current_rot = None
    __rot_variant = None # left or right
    __diving_variant = None # forwards or backwards
    __XYreal = [0,0]
    __breakloop = False
    __mavX=0
    __mavY=0
    __x_old=0.0
    __y_old=0.0
    __steps=0
    __counted_steps=0
    __startPoint=[0,0] #startpunkt für die distanzberechnung
    def __int__(self):
        __wanted_dist=0
        __rot_variant = None
        __diving_variant = None

    # alle Bewegungen werden hier gesteuert
    def move_marvin(self,topic, action):
        if (topic == 'mav/forward'):
            distance = json.loads(action)['distance']
            self.go_forward(distance)
        elif (topic == 'mav/backward'):
            distance = json.loads(action)['distance']
            self.go_backward(distance)
        elif (topic == 'mav/turn_left'):
            grad = json.loads(action)['angle']
            self.turn_left(grad)
        elif (topic == 'mav/turn_right'):
            grad = json.loads(action)['angle']
            self.turn_right(grad)
        elif (topic == 'mav/stop_mav'):
            self.__rot_variant = None
            self.__diving_variant = None
            self.set_mavXY(0.0, 0.0)

    # die Rotation wird in 15° Schritte aufgeteilt die Nacheinander Abgefahren werden Drehungen über die Bewegungerichtung des Mav zu berechnen war zu ungenau
    def turn_left(self,mqtt_rot):
        self.__startPoint = self.get_XYreal()
        self.__rot_variant = "left" # Bewegung nach links initiiert
        self.__steps = int(mqtt_rot / 15)
        self.__counted_steps=0

    def turn_right(self,mqtt_rot):
        self.__startPoint = self.get_XYreal()
        self.__rot_variant = "right" # Bewegung nach rechts initiiert
        self.__steps=int(mqtt_rot/15) # keine brüche mit kommastelle
        self.__counted_steps=0

    def go_forward(self,distance):
        self.__wanted_dist = distance
        self.__diving_variant = "forward" # Bewegung nach vorn initiiert
        self.__startPoint = self.get_XYreal()

    def go_backward(self,distance):
        self.__wanted_dist = distance
        self.__diving_variant = "backwards" # Bewegung nach hinten initiiert
        self.__startPoint = self.get_XYreal()

    def add_step(self):
        self.__counted_steps=self.__counted_steps+1
    #--------------------------------------set/get coordinates for calucation
    def set_real_coordinates(self,x,y):
        self.__XYreal=[x,y]

    def set_current_rotation(self):
        x, y, xb, yb, rot = self.get_lineOfMovement()
        lom = [xb, yb, x, y]
        self.__current_rot = angle_with_y_axis(lom)

    def get_current_rotation(self):
        return self.__current_rot

    def get_lineOfMovement(self):
        return self.__XYreal[0] ,self.__XYreal[1] , self.__x_old, self.__y_old, self.__current_rot

    def set_Old_Coordinates(self,real):
        self.__x_old=real[0]
        self.__y_old=real[1]

    def get_XYreal(self):
        return self.__XYreal

    #/get where the mav should drive
    def get_mavX(self):
        return self.__mavX

    def get_mavY(self):
        return self.__mavY

    def set_mavXY(self,x,y):
        self.__mavX=x
        self.__mavY=y

    #  compute the new data from Alexa, calculate what the maw has to do
    def compute_new_data(self):
        if self.__diving_variant != None:
            if self.__diving_variant == "forward":

                if self.distanz_2d_2p(self.__startPoint, self.__XYreal) <= self.__wanted_dist:
                    self.set_mavXY(0.0, 0.2)

                elif self.distanz_2d_2p(self.__startPoint, self.__XYreal) >= self.__wanted_dist:
                    self.set_mavXY(0, 0)
                    self.__diving_variant=None

            elif self.__diving_variant == "backwards":

                if self.distanz_2d_2p(self.__startPoint, self.__XYreal) <= self.__wanted_dist:
                    self.set_mavXY(0, -0.1)
                elif self.distanz_2d_2p(self.__startPoint, self.__XYreal) >= self.__wanted_dist:
                    self.set_mavXY(0, 0)
                    self.__diving_variant=None

        elif self.__rot_variant != None:
            if self.__rot_variant == "left": #left turn
                if self.__steps > self.__counted_steps:
                    self.set_mavXY(0.1, 0.1)
                else:
                    self.set_mavXY(0, 0)
                    self.__rot_variant = None
                    self.__steps=0
                    self.__counted_steps=0

            elif self.__rot_variant == "right":
                if self.__steps > self.__counted_steps:
                    self.set_mavXY(-0.1, 0.1)
                else:
                    print("else block")
                    self.set_mavXY(0, 0)
                    self.__rot_variant = None
                    self.__steps = 0
                    self.__counted_steps = 0
        else:
            self.set_mavXY(0,0)
    #---------------------------------------------------------------------

    # Distanz zwischen 2 Positionen berechnen
    def distanz_2d_2p(self,punkt1,punkt2):
        x1, y1 = punkt1
        x2, y2 = punkt2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    #---------------------------------------for breaking the threads
    def set_breakloop(self,br_loop):
        self.__breakloop=br_loop

    def get_breakloop(self):
        return self.__breakloop
    #----------------------------------------------------------------
    def input_thread(self):
        while self.__breakloop==False:
            print("input thread")
