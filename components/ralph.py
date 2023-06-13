import pygame
import random


class Ralph(pygame.sprite.Sprite):
    """
    A class representing Ralph, the antagonist character.
    """

    def __init__(self):
        """
        Initializes a Ralph instance with a default position and image.
        """
        super().__init__()
        self.image_base = pygame.image.load("images/ralph.png")
        self.image = pygame.transform.scale(self.image_base, (150, 150))
        self.rect = self.image.get_rect()
        self.x_positions = [
            (750 / 9) + 150,
            (750 / 9) * 2 + 150,
            (750 / 9) * 3 + 150,
            (750 / 9) * 4 + 150,
            (750 / 9) * 5 + 150,
        ]
        self.rect.center = (self.x_positions[2], 80)
        self.current_position = 2
        self.move_img = 0

    def move(self):
        """
        Moves Ralph to a random x position within the bounds of the game window.
        """
        self.rect.center = (self.next_position(), 80)

    def next_position(self):
        """
        Determines the next x position index for Ralph to move to.

        Returns:
            int: the index of the next x position in self.x_positions
        """
        if self.current_position == 0:
            self.current_position += 1
        elif self.current_position == 4:
            self.current_position -= 1
        else:
            self.current_position += random.choice([1, -1])
        return self.x_positions[self.current_position]

    def animate(self):
        """
        Alternates between Ralph's two images for animation.
        """
        if self.move_img == 0:
            self.image = pygame.image.load("images/ralph_2.png")
            self.image = pygame.transform.scale(self.image, (150, 150))
            self.move_img = 1
        elif self.move_img == 1:
            self.image = pygame.image.load("images/ralph.png")
            self.image = pygame.transform.scale(self.image, (150, 150))
            self.move_img = 0
