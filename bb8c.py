from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
from controllers import XboxOneController
import pygame
import math

# const values:
modSpeed=50
turboSpeed=75
maxSpeed=100

def calc_angle_and_speed(x, y):
    '''
        +1
    -1      +1
        -1
    '''
    if x==0 and y==0: return [None, None]
    y=-y # making y to be in the xOy 
    sin_AOB=abs(x)/math.sqrt(x*x+y*y)
    rad_AOB=math.asin(sin_AOB)
    deg_AOB=(rad_AOB*180.0)/math.pi
    if x>0 and y<0:
        # quadrant 4 (idk some symmetry stuff)
        deg_AOB=180-deg_AOB
    elif x<0 and y<0:
        # quadrant 3 (adding 180 to flip it)
        deg_AOB+=180
    elif x<0 and y>0:
        # quadrant 2 (same stuff as quadrant 4 but with +180)
        deg_AOB=360-deg_AOB
    speed=math.sqrt(x*x+y*y)*100.0
    return [deg_AOB, speed]

def move(droid, fangle, fspeed):
    if (fangle!=None and fspeed!=None):
        droid.set_heading(fangle)
        droid.set_speed(fspeed)
    else:
        droid.set_speed(0)

def main():
    print("bb8 will be drivable after it glows blue")
    spherobb8=scanner.find_BB8()
    print("connected to bb8")
    xoc=XboxOneController(0)
    with SpheroEduAPI(spherobb8) as bb8:
        bb8.set_main_led(Color(r=0, g=0, b=255))
        print("you can drive bb8 now")
        run=True
        while run:
            pygame.event.pump() # VERY IMPORTANT, THIS ALLOWS THE BLUETOOTH TO TAKE THE CONTROLLER INPUT
            
            button_states=xoc.get_button_states()
            # print(button_states)
            if button_states['M']:
                run=False
            axis=xoc.get_axes()
            angle_and_speed=calc_angle_and_speed(axis["left_x"], axis["left_y"])[:]
            print(angle_and_speed)
            fangle, fspeed=math.floor(angle_and_speed[0]),math.floor(angle_and_speed[1])
            move(bb8, fangle, fspeed) 
            
    del xoc

if __name__=="__main__":
    main()