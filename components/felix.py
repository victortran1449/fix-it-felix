import pygame


class Felix(pygame.sprite.Sprite):
    """
    A class representing Felix, the character that moves around and fixes things.
    """

    def __init__(self):
        """
        Initialize a new Felix object with the default image and position.
        """
        super().__init__()
        self.felix_base = pygame.image.load("images/felix.png")
        self.felix_image = pygame.transform.scale(self.felix_base, (60, 80))

        self.felix_fixing_base = pygame.image.load("images/felix_fixing.png")
        self.felix_fixing_image = pygame.transform.scale(
            self.felix_fixing_base, (80, 80)
        )

        self.image = self.felix_image
        self.rect = self.image.get_rect()
        self.x_positions = [
            (750 / 9) + 150,
            (750 / 9) * 2 + 150,
            (750 / 9) * 3 + 150,
            (750 / 9) * 4 + 150,
            (750 / 9) * 5 + 150,
        ]
        self.y_positions = [530, 370, 230]
        self.x_position_idx = 0
        self.y_position_idx = 0
        self.rect.center = (
            self.x_positions[self.x_position_idx],
            self.y_positions[self.y_position_idx],
        )
        self.set_mask(self.felix_image)

    def set_mask(self, image):
        """
        Set the mask and the mask image of Felix based on the given image.

        Args:
            image (pygame.Surface): the image to create the mask from
        """
        self.mask = pygame.mask.from_surface(image)
        self.mask_image = self.mask.to_surface()
        self.mask_image.set_colorkey((0, 0, 0))

        mask_w, mask_h = self.mask_image.get_size()
        for x in range(mask_w):
            for y in range(mask_h):
                if self.mask_image.get_at((x, y))[0] != 0:
                    self.mask_image.set_at((x, y), (0, 255, 0))

    def move(self, direction):
        """
        Move Felix in the given direction.

        Args:
            direction (str): the direction to move in ("up", "down", "left", or "right")
        """
        if direction == "right" and self.x_position_idx != 4:
            self.x_position_idx += 1
        if direction == "left" and self.x_position_idx != 0:
            self.x_position_idx -= 1
        if direction == "up" and self.y_position_idx != 2:
            self.y_position_idx += 1
        if direction == "down" and self.y_position_idx != 0:
            self.y_position_idx -= 1

        self.rect.center = (
            self.x_positions[self.x_position_idx],
            self.y_positions[self.y_position_idx],
        )

    def fix(self):
        """
        Changes the sprite image to Felix while he is fixing a door and updates the mask.
        """
        self.image = self.felix_fixing_image
        self.set_mask(self.felix_fixing_image)

    def back(self):
        """
        Changes the sprite image back to the default Felix image and updates the mask.
        """
        self.image = self.felix_image
        self.set_mask(self.felix_image)
