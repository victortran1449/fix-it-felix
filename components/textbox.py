import pygame


class TextBox(pygame.sprite.Sprite):
    """
    A class that represents a text box.
    """

    def __init__(self, value=0, size=(50, 50), font_size=24, font_color=(0,0,0), font_style=pygame.font.get_default_font(), bg_color=((255, 255, 255))):
        """
        Initializes the TextBox object.

        Args:
            value (int or str): The initial value (text) of the text box. Default is 0.
            size (tuple): The size of the text box. Default is (50, 50).
            font_size (int): The size of the font used in the text box. Default is 24.
            font_color (tuple): The color of the font used in the text box. Default is black (0, 0, 0).
            font_style (str): The font style used in the text box. Default is pygame's default font.
            bg_color (tuple): The background color of the text box. Default is white (255, 255, 255).
        """
        super().__init__()
        self.value = value

        pygame.font.init()
        self.image = pygame.Surface(size)
        self.font = pygame.font.Font(font_style, font_size)
        self.rect = self.image.get_rect()

        self.font_color = font_color
        self.bg_color = bg_color

    def update(self):
        """
        Updates the TextBox object.

        Renders the font with the current value, fills the image with the background color,
        and blits the font onto the image.
        """
        font_surface = self.font.render(str(self.value), True, self.font_color)
        self.image.fill(self.bg_color)
        self.image.blit(font_surface, (0, 0))
