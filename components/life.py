import pygame


class Life(pygame.sprite.Sprite):
    """
    A class representing Felix's lives.
    """

    def __init__(self):
        """
        Initialize the Life sprite.
        """
        super().__init__()
        self.image_base = pygame.image.load("images/life.png")
        self.image = pygame.transform.scale(self.image_base, (40, 40))
        self.rect = self.image.get_rect()
