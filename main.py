import pygame, sys
from game import Game


def main():
    pygame.init()
    W, H = 1000, 700
    WINDOW = pygame.display.set_mode((W, H))

    game = Game(WINDOW, W, H)

    not_quit = True

    while not_quit:
        clock = pygame.time.Clock()
        fps = 60

        while game.main_menu:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game.main_menu = False
                        game.playing = True
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            game.menu()

        while game.playing:
            clock.tick(fps)
            if not game.pause_screen:
                game.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        game.left_up = True
                    elif event.key == pygame.K_s:
                        game.left_down = True
                    if event.key == pygame.K_UP:
                        game.right_up = True
                    elif event.key == pygame.K_DOWN:
                        game.right_down = True
                    if event.key == pygame.K_ESCAPE:
                        game.pause_screen = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        game.left_up = False
                    elif event.key == pygame.K_s:
                        game.left_down = False
                    if event.key == pygame.K_UP:
                        game.right_up = False
                    elif event.key == pygame.K_DOWN:
                        game.right_down = False

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            while game.pause_screen:
                game.stop_game()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            game.playing = True
                            game.pause_screen = False

                if game.end:
                    main()


            pygame.display.update()


if '__name__' == main():
    main()
