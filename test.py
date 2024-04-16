import pygame
import sys

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed_x = 0
        self.speed_y = 0

    def handle_movement(self):
        self.speed_x = 0
        self.speed_y = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -5
        if keys[pygame.K_RIGHT]:
            self.speed_x = 5
        if keys[pygame.K_UP]:
            self.speed_y = -5
        if keys[pygame.K_DOWN]:
            self.speed_y = 5

    def update(self):
        self.handle_movement()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

# Define the main game class
class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the screen
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Space Shooter")

        # Create the player object
        self.player = Player("sprites/player.png", self.WIDTH // 2, self.HEIGHT // 2)

        # Create a sprite group for the player
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

    def run(self):
        # Game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update
            self.all_sprites.update()

            # Draw
            self.screen.fill((0, 0, 0))
            self.all_sprites.draw(self.screen)

            # Refresh the display
            pygame.display.flip()

            # Cap the frame rate
            pygame.time.Clock().tick(60)

        # Quit Pygame
        pygame.quit()
        sys.exit()

# Instantiate and run the game
game = Game()
game.run()