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
        self.bird_frame = 0
        original_bird_images = [
            pygame.image.load(f"images/chicken/flying/frame-{i}.png")
            for i in [1, 2, 3, 4]
        ]
        self.bird_imgs = [
            pygame.transform.rotozoom(x, 0, 1/16).convert_alpha()
            for x in original_bird_images
        ]
        original_bg_images = [
            pygame.image.load(f"images/background/layer_{i}.png")
            for i in [1, 2, 3]
        ]
        self.bg_imgs = [
            pygame.transform.rotozoom(x, 0, 600 / x.get_height()).convert_alpha()
            for x in original_bg_images
        ]

    def init_objects(self):
        self.bird_y_speed = 0
        self.bird_pos = (200, 000)
        self.bird_lift = False
        self.bg0_pos = 0
        self.bg1_pos = 0
        self.bg2_pos = 0

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
        self.bg0_pos -= 0.25
        self.bg1_pos -= 0.5
        self.bg2_pos -= 2

        bird_y = self.bird_pos[1]

        if self.bird_lift:
            # Lintua nostetaan (0.5 px nostovauhtia / frame)
            self.bird_y_speed -= 0.5
            self.bird_frame += 1
        else:
            # Painovoima (lisää putoamisnopeutta joka kuvassa)
            self.bird_y_speed += 0.2

        # Liikuta lintua sen nopeuden verran
        bird_y += self.bird_y_speed

        self.bird_pos = (self.bird_pos[0], bird_y)

    def update_screen(self):
        # Täytä tausta vaaleansinisellä
        #self.screen.fill((230, 230, 255))

        self.screen.blit(self.bg_imgs[0], (self.bg0_pos, 0))
        self.screen.blit(self.bg_imgs[1], (self.bg1_pos, 0))
        self.screen.blit(self.bg_imgs[2], (self.bg2_pos, 0))

        # Piirrä lintu
        angle = -90 * 0.04 * self.bird_y_speed
        angle = max(min(angle, 60), -60)

        bird_img_i = self.bird_imgs[(self.bird_frame // 3) % 4]

        bird_img = pygame.transform.rotozoom(bird_img_i, angle, 1)
        self.screen.blit(bird_img, self.bird_pos)

        pygame.display.flip()


if __name__ == "__main__":
    main()
