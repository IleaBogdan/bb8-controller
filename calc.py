from multipledispatch import dispatch
import math

def get_angle(x, y):
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
    return deg_AOB

@dispatch(int,int)
def get_speed(x, y):
    is_neg=-1 if y>0.0 else 1
    speed=math.sqrt(x*x+y*y)*160.0*is_neg # this formula is shit, but I have no better ideas for it 
    return speed

@dispatch((float,int))
def get_speed(x):
    # print(x)
    return 160*x

def normalize_to_circle(x, y):
    length = math.sqrt(x**2 + y**2)
    if length > 1.0:
        x /= length
        y /= length
    return x, y