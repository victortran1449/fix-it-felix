import pygame


class Door(pygame.sprite.Sprite):
    """
    A class representing a broken door in a game.
    """

    def __init__(self):
        """
        Initializes a new instance of the Window class.
        """
        super().__init__()
        self.image_base = pygame.image.load("images/broken_door.png")
        self.image = pygame.transform.scale(self.image_base, (100, 170))
        self.rect = self.image.get_rect()
        self.rect.center = ((750 / 9) * 3 + 150, 500)
        self.broken_value = 2
        self.is_fixed = False

    def fix_door(self):
        """
        Attempts to fix the door by decrementing the broken value.
        If the broken value is 1, the image of the door is changed to represent a half-broken door.
        If the broken value is 0, the image of the door is changed to represent a fixed door.
        """
        if self.broken_value > 0:
            self.broken_value -= 1
        else:
            self.broken_value = -1
        if self.broken_value == 1:
            self.image_base = pygame.image.load("images/half_door.png")
            self.image = pygame.transform.scale(self.image_base, (100, 170))

        if self.broken_value == 0:
            self.is_fixed = True
            self.image_base = pygame.image.load("images/fixed_door.png")
            self.image = pygame.transform.scale(self.image_base, (100, 170))
