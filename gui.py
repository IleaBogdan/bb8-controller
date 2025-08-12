import pygame
import math

class CircleVisualizer:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Screen dimensions
        self.width = 800
        self.height = 400
        self.circle_radius = 150
        
        # Create screen
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("BB-8 Controller Visualization")
        
        # Colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        
        # Circle centers
        self.center1 = (self.width // 4, self.height // 2)
        self.center2 = (3 * self.width // 4, self.height // 2)
        
        # Current point positions
        self.point1 = None
        self.point2 = None
        
        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()
    
    def draw_circles(self):
        """Draw the two circles on the screen."""
        # Clear screen
        self.screen.fill(self.white)
        
        # Draw circles
        pygame.draw.circle(self.screen, self.black, self.center1, self.circle_radius, 2)
        pygame.draw.circle(self.screen, self.black, self.center2, self.circle_radius, 2)
        
        # Draw center points
        pygame.draw.circle(self.screen, self.red, self.center1, 3)
        pygame.draw.circle(self.screen, self.red, self.center2, 3)
        
        # Draw points and lines if they exist
        if self.point1:
            pygame.draw.line(self.screen, self.blue, self.center1, self.point1, 2)
            pygame.draw.circle(self.screen, self.red, self.point1, 6)
        
        if self.point2:
            pygame.draw.line(self.screen, self.blue, self.center2, self.point2, 2)
            pygame.draw.circle(self.screen, self.red, self.point2, 6)
        
        # Update display
        pygame.display.flip()
    
    def update_point(self, x, y, use_second_circle=False):
        """Update the point position in one of the circles."""
        center = self.center2 if use_second_circle else self.center1
        
        # Convert normalized coordinates (-1 to 1) to screen coordinates
        screen_x = center[0] + x * self.circle_radius
        screen_y = center[1] - y * self.circle_radius  # Subtract because Pygame Y increases downward
        
        if use_second_circle:
            self.point2 = (int(screen_x), int(screen_y))
        else:
            self.point1 = (int(screen_x), int(screen_y))
    
    def process_events(self):
        """Process Pygame events and return False if window should close."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    
    def tick(self, fps=60):
        """Control frame rate and process events."""
        self.clock.tick(fps)
        return self.process_events()
    
    def close(self):
        """Close the visualization window."""
        pygame.quit()