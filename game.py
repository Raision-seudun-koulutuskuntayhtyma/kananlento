import pygame


def main():
    game = Game()
    game.run()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.running = False
        self.init_graphics()
        self.init_objects()

    def init_graphics(self):
        img_bird1 = pygame.image.load("images/chicken/flying/frame-1.png")
        self.img_bird1 = pygame.transform.rotozoom(img_bird1, 0, 1/16)

    def init_objects(self):
        self.bird_y_speed = 0
        self.bird_pos = (200, 000)
        self.bird_lift = False

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
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    self.bird_lift = True
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    self.bird_lift = False

    def handle_game_logic(self):
        bird_y = self.bird_pos[1]

        if self.bird_lift:
            # Lintua nostetaan (8 px / frame)
            self.bird_y_speed -= 1
        else:
            # Painovoima (lisää putoamisnopeutta joka kuvassa)
            self.bird_y_speed += 0.2


        # Liikuta lintua sen nopeuden verran
        bird_y += self.bird_y_speed


        self.bird_pos = (self.bird_pos[0], bird_y)

    def update_screen(self):
        # Täytä tausta vaaleansinisellä
        self.screen.fill((230, 230, 255))

        # Piirrä lintu
        self.screen.blit(self.img_bird1, self.bird_pos)

        pygame.display.flip()


if __name__ == "__main__":
    main()
