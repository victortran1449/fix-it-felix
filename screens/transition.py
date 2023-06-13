import pygame

from components import TextBox
from .base_screen import BaseScreen


class TransitionScreen(BaseScreen):
    """
    A class representing the transition screen displayed between levels.
    """

    def __init__(self, window):
        """
        Initializes the transition screen.

        Args:
            window (pygame.Surface): The window to draw the screen on.
        """
        super().__init__(window)
        self.sprites = pygame.sprite.Group()

        self.heading = TextBox(
            value="",
            size=(340, 100),
            font_size=40,
            font_color=(255, 255, 255),
            bg_color=(0, 0, 0),
            font_style='fonts/ARCADE_N.TTF'
        )
        self.heading.rect.centerx = window.get_size()[0] / 2 + 30
        self.heading.rect.centery = window.get_size()[1] / 2
        self.sprites.add(self.heading)

        self.counter = 0

    def update(self):
        """
        Updates the value of the heading TextBox, as well as
        manages the delay before the game starts.
        """
        self.heading.value = f"Level {self.persistent['lvl']}"
        self.heading.update()

        self.counter += 1
        if self.counter > 140:
            self.counter = 0
            self.next_screen = "game"
            self.running = False

    def draw(self):
        """
        Fills the screen with black color and draws the sprites on it.
        """
        self.window.fill((0, 0, 0))
        self.sprites.draw(self.window)

    def manage_event(self, event):
        pass
