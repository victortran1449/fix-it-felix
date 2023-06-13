import pygame


class BaseScreen:
    """
    Base class for a screen.
    """

    def __init__(self, window):
        """
        Initializes the base screen.
        """
        self.window = window
        self.next_screen = False
        self.persistent = {}
        self.clock = pygame.time.Clock()
        self.persistent["all_scores"] = {}
        # self.persistent["score"] = 0

    def run(self):
        """
        Runs the pygame event loop
        """
        self.running = True
        while self.running:
            self.clock.tick(60)
            self.update()
            self.draw()
            pygame.display.update()

            # Default event management
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.manage_event(event)

    @property
    def rect(self):
        return self.window.get_rect()

    def draw(self):
        pass

    def update(self):
        pass

    def manage_event(self, event):
        pass
