import pygame
import json

from components import Button, TextBox
from .base_screen import BaseScreen


class ScoresScreen(BaseScreen):
    """
    A screen to display and manage the top 5 scores of the game.
    """

    def __init__(self, window):
        """
        Initializes the scores screen.

        Args:
            window (pygame.Surface): The window to draw the screen on.
        """
        super().__init__(window)

        self.sprites = pygame.sprite.Group()

        self.button1 = Button(200, 100, "BACK")
        self.button1.rect.x = 500
        self.button1.rect.y = 450
        self.button2 = Button(200, 100, "SAVE")
        self.button2.rect.x = 500
        self.button2.rect.y = 300
        self.button3 = Button(200, 100, "CLEAR")
        self.button3.rect.x = 500
        self.button3.rect.y = 150

        self.heading = TextBox(value="", size=(500, 100), font_size=32)
        self.heading.rect.x = 100
        self.heading.rect.y = 100

        self.saved_message = TextBox(
            value="Scores saved.", size=(150, 25), font_size=18
        )
        self.saved_message.rect.x = 500
        self.saved_message.rect.y = 400

        self.sprites.add(self.button1, self.button2, self.heading, self.button3)

        # A list to hold top 5 scores
        self.scores_display = []

    def create_scores_textbox(self):
        """
        Creates a list of top 5 scores as text boxes, sorted in descending order.
        If there are no scores, a message is displayed instead.
        """
        if len(self.persistent["all_scores"]) != 0:
            top_5_sorted = sorted(
                self.persistent["all_scores"].items(), key=lambda x: x[1], reverse=True
            )[:5]
            for key, value in top_5_sorted:
                self.scores_display.append(
                    TextBox(value=f"{key} | {value}", size=(300, 100))
                )
        else:
            self.scores_display.append(
                TextBox(value="No scores to display...", size=(300, 500))
            )

    def update(self):
        """
        Updates the state of the screen.

        - Sets the heading to "Top 5 scores".
        - If the scores have not been created yet, calls create_scores_textbox() to create them.
        - Positions and updates all score text boxes and rank text boxes.
        - Updates the heading and saved message text boxes.
        """
        self.heading.value = "Top 5 scores: "

        if len(self.scores_display) == 0:
            self.create_scores_textbox()

            x_left_corner = 150
            y_left_corner = 200
            # Update the score
            for score in self.scores_display:
                score.rect.topleft = (x_left_corner, y_left_corner)
                score.image.fill((0, 0, 0))
                y_left_corner += 50
                score.update()
                self.sprites.add(score)

            y_left_corner = 200
            # Update the rank
            for top5 in range(5):
                rank_textbox = TextBox(value=f"#{top5 + 1} | ", size=(40, 25))
                rank_textbox.rect.topleft = (x_left_corner - 50, y_left_corner)
                y_left_corner += 50
                rank_textbox.update()
                self.sprites.add(rank_textbox)

        self.heading.update()
        self.saved_message.update()

    def draw(self):
        """
        Fills the screen with white color and draws the sprites on it.
        """
        self.window.fill((255, 255, 255))
        self.sprites.draw(self.window)

    def manage_event(self, event):
        """
        Manages events on the scores screen.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        self.next_screen = False
        if event.type == pygame.MOUSEBUTTONDOWN:

            # If the 'BACK' button is clicked, remove the 'saved_message' sprite, set 'self.running' to False, clear the
            # 'scores_display' list, and set 'self.next_screen' to 'welcome'.
            if self.button1.rect.collidepoint(event.pos):
                self.sprites.remove(self.saved_message)
                self.running = False
                self.scores_display = []
                self.next_screen = "welcome"

            # If the 'SAVE' button is clicked, write the current scores to a JSON file, add the 'saved_message' sprite to
            # the sprite group, and redraw the screen.
            if self.button2.rect.collidepoint(event.pos):
                with open("database.json", "w") as fp:
                    json.dump(self.persistent["all_scores"], fp)
                self.sprites.add(self.saved_message)
                self.draw()

            # If the 'CLEAR' button is clicked, clear the current scores from the JSON file, clear the 'all_scores'
            # dictionary, clear the 'scores_display' list, update the screen, and redraw the screen.
            if self.button3.rect.collidepoint(event.pos):
                with open("database.json", "w") as fp:
                    json.dump({}, fp)
                    self.persistent["all_scores"] = {}
                self.scores_display = []
                pygame.display.update()
                self.update()
                self.draw()
