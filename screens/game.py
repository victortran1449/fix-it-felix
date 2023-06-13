import pygame
import random

from components import Felix, TextBox, Window, Ralph, Brick, Door, Life, Bird, Cake

from .base_screen import BaseScreen


class GameScreen(BaseScreen):
    """
    A class that represents the game screen.

    This class is responsible for managing the game's logic and rendering
    its visual components.
    """

    def __init__(self, window):
        """
        Initializes the game screen.

        Args:
            window (pygame.Surface): The window to draw the screen on.
        """
        super().__init__(window)

        # Layout of the windows (center x)
        self.x_positions = [
            (750 / 9) + 150,
            (750 / 9) * 2 + 150,
            (750 / 9) * 3 + 150,
            (750 / 9) * 4 + 150,
            (750 / 9) * 5 + 150,
        ]

        # Layout of the windows (center y)
        self.y_positions = [530, 370, 230]

        # Load and scale the building and window images
        self.building_base = pygame.image.load("images/building.png")
        self.building = pygame.transform.scale(self.building_base, (500, 1800))
        self.big_window_base = pygame.image.load("images/big_window.png")
        self.big_window_image = pygame.transform.scale(self.big_window_base, (100, 100))
        self.big_window_rect = self.big_window_image.get_rect()
        self.big_window_rect.center = (self.x_positions[2], 365)

        # Create all the sprites and sprite groups for the game
        self.felix = Felix()
        self.window_list = [Window() for x in range(13)]
        self.door = Door()
        self.ralph = Ralph()
        self.bricks = pygame.sprite.Group()
        self.birds = pygame.sprite.Group()

        # Create the score and pause message text boxes
        self.scorebox = TextBox(
            size=(100, 50),
            font_color=(255, 255, 255),
            bg_color=(0, 0, 0),
            font_style="fonts/ARCADE_N.TTF",
        )
        self.pause_msg = TextBox(
            value="PAUSED",
            size=(330, 64),
            font_size=70,
            font_color=(255, 255, 255),
            bg_color=(0, 0, 0),
            font_style="fonts/ARCADE_N.TTF",
        )
        self.timer_box = TextBox(
            size=(100, 50),
            font_color=(255, 255, 255),
            bg_color=(0, 0, 0),
            font_style="fonts/ARCADE_N.TTF",
        )

        # Set initial values for game variables (that DON'T use lvl data)
        self.ralph_counter = 0
        self.felix_counter = 0
        self.animate_counter = 0
        self.fix_time = None
        self.collision_counter = 0
        self.throw_brick = True
        self.lvl_updated = False
        self.lives_updated = False
        self.spawn_bird = False
        self.bird_counter = 0
        self.invincible = False
        self.invincible_counter = 0
        self.cake = None
        self.cake_counter = 0
        self.pause = False
        self.timer_counter = 0

    def update(self):
        """
        Updates the game state by updating variables and game objects.

        This method updates the persistent data based on the game level, sets
        up the window lives and sprites, and manages the timing of the
        bricks thrown by Ralph. It also manages the movement and collision of
        game objects like Ralph, Felix, bricks, and birds.
        """
        # Set initial values for game variables (that DO use lvl data)
        if self.lvl_updated is False:
            self.ralph_throw_speed = 95 - 5 * self.persistent["lvl"]
            self.ralph_walk_speed = 55 - 5 * self.persistent["lvl"]
            self.brick_speed = 3 + self.persistent["lvl"]
            self.brick_chance = 0.60 + self.persistent["lvl"] * 0.01
            self.throw_delay = max((10 - int(self.persistent["lvl"] * 0.8)), 2)
            self.bird_chance = 400 - ((self.persistent["lvl"] - 4) * 30)
            self.bird_speed = 4 + ((self.persistent["lvl"] - 4) * 0.5)
            self.animate_speed = 40 - self.persistent["lvl"] * 2
            self.cake_spawn_speed = 500 - ((self.persistent["lvl"] - 5) * 40)
            self.lvl_updated = True

        # Increment the time by 1 every 60 ticks
        self.timer_counter += 1
        if self.timer_counter == 60:
            self.persistent["time"] += 1
            self.timer_counter = 0

        # Update the timer box
        self.timer_box.value = self.persistent["time"]
        self.timer_box.update()

        # Update the lives once lvl starts and when Felix is hit
        if self.lives_updated is False:
            self.life_x_position = 680
            self.lives = pygame.sprite.Group()
            self.lives.add(Life() for i in range(self.persistent["lives"]))
            for life in self.lives:
                life.rect.center = (self.life_x_position, 20)
                self.life_x_position += 45
            self.lives_updated = True

        # Add the bricks to sprite group
        self.brick = Brick(self.brick_speed)
        self.brick.rect.center = self.ralph.rect.center
        self.ralph_counter += 1
        if self.throw_brick:
            if self.ralph_counter == self.throw_delay:
                self.bricks.add(self.brick)
            elif self.ralph_counter == self.throw_delay * 2:
                self.bricks.add(self.brick)
            elif self.ralph_counter == self.throw_delay * 3:
                self.bricks.add(self.brick)

        # Update Ralph and decide weather to throw bricks
        if self.ralph_counter == self.ralph_throw_speed:
            self.ralph.move()
            self.ralph_counter = 0
            self.throw_brick = True
            if random.random() > self.brick_chance:
                self.ralph_counter = self.ralph_walk_speed
                self.throw_brick = False

        # Drop the bricks and check for collision with Felix
        self.collision_counter += 1
        for brick in self.bricks:
            brick.drop()
            if (
                self.felix.rect.colliderect(brick.rect)
                and self.collision_counter > 45
                and self.invincible is False
            ):
                self.lives_updated = False
                if self.persistent["lives"] == 1:
                    self.running = False
                    self.next_screen = "game_over"
                self.persistent["lives"] -= 1
                self.collision_counter = 0

        # If enough time has passed since self.felix.fix(), set Felix's image back
        self.felix_counter += 1
        if self.fix_time:
            if self.felix_counter - self.fix_time > 5:
                self.felix.back()
                self.fix_time = None

        # Spawn the birds. If the player's level is greater than 4, enable bird spawning.
        # If bird spawning is enabled and enough time has passed, spawn a new bird.
        self.bird_counter += 1
        if self.persistent["lvl"] > 4:
            self.spawn_bird = True
        if self.spawn_bird:
            if self.bird_counter > self.bird_chance:
                self.random_index = random.randint(0, 2)
                self.bird = Bird(self.bird_speed)
                self.bird.rect.centery = self.y_positions[self.random_index]
                self.birds.add(self.bird)
                self.bird_counter = 0

        # Move all birds and check for collisions with Felix
        for bird in self.birds:
            bird.move()
            if (
                self.felix.rect.colliderect(bird.rect)
                and self.collision_counter > 30
                and self.invincible is False
            ):
                self.lives_updated = False
                if self.persistent["lives"] == 1:
                    self.running = False
                    self.next_screen = "game_over"
                self.persistent["lives"] -= 1
                self.collision_counter = 0

        # Timer for invincibility
        self.invincible_counter += 1
        if self.invincible and self.invincible_counter > 150:
            self.invincible = False
            self.cake_counter = 0

        # Spawn cake depending on the lvl and time
        self.cake_counter += 1
        if (
            not self.cake
            and self.persistent["lvl"] > 4
            and self.cake_counter == self.cake_spawn_speed
        ):
            self.cake = Cake()

        # Set limited amount of time the cake is available
        if self.cake and self.cake_counter == self.cake_spawn_speed + 200:
            self.cake = None
            self.cake_counter = 0

        # If a cake is currently on the screen and Felix collides with it, make Felix invincible
        if self.cake:
            if self.felix.rect.colliderect(self.cake.rect):
                self.invincible = True
                self.invincible_counter = 0
                self.cake = None

        # Update the scorebox
        self.scorebox.value = self.persistent["score"]
        self.scorebox.update()

        # Update the pause message
        self.pause_msg.update()

        # If enough time has passed, animate Ralph
        self.animate_counter += 1
        if self.animate_counter == self.animate_speed:
            self.ralph.animate()
            self.animate_counter = 0

    def draw(self):
        """
        Draw the game screen with all its elements.
        """
        # Fill the screen with black
        self.window.fill((0, 0, 0))

        # Draw the background building image
        self.window.blit(self.building, (150, -1210))

        # Draw the score box
        self.window.blit(self.scorebox.image, self.scorebox.rect)

        # Draw the timer box
        self.window.blit(self.timer_box.image, (self.timer_box.rect[0], self.timer_box.rect[1] + 25))

        # Center the pause message on the screen
        self.pause_msg.rect.centerx = self.window.get_size()[0] / 2
        self.pause_msg.rect.centery = self.window.get_size()[1] / 2

        # Draw the windows
        window_count = 0
        door = False
        big_window = False
        for x in self.x_positions:
            for y in self.y_positions:
                # Draw the door on the 6th window
                if window_count == 6 and door is False:
                    self.window.blit(self.door.image, self.door.rect)
                    door = True
                # Draw the big window on the 7th window
                elif window_count == 6 and big_window is False:
                    self.window.blit(self.big_window_image, self.big_window_rect)
                    big_window = True
                # Draw a normal window for all other windows
                else:
                    self.window_list[window_count].rect.center = (x, y)
                    self.window.blit(
                        self.window_list[window_count].image,
                        self.window_list[window_count].rect,
                    )
                    window_count += 1

        # Draw the invincibility mask on Felix if he's invincible
        if self.invincible:
            offset = 3
            self.window.blit(
                self.felix.mask_image, (self.felix.rect[0] + offset, self.felix.rect[1])
            )
            self.window.blit(
                self.felix.mask_image, (self.felix.rect[0] - offset, self.felix.rect[1])
            )
            self.window.blit(
                self.felix.mask_image, (self.felix.rect[0], self.felix.rect[1] - offset)
            )
            self.window.blit(
                self.felix.mask_image, (self.felix.rect[0], self.felix.rect[1] + offset)
            )

        # Draw Felix and Ralph sprites
        self.window.blit(self.ralph.image, self.ralph.rect)
        self.window.blit(self.felix.image, self.felix.rect)

        # Draw the cake sprite if there is one
        if self.cake:
            self.window.blit(self.cake.image, self.cake.rect)

        # Draw the brick sprites if there are any
        if self.bricks:
            self.bricks.draw(self.window)

        # Draw the bird sprites if there are any
        if self.birds:
            self.birds.draw(self.window)

        # Draw the lives sprites
        self.lives.draw(self.window)

    def manage_event(self, event):
        """
        Manages events on the game screen.

        Args:
            event (pygame.event.Event): The event to handle.
        """

        if event.type == pygame.KEYDOWN:
            # Move Felix
            if event.key == pygame.K_LEFT:
                self.felix.move("left")
            if event.key == pygame.K_RIGHT:
                self.felix.move("right")
            if event.key == pygame.K_UP:
                self.felix.move("up")
            if event.key == pygame.K_DOWN:
                self.felix.move("down")

            # Pause the game when the Escape key is pressed, and display pause message
            if event.key == pygame.K_ESCAPE:
                self.pause = True
            while self.pause:
                self.window.blit(self.pause_msg.image, self.pause_msg.rect)
                pygame.display.update()

                # Handle events while paused
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        return
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.pause = False
                        return

            # Fix a window or door when the space key is pressed. If the window
            # or door is fully fixed, add to scorebox
            if event.key == pygame.K_SPACE:
                self.felix.fix()
                self.fix_time = self.felix_counter
                window_index = self.felix.rect.collidelist(
                    [fix_window.rect for fix_window in self.window_list]
                )
                if window_index != -1:
                    self.window_list[window_index].fix_window()
                    if self.window_list[window_index].broken_value == 0:
                        self.persistent["score"] += int(
                            10 * ((self.persistent["lvl"] + 1) / 2)
                        )
                if self.felix.rect.colliderect(self.door.rect):
                    self.door.fix_door()
                    if self.door.broken_value == 0:
                        self.persistent["score"] += int(
                            10 * ((self.persistent["lvl"] + 1) / 2)
                        )

                # Check if all windows and the door are fixed, update game state and move to next screen
                if (
                    False not in [window.is_fixed for window in self.window_list]
                    and self.door.is_fixed is True
                ):
                    self.update()
                    self.running = False
                    self.persistent["score"] = self.scorebox.value
                    self.persistent["lvl"] += 1
                    if self.persistent["lvl"] == 16:
                        self.next_screen = "game_over"
                    else:
                        self.next_screen = "transition"
