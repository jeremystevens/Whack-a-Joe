# /usr/bin/python
# Copyright 2023 Jeremy Stevens <jeremiahstevens@gmail.com>
#Wack-A-Mole is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Wack-A-Mole is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.

import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 640
HEIGHT = 480
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whack-A-Joe")

# Set up game assets
BACKGROUND_COLOR = (255, 255, 255)
MOLE_IMAGE = pygame.transform.scale(pygame.image.load("mole.png"), (50, 50))
MOLE_WIDTH = MOLE_HEIGHT = 30
WHACK_SOUND = pygame.mixer.Sound("whack.wav")
DEAD_SOUND = pygame.mixer.Sound("dead.wav")
FONT = pygame.font.SysFont(None, 36)
MOUSE_IMAGE = pygame.transform.scale(pygame.image.load("hand.png"), (50, 50))

# Set up game variables
score = 0
clock = pygame.time.Clock()

class Mole:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visible = False
        self.image = MOLE_IMAGE

    def appear(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def update(self):
        if random.randint(1, 1000) == 1:
            self.appear()

    def draw(self):
        if self.visible:
            WINDOW.blit(self.image, (self.x, self.y))

# Set up moles
moles = []
for i in range(5):
    x = random.randint(0, WIDTH - MOLE_WIDTH)
    y = random.randint(0, HEIGHT - MOLE_HEIGHT)
    moles.append(Mole(x, y))

# Set up mouse pointer
pygame.mouse.set_visible(False)
mouse_image_rect = MOUSE_IMAGE.get_rect()

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for mole in moles:
                if mole.visible and mole.x < pos[0] < mole.x + MOLE_WIDTH and mole.y < pos[1] < mole.y + MOLE_HEIGHT:
                    mole.hide()
                    score += 1
                    WHACK_SOUND.play()
                    DEAD_SOUND.play()

                # play whack sound if the mouse button is clicked
                else:
                    WHACK_SOUND.play()

    # Update game
    for mole in moles:
        mole.update()

    # Draw game
    WINDOW.fill(BACKGROUND_COLOR)
    for mole in moles:
        mole.draw()
    score_text = FONT.render("Score: " + str(score), True, (0, 0, 0))
    WINDOW.blit(score_text, (10, 10))
    pos = pygame.mouse.get_pos()
    mouse_image_rect.center = pos
    WINDOW.blit(MOUSE_IMAGE, mouse_image_rect)
    pygame.display.flip()

    # Control game speed
    clock.tick(60)

# Clean up
pygame.quit()
