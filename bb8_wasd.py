'''
angles:
0 - w => -1
90 - d => +1
180 - s => +1
270 - a => -1
'''
import time
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
import keyboard
import math
 
# consts:
modSpeed=50
turboSpeed=75

def move(droid, angle, speed):
    if (angle!=None):
        droid.set_heading(angle)
        droid.set_speed(speed)
    else:
        droid.set_speed(0)

def dumb_angle(keys):
    if keys.get('w'):
        return 0
    if keys.get('d'):
        return 90
    if keys.get('s'):
        return 180
    if keys.get('a'):
        return 270
    return None

def calc_angle(keys): # normalizing angels with vectors for smoother driving
    return dumb_angle(keys) # get rid of this shit as soon as you can 
    
    #problem: it only goes up, down and right. WHY ISN'T IT GOING TO THE LEFT???????
    x,y=0,0
    if keys.get('w'): y-=1
    if keys.get('s'): y+=1
    if keys.get('d'): x+=1
    if keys.get('a'): x-=1

    '''
        +1
    -1      +1
        -1
    '''
    if x==0 and y==0: return None
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
    return math.floor(deg_AOB)
    
    
def main():
    print("when bb8 glos blue you can start moveing him")
    
    useSpeed=modSpeed
    keys={}
    bb8=scanner.find_toy() # NOTE: when I will put the controller with the pygame library I will have to do tha pygame.init() after this
    with SpheroEduAPI(bb8) as droid:
        droid.set_main_led(Color(r=0, g=0, b=255))
        while True:
            keys['w']=keyboard.is_pressed('w')
            keys['a']=keyboard.is_pressed('a')
            keys['s']=keyboard.is_pressed('s')
            keys['d']=keyboard.is_pressed('d')
            move(droid, calc_angle(keys), useSpeed)
            keys.clear()

main()