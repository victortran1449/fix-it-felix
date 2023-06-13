import pygame


class Window(pygame.sprite.Sprite):
    """
    A class that represents a broken window in a game.
    """

    def __init__(self):
        """
        Initializes a new instance of the Window class.
        """
        super().__init__()
        self.image_base = pygame.image.load("images/broken_window.png")
        self.image = pygame.transform.scale(self.image_base, (70, 100))
        self.rect = self.image.get_rect()
        self.broken_value = 2
        self.is_fixed = False

    def fix_window(self):
        """
        Attempts to fix the window by decrementing the broken value.
        If the broken value is 1, the image of the window is changed to represent a half-broken window.
        If the broken value is 0, the image of the window is changed to represent a fixed window.
        """
        if self.broken_value > 0:
            self.broken_value -= 1
        else:
            self.broken_value = -1
        if self.broken_value == 1:
            self.image_base = pygame.image.load("images/half_window.png")
            self.image = pygame.transform.scale(self.image_base, (70, 100))

        if self.broken_value == 0:
            self.is_fixed = True
            self.image_base = pygame.image.load("images/fixed_window.png")
            self.image = pygame.transform.scale(self.image_base, (70, 100))
