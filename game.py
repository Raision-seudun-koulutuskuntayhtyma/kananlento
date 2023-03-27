import pygame


def main():
    game = Game()
    game.run()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.running = False

    def run(self):
        clock = pygame.time.Clock()
        self.running = True
        while self.running:
            self.handle_events()
            self.handle_game_logic()
            self.update_screen()
            # Odota niin kauan, että ruudun päivitysnopeus on 60fps
            clock.tick(60)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def handle_game_logic(self):
        pass

    def update_screen(self):
        self.screen.fill((230, 230, 255))
        pygame.display.flip()


if __name__ == "__main__":
    main()
