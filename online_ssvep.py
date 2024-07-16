import pygame
import time

# Initialize pygame
pygame.init()

# Set up the display
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)

# Define the stimulus properties
stim_color = (255, 255, 255)
stim_size = (100, 100)
stim_position = (window_size[0] // 2, window_size[1] // 2)
frequency = 10  # Frequency in Hz
flash_duration = 1.0 / frequency / 2  # Half period

# Define the properties for the nine squares
squares = [
    {"color": (255, 255, 255), "size": (100, 100), "position": (100, 100), "frequency": 9.25},
    {"color": (255, 255, 255), "size": (100, 100), "position": (400, 100), "frequency": 11.25},
    {"color": (255, 255, 255), "size": (100, 100), "position": (700, 100), "frequency": 7.5},
    {"color": (255, 255, 255), "size": (100, 100), "position": (100, 300), "frequency": 1.2},
    {"color": (255, 255, 255), "size": (100, 100), "position": (400, 300), "frequency": 6.5},
    {"color": (255, 255, 255), "size": (100, 100), "position": (700, 300), "frequency": 3.5},
    {"color": (255, 255, 255), "size": (100, 100), "position": (100, 500), "frequency": 4.5},
    {"color": (255, 255, 255), "size": (100, 100), "position": (400, 500), "frequency": 5.75},
    {"color": (255, 255, 255), "size": (100, 100), "position": (700, 500), "frequency": 6.75},
]

# # Calculate the flash duration for each square
# for square in squares:
#     square["flash_duration"] = 1.0 / square["frequency"] / 2

running = True

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the stimuli
    screen.fill((0, 0, 0))  # Clear screen with black
    for square in squares:
        pygame.draw.rect(screen, square["color"], (*square["position"], *square["size"]))
    # pygame.display.flip()

    # Flash each square
    for square in squares:
        # time.sleep(square["flash_duration"])
        screen.fill((0, 0, 0))
        pygame.display.flip()
        # time.sleep(square["flash_duration"])

pygame.quit()