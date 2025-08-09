import warnings
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")
import pygame

pygame.init()  
pygame.joystick.init()

try:
    # Attempt to setup the joystick
    joystick = pygame.joystick.Joystick(0)  # 0 for first controller
    joystick.init()
    print(f"Controller detected: {joystick.get_name()}")
except pygame.error:
    print("No controller detected!")
    exit()

button_code_to_name={
    0:'A',
    1:'B',
    2:'X',
    3:'Y',
    4:'LB', # Left Bumper
    5:'RB', # Right Bumper
    6:'CV', # Change View
    7:'M',  # Menu
    8:'LSP', # Left Stick Press
    9:'RSP', # Righ Stick Press
    10:'H', # Home/Xbox Button (The Big Round One With The Xbox Logo)
}
button_name_to_code={

}

run=True
while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.JOYBUTTONDOWN:
            if event.button in button_code_to_name.keys():
                print(button_code_to_name[event.button])
            else:
                print(f"unknown button code: {event.button}")
    # instantly checking all the buttons (keep in mind when making the xbox_one_controller class)
    # button_states = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
    # print(button_states)


    # the D-pad (the cross)
    # -1,0 => left
    # 1,0 => right
    # 0,1 => up
    # 0,-1 => down
    hat=joystick.get_hat(0)
    # print(hat)
    

    left_x = joystick.get_axis(0)
    left_y = joystick.get_axis(1)
    right_x = joystick.get_axis(2)
    right_y = joystick.get_axis(3)
    left_trigger = joystick.get_axis(4)  # Values from -1 to 1 (often needs adjustment)
    right_trigger = joystick.get_axis(5)  # Values from -1 to 1 (often needs adjustment)
    # print(f"Left joystick: {left_x},{left_y}")
    # print(f"Right joystick: {right_x},{right_y}")
    # print(f"Left trigger: {left_trigger}")
    print(f"Right trigger: {right_trigger}")
    

pygame.quit()