import math

def angle_with_y_axis(lom):
                        #xA, yA, xB, yB
                        # old, new

    xB,yB= lom[0],lom[1]
    xA,yA= lom[2],lom[3]
    deltaY = xB - xA
    distance_AB = math.sqrt((xB - xA) ** 2 + (yB - yA) ** 2)
    sin_theta = deltaY / distance_AB
    angle_in_radians = math.asin(sin_theta)
    angle_in_degrees = math.degrees(angle_in_radians)
    if yB >= yA:
        if xB >= xA:
            pass
        else:
            angle_in_degrees = 360 + angle_in_degrees
    else:
        if xB >= xA:
            angle_in_degrees = 180 - angle_in_degrees
        else:
            angle_in_degrees = 180 - angle_in_degrees

    if angle_in_degrees < 0:
        angle_in_degrees += 360
    elif angle_in_degrees >= 360:
        angle_in_degrees -= 360

    return angle_in_degrees
