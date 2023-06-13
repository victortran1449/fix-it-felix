import pygame
import json

from screens import (
    GameOverScreen,
    GameScreen,
    WelcomeScreen,
    ScoresScreen,
    TransitionScreen,
)


class App:
    """
    This is the main class for our application.
    It runs the "screens" and manages state (persistent data).
    """

    def __init__(self):
        """
        Creates a Pygame window
        """
        self.window = pygame.display.set_mode((800, 600))
        self.persistent = {}
        self.persistent['lvl'] = 0

        with open('database.json', 'r') as fp:
            self.persistent["all_scores"] = json.load(fp)

    def run(self):
        """
        This method runs the main loop, and switches between screens using the next_screen attribute.
        """
        screens = {
            "welcome": WelcomeScreen(self.window),
            "game": GameScreen(self.window),
            "game_over": GameOverScreen(self.window),
            "scores": ScoresScreen(self.window),
            "transition": TransitionScreen(self.window),
        }
        running = True
        current_screen = "welcome"
        new_game_created = False
        while running:
            # Gets the screen instance to "run"
            screen = screens.get(current_screen)
            if not screen:
                raise RuntimeError(f"Screen {current_screen} not found!")

            if current_screen == "game_over" or current_screen == "transition":
                if not new_game_created:
                    screens["game"] = GameScreen(self.window)
                    new_game_created = True
            if current_screen == "game":
                new_game_created = False

            # Updates the persistent data on the instance
            screen.persistent = self.persistent
            # Runs the main loop of the screen
            screen.run()
            # Exits the loop if necessary
            if screen.next_screen is False:
                running = False
            # Switch to the next screen and update the persistent data
            current_screen = screen.next_screen
            self.persistent = screen.persistent


if __name__ == "__main__":
    g = App()
    g.run()
