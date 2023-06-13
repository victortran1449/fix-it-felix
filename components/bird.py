import pygame


class Bird(pygame.sprite.Sprite):
    """
    A class representing a bird sprite in a game.
    """
    
    def __init__(self, speed):
        """
        Initialize the Bird sprite with a speed and image.
        
        Args:
            speed (int): The speed at which the Bird sprite moves.
        """
        super().__init__()
        self.image_base = pygame.image.load("images/bird.png")
        self.image = pygame.transform.scale(self.image_base, (50, 30))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.centerx = 800

    def move(self):
        """
        Move the Bird sprite to the left based on its speed.
        """
        self.rect.centerx -= self.speed
