import pygame


class Button(pygame.sprite.Sprite):
    """
    A class representing a clickable button in a game.
    """

    def __init__(self, width, height, text, bgcolor=(0, 0, 0), fgcolor=(255, 255, 255)):
        """
        Initialize the Button sprite with a specified width, height, text, and colors.
        
        Args:
            width (int): The width of the button in pixels.
            height (int): The height of the button in pixels.
            text (str): The text to be displayed on the button.
            bgcolor (tuple): The background color of the button in RGB format.
            fgcolor (tuple): The text color of the button in RGB format.
        """
        super().__init__()
        pygame.font.init()
        font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.image = pygame.Surface((width, height))
        self.image.fill(bgcolor)
        text_surface = font.render(text, True, fgcolor)
        text_size = font.size(text)
        pos_x = (width - text_size[0]) / 2
        pos_y = (height - text_size[1]) / 2
        self.image.blit(text_surface, (pos_x, pos_y))
        self.rect = self.image.get_rect()
