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

pygame.quit()