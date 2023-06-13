import pygame


class Brick(pygame.sprite.Sprite):
    """
    A class representing a brick sprite in a game.
    """

    def __init__(self, speed):
        """
        Initialize the Brick sprite with a speed and image.

        Args:
            speed (int): The speed at which the Brick sprite drops.
        """
        super().__init__()
        self.image_base = pygame.image.load("images/brick.png")
        self.image = pygame.transform.scale(self.image_base, (50, 20))
        self.rect = self.image.get_rect()
        self.speed = speed

    def drop(self):
        """
        Move the Brick sprite down based on its speed.
        """
        self.rect.centery = self.rect.centery + self.speed
