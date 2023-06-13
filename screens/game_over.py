import pygame

from components import Button, TextBox

from .base_screen import BaseScreen


class GameOverScreen(BaseScreen):
    """
    A class representing the game over screen of the game.
    """

    def __init__(self, window):
        """
        Initializes the game over screen.

        Args:
            window (pygame.Surface): The window to draw the screen on.
        """
        super().__init__(window)

        self.sprites = pygame.sprite.Group()

        self.button1 = Button(200, 100, "Again")
        self.button1.rect.x = 150
        self.button1.rect.y = 400
        self.button2 = Button(200, 100, "Quit")
        self.button2.rect.x = 450
        self.button2.rect.y = 400

        self.textbox = TextBox(value="", size=(1000, 100))
        self.textbox.rect.x = 50
        self.textbox.rect.y = 150

        self.sprites.add(self.button1, self.button2, self.textbox)

        self.saved_score = False

    def update(self):
        """
        Displays the final score in the textbox and saves the score to the persistent data.
        """
        if not self.saved_score:
            # Get the scores from the persistent data and display the final score in the textbox
            self.scores = self.persistent["all_scores"]
            if self.persistent["lvl"] == 16:
                self.textbox.value = f'You won! Your Final score is {self.persistent.get("score")} and you took {self.persistent["time"]} seconds.'
            else:
                self.textbox.value = f'You died. Your Final score is {self.persistent.get("score")} and you took {self.persistent["time"]} seconds.'
            self.textbox.update()

            # Save the final score to the persistent data
            attempts = len(self.scores) + 1
            self.scores[f"Attempt {attempts}"] = self.persistent.get("score")
            self.persistent["all_scores"] = self.scores
            self.saved_score = True

    def draw(self):
        """
        Draw the sprites in the game over screen.
        """
        self.window.fill((255, 255, 255))
        self.sprites.draw(self.window)

    def manage_event(self, event):
        """
        Manages events on the game over screen.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button2.rect.collidepoint(event.pos) or event.type == pygame.QUIT:
                self.next_screen = False
                self.running = False
            if self.button1.rect.collidepoint(event.pos):
                self.running = False
                self.saved_score = False
                self.next_screen = "welcome"
