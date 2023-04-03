import pygame


def main():
    game = Game()
    game.run()


DEFAULT_SCREEN_SIZE = (800, 450)

class Game:
    def __init__(self):
        pygame.init()
        self.is_fullscreen = False
        self.screen = pygame.display.set_mode(DEFAULT_SCREEN_SIZE)
        self.screen_w = self.screen.get_width()
        self.screen_h = self.screen.get_height()
        self.running = False
        self.init_graphics()
        self.init_objects()

    def init_graphics(self):
        original_bird_images = [
            pygame.image.load(f"images/chicken/flying/frame-{i}.png")
            for i in [1, 2, 3, 4]
        ]
        self.bird_imgs = [
            pygame.transform.rotozoom(x, 0, self.screen_h / 9600).convert_alpha()
            for x in original_bird_images
        ]
        original_bird_dead_images = [
            pygame.image.load(f"images/chicken/got_hit/frame-{i}.png")
            for i in [1, 2]
        ]
        self.bird_dead_imgs = [
            pygame.transform.rotozoom(img, 0, self.screen_h / 9600).convert_alpha()
            for img in original_bird_dead_images
        ]
        original_bg_images = [
            pygame.image.load(f"images/background/layer_{i}.png")
            for i in [1, 2, 3]
        ]
        self.bg_imgs = [
            pygame.transform.rotozoom(
                img, 0, self.screen_h / img.get_height()
            ).convert_alpha()
            for img in original_bg_images
        ]
        self.bg_widths = [img.get_width() for img in self.bg_imgs]
        self.bg_pos = [0, 0, 0]

    def init_objects(self):
        self.bird_alive = True
        self.bird_y_speed = 0
        self.bird_pos = (self.screen_w / 3, self.screen_h / 4)
        self.bird_angle = 0
        self.bird_frame = 0
        self.bird_lift = False

    def scale_positions(self, scale_x, scale_y):
        self.bird_pos = (self.bird_pos[0] * scale_x, self.bird_pos[1] * scale_y)
        self.bg_pos[0] = self.bg_pos[0] * scale_x
        self.bg_pos[1] = self.bg_pos[1] * scale_x
        self.bg_pos[2] = self.bg_pos[2] * scale_x

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
                elif event.key in (pygame.K_f, pygame.K_F11):
                    self.toggle_fullscreen()
                elif event.key in (pygame.K_r, pygame.K_RETURN):
                    self.init_objects()

    def toggle_fullscreen(self):
        old_w = self.screen_w
        old_h = self.screen_h
        if self.is_fullscreen:
            pygame.display.set_mode(DEFAULT_SCREEN_SIZE)
            self.is_fullscreen = False
        else:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.is_fullscreen = True
        screen = pygame.display.get_surface()
        self.screen_w = screen.get_width()
        self.screen_h = screen.get_height()
        self.init_graphics()
        self.scale_positions(
            scale_x=(self.screen_w / old_w),
            scale_y=(self.screen_h / old_h),
        )

    def handle_game_logic(self):
        if self.bird_alive:
            self.bg_pos[0] -= 0.5
            self.bg_pos[1] -= 1
            self.bg_pos[2] -= 3

        bird_y = self.bird_pos[1]

        if self.bird_alive and self.bird_lift:
            # Lintua nostetaan (0.5 px nostovauhtia / frame)
            self.bird_y_speed -= 0.5
        else:
            # Painovoima (lisää putoamisnopeutta joka kuvassa)
            self.bird_y_speed += 0.2

        if self.bird_lift or not self.bird_alive:
            self.bird_frame += 1

        # Liikuta lintua sen nopeuden verran
        bird_y += self.bird_y_speed

        if self.bird_alive:  # Jos lintu on elossa
            # Laske linnun asento
            self.bird_angle = -90 * 0.04 * self.bird_y_speed
            self.bird_angle = max(min(self.bird_angle, 60), -60)

        # Tarkista onko lintu pudonnut maahan
        if bird_y > self.screen_h * 0.78:
            bird_y = self.screen_h * 0.78
            self.bird_y_speed = 0
            self.bird_alive = False

        # Aseta linnun x-y-koordinaatit self.bird_pos-muuttujaan
        self.bird_pos = (self.bird_pos[0], bird_y)

    def update_screen(self):
        # Täytä tausta vaaleansinisellä
        #self.screen.fill((230, 230, 255))

        # Piirrä taustakerrokset (3 kpl)
        for i in [0, 1, 2]:
            # Ensin piirrä vasen tausta
            self.screen.blit(self.bg_imgs[i], (self.bg_pos[i], 0))
            # Jos vasen tausta ei riitä peittämään koko ruutua, niin...
            if self.bg_pos[i] + self.bg_widths[i] < self.screen_w:
                # ...piirrä sama tausta vielä oikealle puolelle
                self.screen.blit(
                    self.bg_imgs[i],
                    (self.bg_pos[i] + self.bg_widths[i], 0)
                )
            # Jos taustaa on jo siirretty sen leveyden verran...
            if self.bg_pos[i] < -self.bg_widths[i]:
                # ...niin aloita alusta
                self.bg_pos[i] += self.bg_widths[i]

        # Piirrä lintu
        if self.bird_alive:
            bird_img_i = self.bird_imgs[(self.bird_frame // 3) % 4]
        else:
            bird_img_i = self.bird_dead_imgs[(self.bird_frame // 10) % 2]
        bird_img = pygame.transform.rotozoom(bird_img_i, self.bird_angle, 1)
        self.screen.blit(bird_img, self.bird_pos)

        pygame.display.flip()


if __name__ == "__main__":
    main()
