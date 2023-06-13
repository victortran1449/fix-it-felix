import pygame

from components import Button, TextBox

from .base_screen import BaseScreen


class WelcomeScreen(BaseScreen):
    """
    A class representing the welcome screen of the game.
    """

    def __init__(self, window):
        """
        Initializes the welcome screen.

        Args:
            window (pygame.Surface): The window to draw the screen on.
        """
        super().__init__(window)
        self.sprites = pygame.sprite.Group()

        self.button1 = Button(200, 100, "START")
        self.button1.rect.x = 150
        self.button1.rect.y = 300
        self.button2 = Button(200, 100, "SCORES")
        self.button2.rect.x = 450
        self.button2.rect.y = 300

        self.heading = TextBox(
            value="Fix-It",
            size=(400, 150),
            font_size=70,
            font_style="fonts/ARCADE_N.TTF",
        )
        self.heading.rect.centerx = window.get_size()[0] / 2
        self.heading.rect.centery = window.get_size()[1] / 2 - 100

        self.textbox = TextBox(
            value="By Timur and Victor",
            size=(350, 100),
            font_size=18,
            font_style="fonts/ARCADE_N.TTF",
        )
        self.textbox.rect.centerx = window.get_size()[0] / 2
        self.textbox.rect.centery = window.get_size()[1] / 2 - 50

        self.persistent["all_scores"] = {}

        self.sprites.add(self.button1, self.button2, self.heading, self.textbox)
        self.sprites.add()

    def update(self):
        """
        Updates the welcome screen.
        """
        self.textbox.update()
        self.heading.update()

    def draw(self):
        """
        Draws the welcome screen.
        """
        self.window.fill((255, 255, 255))
        self.sprites.draw(self.window)

    def manage_event(self, event):
        """
        Manages events on the welcome screen.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        self.next_screen = False
        if event.type == pygame.MOUSEBUTTONDOWN:

            # You can set the lvl, score, and lives here before starting the game for testing purposes
            if self.button1.rect.collidepoint(event.pos):
                self.persistent["lvl"] = 1
                self.persistent["score"] = 0
                self.persistent["lives"] = 3
                self.persistent["time"] = 0
                self.running = False
                self.next_screen = "transition"

            if self.button2.rect.collidepoint(event.pos):
                self.running = False
                self.next_screen = "scores"
