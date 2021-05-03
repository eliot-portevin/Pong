import pygame, sys


class Game:
    def __init__(self, win, W, H):
        self.W = W
        self.H = H
        self.WINDOW = win
        self.playing = False
        self.pause_screen = False
        self.wait = False
        self.end = False
        self.time = 0
        self.mouse_rect = pygame.Rect((0, 0, 1, 1))

        # Colours
        self.white = (200, 200, 200)
        self.black = pygame.Color('grey12')
        self.black_transparent = (0, 0, 0, 30)

        # Main menu variables
        self.main_menu = True
        self.show_prompt = True
        self.menu_font = pygame.font.SysFont('toonaround', 50)
        self.menu_font2 = pygame.font.SysFont('toonaround', 55)
        self.menu_prompt = self.menu_font.render('Press Space to Continue', True, self.white)
        self.prompt_time = 0
        self.transparent_surface = pygame.Surface((W, H), pygame.SRCALPHA)
        self.transparent_surface.fill(self.black_transparent)

        # Pause Variables
        self.pause = False

        self.left_up = False  # Putting all these values to false
        self.left_down = False  # so the pads don't move alone
        self.right_up = False
        self.right_down = False

        # Score variables
        self.score_1 = 0
        self.score_2 = 0
        self.font = pygame.font.SysFont('toonaround', 35)

        self.left_pad = pygame.surface.Surface((10, 100))
        self.right_pad = pygame.surface.Surface((10, 100))
        self.left_pad.fill(self.white)
        self.right_pad.fill(self.white)

        self.x_left = 30
        self.y_left = H / 2 - self.left_pad.get_height() / 2
        self.x_right = W - 30
        self.y_right = H / 2 - self.left_pad.get_height() / 2

        self.ball = pygame.surface.Surface((20, 20))
        self.ball_speed_x = 5
        self.ball_speed_y = 5
        self.x_ball = W / 2
        self.y_ball = H / 2 - self.ball.get_height() / 2

    def move_pad(self):
        if self.right_up:
            if self.y_right > 10:
                self.y_right -= 5
        if self.right_down:
            if self.y_right < self.H - self.right_pad.get_height() - 10:
                self.y_right += 5

        if self.left_up:
            if self.y_left > 10:
                self.y_left -= 5
        if self.left_down:
            if self.y_left < self.H - self.left_pad.get_height() - 10:
                self.y_left += 5

    def update(self):
        self.move_pad()

        # Blitting everything to the screen
        self.WINDOW.fill(self.black)
        self.WINDOW.blit(self.left_pad, (self.x_left, self.y_left))
        self.WINDOW.blit(self.right_pad, (self.x_right, self.y_right))
        pygame.draw.rect(self.WINDOW, self.white, (self.W / 2 - 2, 0, 4, self.H))
        pygame.draw.circle(self.WINDOW, self.white, (self.x_ball, self.y_ball), 10)

        score1 = self.font.render(str(self.score_1), True, self.white)
        score2 = self.font.render(str(self.score_2), True, self.white)
        self.WINDOW.blit(score1, (self.W / 2 - 2 * score1.get_width(), self.H / 2 - score1.get_height() / 2))
        self.WINDOW.blit(score2, (self.W / 2 + score2.get_width(), self.H / 2 - score1.get_height() / 2))

        if self.wait:
            pygame.time.delay(800)
            self.wait = False

        # Checking for ball collision
        ball_rect = pygame.Rect((self.x_ball, self.y_ball, 20, 20))
        left_rect = pygame.Rect((self.x_left + 10, self.y_left, 15, 100))
        right_rect = pygame.Rect((self.x_right + 10, self.y_right, 15, 100))

        if self.x_ball < self.x_left + 10 or self.x_ball > self.x_right:
            if self.x_ball < 100:
                self.score_2 += 1
            else:
                self.score_1 += 1

            # Resetting all values
            self.x_ball = self.W / 2
            self.y_ball = self.H / 2 - 10
            self.wait = True
            self.y_left = self.H / 2 - self.left_pad.get_height() / 2
            self.y_right = self.H / 2 - self.left_pad.get_height() / 2
            self.ball_speed_x = self.ball_speed_x * (-1)
            self.ball_speed_x = 5
            self.ball_speed_y = 5

        if self.y_ball <= 10 or self.y_ball > self.H - 20:
            self.ball_speed_y = self.ball_speed_y * (-1)

        if ball_rect.colliderect(left_rect) or ball_rect.colliderect(right_rect):
            self.ball_speed_x = self.ball_speed_x * (-1)
        self.x_ball += self.ball_speed_x
        self.y_ball += self.ball_speed_y

        # Accelerating ball
        if pygame.time.get_ticks() - self.time > 10000:
            if self.ball_speed_x > 0:
                self.ball_speed_x += 1
            else:
                self.ball_speed_x -= 1

            if self.ball_speed_y > 0:
                self.ball_speed_y += 1
            else:
                self.ball_speed_y -= 1
            self.time = pygame.time.get_ticks()

    def menu(self):
        self.WINDOW.fill(self.black)
        self.WINDOW.blit(self.left_pad, (self.x_left, self.y_left))
        self.WINDOW.blit(self.right_pad, (self.x_right, self.y_right))
        pygame.draw.rect(self.WINDOW, self.white, (self.W / 2 - 2, 0, 4, self.H))
        pygame.draw.circle(self.WINDOW, self.white, (self.x_ball, self.y_ball), 10)
        if self.show_prompt:
            self.WINDOW.blit(self.menu_prompt, (self.W / 2 - self.menu_prompt.get_width() / 2, self.H / 2))
            self.WINDOW.blit(self.transparent_surface, (0, 0))
        if pygame.time.get_ticks() - self.prompt_time > 500:
            self.show_prompt = not self.show_prompt
            self.prompt_time = pygame.time.get_ticks()

        pygame.display.update()

    def stop_game(self):
        self.time = pygame.time.get_ticks()

        #Blit background to screen
        self.WINDOW.fill(self.black)
        self.WINDOW.blit(self.left_pad, (self.x_left, self.y_left))
        self.WINDOW.blit(self.right_pad, (self.x_right, self.y_right))
        pygame.draw.circle(self.WINDOW, self.white, (self.x_ball, self.y_ball), 10)
        self.WINDOW.blit(self.transparent_surface, (0, 0))

        #Middle Text
        text = self.font.render('Press Esc again to resume game', True, self.white)
        if self.show_prompt:
            self.WINDOW.blit(text, (self.W / 2 - text.get_width() / 2, self.H / 2.5))
        if pygame.time.get_ticks() - self.prompt_time > 500:
            self.show_prompt = not self.show_prompt
            self.prompt_time = pygame.time.get_ticks()


        #Menu button
        menu_button = self.menu_font.render('Menu', True, self.white)
        menu_button_hovering = self.menu_font2.render('Menu', True, self.white)
        self.mouse_rect.x, self.mouse_rect.y = pygame.mouse.get_pos()
        menu_rect = pygame.Rect((50, 50, menu_button.get_width(), menu_button.get_height()))
        if self.mouse_rect.colliderect(menu_rect):
            self.WINDOW.blit(menu_button_hovering, (47.5, 47.5))
            hovering = True
        else:
            self.WINDOW.blit(menu_button, (50, 50))
            hovering = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and hovering:
                self.end = True

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
