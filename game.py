import pygame

from menu import Menu
from obstacle import Obstacle

DEFAULT_SCREEN_SIZE = (800, 450)
FPS_TEXT_COLOR = (128, 0, 128)  # dark purple
SCORE_TEXT_COLOR = (0, 64, 160)  
TEXT_COLOR = (128, 0, 0)  # dark red

DEBUG = 0

def main():
    game = Game()
    game.run()


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.menu = Menu([
            "New Game",
            "High Scores",
            "About",
            "Quit",
        ])
        self.is_fullscreen = False
        self.is_in_menu = True
        self.show_fps = True
        self.screen = pygame.display.set_mode(DEFAULT_SCREEN_SIZE)
        self.screen_w = self.screen.get_width()
        self.screen_h = self.screen.get_height()
        self.running = False
        self.font16 = pygame.font.Font("fonts/SyneMono-Regular.ttf", 16)
        self.init_graphics()
        self.init_objects()

    def init_graphics(self):
        self.menu.set_font_size(int(48 * self.screen_h / 450))
        big_font_size = int(96 * self.screen_h / 450)
        self.font_big = pygame.font.Font("fonts/SyneMono-Regular.ttf", big_font_size)
        original_bird_images = [
            pygame.image.load(f"images/chicken/flying/frame-{i}.png")
            for i in [1, 2, 3, 4]
        ]
        self.bird_imgs = [
            pygame.transform.rotozoom(x, 0, self.screen_h / 9600).convert_alpha()
            for x in original_bird_images
        ]
        self.bird_radius = self.bird_imgs[0].get_height() / 2  # Likiarvo
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
        self.score = 0
        self.bird_alive = True
        self.bird_y_speed = 0
        self.bird_pos = (self.screen_w / 3, self.screen_h / 4)
        self.bird_angle = 0
        self.bird_frame = 0
        self.bird_lift = False
        self.obstacles: list[Obstacle] = []
        self.add_obstacle()

    def add_obstacle(self):
        obstacle = Obstacle.make_random(self.screen_w, self.screen_h)
        self.obstacles.append(obstacle)

    def remove_oldest_obstacle(self):
        self.obstacles.pop(0)

    def scale_positions(self, scale_x, scale_y):
        self.bird_pos = (self.bird_pos[0] * scale_x, self.bird_pos[1] * scale_y)
        for i in range(len(self.bg_pos)):
            self.bg_pos[i] = self.bg_pos[i] * scale_x

    def run(self):
        self.running = True

        while self.running:
            # Käsittele tapahtumat (eventit)
            self.handle_events()

            # Pelin logiikka (liikkumiset, painovoima, yms.)
            self.handle_game_logic()

            # Päivitä näyttö
            self.update_screen()

            # Päivitä näytölle piirretyt asiat näkyviin
            pygame.display.flip()

            # Odota niin kauan, että ruudun päivitysnopeus on 60fps
            self.clock.tick(60)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if not self.is_in_menu:
                        self.bird_lift = True
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_f, pygame.K_F11):
                    self.toggle_fullscreen()
                elif self.is_in_menu:
                    if event.key == pygame.K_UP:
                        self.menu.select_previous_item()
                    elif event.key == pygame.K_DOWN:
                        self.menu.select_next_item()
                    elif event.key == pygame.K_RETURN:
                        item = self.menu.get_selected_item()
                        if item == "New Game":
                            self.is_in_menu = False
                            self.init_objects()
                        elif item == "High Scores":
                            pass  # TODO: Implement High Score view
                        elif item == "About":
                            pass  # TODO: Implement About view
                        elif item == "Quit":
                            self.running = False
                elif event.key in (pygame.K_SPACE, pygame.K_UP):
                    self.bird_lift = False
                elif event.key == pygame.K_ESCAPE or not self.bird_alive:
                    self.is_in_menu = True

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
        if self.is_in_menu:
            return

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
        if bird_y > self.screen_h * 0.82:
            bird_y = self.screen_h * 0.82
            self.bird_y_speed = 0
            self.bird_alive = False

        # Aseta linnun x-y-koordinaatit self.bird_pos-muuttujaan
        self.bird_pos = (self.bird_pos[0], bird_y)

        # Lisää uusi este, kun viimeisin este on yli ruudun puolivälin
        if self.obstacles[-1].position < self.screen_w / 2:
            self.add_obstacle()

        # Poista vasemmanpuoleisin este, kun se menee pois ruudulta
        if not self.obstacles[0].is_visible():
            self.remove_oldest_obstacle()
            self.score += 1

        # Siirrä esteitä sopivalla nopeudella ja tarkista törmäys
        self.bird_collides_with_obstacle = False
        for obstacle in self.obstacles:
            if self.bird_alive:
                obstacle.move(self.screen_w * 0.005)
            if obstacle.collides_with_circle(self.bird_pos, self.bird_radius):
                self.bird_collides_with_obstacle = True
        
        if self.bird_collides_with_obstacle:
            self.bird_alive = False

    def update_screen(self):
        # Täytä tausta vaaleansinisellä
        #self.screen.fill((230, 230, 255))

        # Piirrä taustakerrokset (3 kpl)
        for i in range(len(self.bg_imgs)):
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

        if self.is_in_menu:
            self.menu.render(self.screen)
            return

        for obstacle in self.obstacles:
            obstacle.render(self.screen)

        # Piirrä lintu
        if self.bird_alive:
            bird_img_i = self.bird_imgs[(self.bird_frame // 3) % 4]
        else:
            bird_img_i = self.bird_dead_imgs[(self.bird_frame // 10) % 2]
        bird_img = pygame.transform.rotozoom(bird_img_i, self.bird_angle, 1)
        bird_x = self.bird_pos[0] - bird_img.get_width() / 2 * 1.25
        bird_y = self.bird_pos[1] - bird_img.get_height() / 2
        self.screen.blit(bird_img, (bird_x, bird_y))

        # Piirrä pisteet
        score_text = f"{self.score}"
        score_img = self.font_big.render(score_text, True, SCORE_TEXT_COLOR)
        score_pos = (self.screen_w * 0.95 - score_img.get_width(),
                     self.screen_h - score_img.get_height())
        self.screen.blit(score_img, score_pos)

        # Piirrä GAME OVER -teksti
        if not self.bird_alive:
            game_over_img = self.font_big.render("GAME OVER", True, TEXT_COLOR)
            x = self.screen_w / 2 - game_over_img.get_width() / 2
            y = self.screen_h / 2 - game_over_img.get_height() / 2
            self.screen.blit(game_over_img, (x, y))

        # Piirrä kehittämistä helpottava ympyrä
        if DEBUG:
            color = (0, 0, 0) if not self.bird_collides_with_obstacle else (255, 0, 0)
            pygame.draw.circle(self.screen, color, self.bird_pos, self.bird_radius)

        # Piirrä FPS luku
        if self.show_fps:
            fps_text = f"{self.clock.get_fps():.1f} fps"
            fps_img = self.font16.render(fps_text, True, FPS_TEXT_COLOR)
            self.screen.blit(fps_img, (0, 0))


if __name__ == "__main__":
    main()
