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

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the stimulus
    screen.fill((0, 0, 0))  # Clear screen with black
    pygame.draw.rect(screen, stim_color, (*stim_position, *stim_size))
    pygame.display.flip()
    time.sleep(flash_duration)

    # Blank screen
    screen.fill((0, 0, 0))
    pygame.display.flip()
    time.sleep(flash_duration)

pygame.quit()