import warnings
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")
import pygame
import math
from typing import Optional, Dict, Tuple

class XboxOneController:
    # Class-level button mappings
    BUTTON_CODE_TO_NAME = {
        0: 'A',
        1: 'B',
        2: 'X',
        3: 'Y',
        4: 'LB',  # Left Bumper
        5: 'RB',  # Right Bumper
        6: 'CV',  # Change View
        7: 'M',   # Menu
        8: 'LSP',  # Left Stick Press
        9: 'RSP',  # Right Stick Press
        10: 'H',   # Home/Xbox Button
    }
    
    # Reverse mapping for convenience
    BUTTON_NAME_TO_CODE = {v: k for k, v in BUTTON_CODE_TO_NAME.items()}

    def __init__(self, controller_index: int = 0):
        self._init_pygame()
        self.joystick = self._init_controller(controller_index)
        self._setup_button_mappings()

    def _init_pygame(self) -> None:
        if not pygame.get_init():
            pygame.init()
        if not pygame.joystick.get_init():
            pygame.joystick.init()

    def _init_controller(self, index: int) -> pygame.joystick.Joystick:
        try:
            joystick = pygame.joystick.Joystick(index)
            joystick.init()
            print(f"Controller detected: {joystick.get_name()}")
            return joystick
        except pygame.error as e:
            raise RuntimeError(f"No controller detected at index {index}: {str(e)}")

    def _setup_button_mappings(self) -> None:
        """Setup button mappings for this controller instance."""
        self.button_code_to_name = self.BUTTON_CODE_TO_NAME.copy()
        self.button_name_to_code = self.BUTTON_NAME_TO_CODE.copy()

    @staticmethod
    def calc_angle(x, y):
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

    def get_button_states(self) -> Dict[str, bool]:
        return {
            name: self.joystick.get_button(code)
            for code, name in self.button_code_to_name.items()
            if code < self.joystick.get_numbuttons()
        }

    def get_axes(self) -> Dict[str, float]:
        return {
            "left_x": self.joystick.get_axis(0),
            "left_y": self.joystick.get_axis(1),
            "right_x": self.joystick.get_axis(2),
            "right_y": self.joystick.get_axis(3),
            "left_trigger": (self.joystick.get_axis(4) + 1) / 2,  # Normalize to 0-1
            "right_trigger": (self.joystick.get_axis(5) + 1) / 2,  # Normalize to 0-1
        }

    def process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.JOYBUTTONDOWN:
                button_name = self.button_code_to_name.get(event.button, f"Unknown({event.button})")
                print(f"Button pressed: {button_name}")
            elif event.type == pygame.JOYBUTTONUP:
                button_name = self.button_code_to_name.get(event.button, f"Unknown({event.button})")
                print(f"Button released: {button_name}")
        return True

if __name__ == "__main__":
    try:
        controller = XboxOneController()
        
        running = True
        while running:
            running = controller.process_events()
            
            # Get and print current controller state
            axes = controller.get_axes()
            angle = controller.calc_angle(axes["left_x"], axes["left_y"])
            
            print(f"Left stick: ({axes['left_x']:.2f}, {axes['left_y']:.2f}) Angle: {angle}°")
            # print(f"Right stick: ({axes['right_x']:.2f}, {axes['right_y']:.2f})")
            # print(f"Triggers: LT={axes['left_trigger']:.2f}, RT={axes['right_trigger']:.2f}")
            
            pygame.time.delay(1000)  

    except RuntimeError as e:
        print(f"Error: {e}")
    finally:
        pygame.quit()