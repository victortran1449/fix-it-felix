import pygame
import random


class Cake(pygame.sprite.Sprite):
    """
    A class representing a cake object in a game.
    """

    def __init__(self):
        """
        Initialize the Cake sprite with a random position on the screen.
        """
        super().__init__()
        self.image_base = pygame.image.load("images/cake.png")
        self.image = pygame.transform.scale(self.image_base, (50, 60))
        self.rect = self.image.get_rect()
        self.x_positions = [
            (750 / 9) + 150,
            (750 / 9) * 2 + 150,
            (750 / 9) * 3 + 150,
            (750 / 9) * 4 + 150,
            (750 / 9) * 5 + 150,
        ]
        self.y_positions = [530, 370, 230]
        self.rect.center = (
            self.x_positions[random.randint(0, 4)],
            self.y_positions[random.randint(0, 2)] + 5,
        )
