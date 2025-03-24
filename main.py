import pygame
import sys
import asyncio
import random
# Initialize the Pygame library
pygame.init()
pygame.mixer.init()

async def main():
    # Load music
    #pygame.mixer.music.load('path/to/your/musicfile.mp3')

    # Load sound effect
    shuru = pygame.mixer.Sound('start.mp3')
    eat = pygame.mixer.Sound('eat.mp3')
    dead = pygame.mixer.Sound('dead2.mp3')
    bg = pygame.mixer.Sound('bg.mp3')

    # Create a screen object (using FULLSCREEN mode for adaptability)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Get screen width and height
    screen_width, screen_height = screen.get_width(), screen.get_height()
    if screen_width > screen_height:
        
        screen = pygame.display.set_mode((screen_height, screen_height-50))
        screen_width, screen_height = screen.get_width(), screen.get_height()

    #Colors
    white = (255, 255,255)
    red = (255, 0,0)
    yellow = (255, 255, 0)
    blue = (0, 0, 255)
    black = (0,0,0)
    # Set the caption of the window
    pygame.display.set_caption("Retro Naagin")
    pygame.display.update()

    font = pygame.font.Font("retrofont.TTF", screen_width // 16)



    def food():
        food_x = random.randint(screen_width // 12, screen_width - screen_width // 12)
        food_y = random.randint(screen_height // 12, screen_height // 2)
        return food_x, food_y

    def draw_snake(li):
        for x,y in li:
            pygame.draw.rect(screen, red, [x, y, screen_width // 12, screen_width // 12])



    def text_screen(text, color, x, y):
        screen_text = font.render(text, True, color)
        screen.blit(screen_text, [x,y])

    def game():
        
        head = pygame.Rect((screen_width // 2, screen_height // 3, screen_width // 12, screen_width // 12))
        
        exit = False
        gameOver = False

        vel_x = 0
        vel_y = 0
        vel = screen_width // 120

        clock=pygame.time.Clock()
        fps=60

        snake_len = 1
        snake_pos = []
        sc = 0
        
        food_x, food_y = food()
        snake_pos = [[head.x, head.y]]
        
        #mobile controls
        button_font = pygame.font.SysFont('Arial', 36)
        bu = button_font.render("↑", True, (255, 255, 0))
        bd = button_font.render("↓", True, (255, 255, 0))
        br = button_font.render("→", True, (255, 255, 0))
        bl = button_font.render("←", True, (255, 255, 0))

        but_bu = pygame.Rect(screen_width * 0.45, screen_height * 0.76, screen_width * 0.1, screen_width * 0.1)
        but_bl = pygame.Rect(screen_width * 0.35, screen_height * 0.84, screen_width * 0.1, screen_width * 0.1)
        but_br = pygame.Rect(screen_width * 0.55, screen_height * 0.84, screen_width * 0.1, screen_width * 0.1)
        but_bd = pygame.Rect(screen_width * 0.45, screen_height * 0.92, screen_width * 0.1, screen_width * 0.1)
        
        def hover(but, color1, color2):
            a, b = pygame.mouse.get_pos()
            if but.collidepoint(a, b):
                pygame.draw.rect(screen, color1, but, border_radius=10)
            else:
                pygame.draw.rect(screen, color2, but, border_radius=10)
        
        while not exit:
            screen.fill((0, 0, 20))
            
            # Mobile controls background
            pygame.draw.rect(screen, white, (0, screen_height * 0.75, screen_width, screen_height * 0.25))

            # Ensure buttons are drawn with enough contrast
            hover(but_bu, (50, 50, 50), (100, 100, 100))
            hover(but_bl, (50, 50, 50), (100, 100, 100))
            hover(but_br, (50, 50, 50), (100, 100, 100))
            hover(but_bd, (50, 50, 50), (100, 100, 100))

            screen.blit(bu, (but_bu.x + screen_width * 0.02, but_bu.y + screen_width * 0.01))
            screen.blit(bd, (but_bd.x + screen_width * 0.02, but_bd.y + screen_width * 0.01))
            screen.blit(bl, (but_bl.x + screen_width * 0.02, but_bl.y + screen_width * 0.01))
            screen.blit(br, (but_br.x + screen_width * 0.02, but_br.y + screen_width * 0.01))
    
            if gameOver:
                

                # Gradient Background
                for i in range(screen_height):
                    pygame.draw.line(screen, (255, 100 - i//10, 100 - i//10), (0, i), (screen_width, i))

                # Game Over Box
                but_dead = pygame.Rect(screen_width * 0.2, screen_height * 0.17, screen_width * 0.6, screen_height * 0.2)
                pygame.draw.rect(screen, (200, 0, 0), but_dead, border_radius=20)
                pygame.draw.rect(screen, (255, 50, 50), but_dead.inflate(10, 10), 5, border_radius=20)

                # Buttons
                but_rs = pygame.Rect(screen_width * 0.3, screen_height * 0.42, screen_width * 0.4, screen_height * 0.1)
                but_ex = pygame.Rect(screen_width * 0.3, screen_height * 0.55, screen_width * 0.4, screen_height * 0.1)

                hover(but_rs, (0, 255, 0), (0, 180, 0))  # Green restart button
                hover(but_ex, (255, 0, 0), (180, 0, 0))  # Red exit button

                text_screen("GAME OVER!", white, but_dead.x + screen_width * 0.05, but_dead.y + screen_height * 0.05)
                text_screen(f"Score   {sc * 5}", yellow, but_dead.x + screen_width * 0.15, but_dead.y + screen_height * 0.12)
                text_screen("Restart", white, but_rs.x + screen_width * 0.1, but_rs.y + screen_height * 0.02)
                text_screen("Quit", white, but_ex.x + screen_width * 0.15, but_ex.y + screen_height * 0.02)

                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit = True
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        a, b = pygame.mouse.get_pos()
                        if but_rs.collidepoint(a, b):
                            gameOver = False
                            shuru.play()
                            game()
                        elif but_ex.collidepoint(a, b):
                            exit = True
                            sys.exit(0)
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            gameOver = False
                            game()
                        if event.key == pygame.K_ESCAPE :
                            exit = True
                            sys.exit(0)
            
            else:
                for event in pygame.event.get():
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            vel_x = -vel
                            vel_y = 0
                        elif event.key == pygame.K_RIGHT:
                            vel_x = vel
                            vel_y = 0
                        elif event.key == pygame.K_UP:
                            vel_y = -vel
                            vel_x = 0
                        elif event.key == pygame.K_DOWN:
                            vel_y = vel
                            vel_x = 0
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        a, b = pygame.mouse.get_pos()
                        if but_bu.collidepoint(a, b):
                            vel_y = -vel
                            vel_x = 0
                        elif but_bd.collidepoint(a, b):
                            vel_y = vel
                            vel_x = 0
                        elif but_br.collidepoint(a, b):
                            vel_x = vel
                            vel_y = 0
                        elif but_bl.collidepoint(a, b):
                            vel_x = -vel
                            vel_y = 0
                    
                    if event.type == pygame.QUIT:
                        exit = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            exit = True
                            sys.exit(0)
                            
                head.x += vel_x
                head.y += vel_y
                
                #if abs(head.x - food_x)<15 and abs(head.y - food_y)<15:
                if abs(head.x - food_x) < screen_width // 20 and abs(head.y - food_y) < screen_width // 20:
                    eat.play()
                    snake_len += 5
                    food_x, food_y = food()
                    sc += 1
                    if vel<screen_width // 40:
                        vel+=0.7
                
                pygame.draw.rect(screen, yellow, (food_x, food_y, screen_width // 12, screen_width // 12))
                
                if len(snake_pos)>snake_len:
                    snake_pos.pop(0)
                    
                score = 'Score  ' + str(sc*5)
                text_screen(score, white, 5, 5)
                
                if head.x<0 or head.x>screen_width or head.y<0 or head.y>screen_height * 0.75:
                # print('game over')
                    dead.play()
                    gameOver = True
                
                l = [head.x, head.y]
                snake_pos.append(l)
                
                if l in snake_pos[:-2]:
                    dead.play()
                    gameOver = True
                
                draw_snake(snake_pos)
            
            pygame.display.update()
            clock.tick(fps)

    def rules_screen():
        """Displays the game rules screen."""
        rules_font = pygame.font.Font("retrofont.ttf", screen_width // 12)
        text_font = pygame.font.Font("retrofont.ttf", screen_width // 25)
        button_font = pygame.font.Font("retrofont.ttf", screen_width // 15)

        title = rules_font.render("GAME RULES", True, (255, 255, 0))
        rules_text = [
            "1 Use arrow keys or buttons to move",
            "2 Eat food to grow longer",
            "3 Avoid hitting the walls",
            "4 Do not collide with yourself!",
            "5 Score increases as you eat"
        ]

        but_back = pygame.Rect(screen_width * 0.3, screen_height * 0.75, screen_width * 0.4, screen_height * 0.08)
        back_text = button_font.render("BACK", True, black)

        clock = pygame.time.Clock()

        while True:
            for i in range(screen_height):
                pygame.draw.line(screen, (255, 100 - i // 10, 100 - i // 10), (0, i), (screen_width, i))

            pygame.draw.rect(screen, (0, 0, 50), (screen_width * 0.1, screen_height * 0.12, screen_width * 0.8, screen_height * 0.1), border_radius=10)
            screen.blit(title, (screen_width * 0.2, screen_height * 0.14))

            y_offset = screen_height * 0.3
            for rule in rules_text:
                rule_render = text_font.render(rule, True, black)
                screen.blit(rule_render, (screen_width * 0.1, y_offset))
                y_offset += screen_height * 0.08

            pygame.draw.rect(screen, (200, 200, 200), but_back, border_radius=10)
            screen.blit(back_text, (but_back.x + screen_width * 0.12, but_back.y + screen_height * 0.01))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if but_back.collidepoint(pygame.mouse.get_pos()):
                        return  # Return to main menu

            pygame.display.update()
            clock.tick(60)


    def main_menu():
        """Displays the main menu with Start, Rules, and Quit buttons."""
        menu_text = pygame.font.Font("retrofont.ttf", screen_width // 12)
        button_font = pygame.font.Font("retrofont.ttf", screen_width // 15)

        tt = menu_text.render("WELCOME TO THE GAME", True, (255, 255, 0))
        st = button_font.render("START", True, black)
        rl = button_font.render("RULES", True, black)
        qt = button_font.render("QUIT", True, black)

        but_tt = pygame.Rect(screen_width * 0.08, screen_height * 0.12, screen_width * 0.85, screen_height * 0.1)
        but_st = pygame.Rect(screen_width * 0.25, screen_height * 0.38, screen_width * 0.5, screen_height * 0.08)
        but_rl = pygame.Rect(screen_width * 0.25, screen_height * 0.48, screen_width * 0.5, screen_height * 0.08)
        but_qt = pygame.Rect(screen_width * 0.25, screen_height * 0.58, screen_width * 0.5, screen_height * 0.08)

        clock = pygame.time.Clock()
        fps = 60

        def hover(but, color1, color2):
            a, b = pygame.mouse.get_pos()
            if but.collidepoint(a, b):
                pygame.draw.rect(screen, color1, but, border_radius=10)
            else:
                pygame.draw.rect(screen, color2, but, border_radius=10)

        while True:
            for i in range(screen_height):
                pygame.draw.line(screen, (255, 100 - i // 10, 100 - i // 10), (0, i), (screen_width, i))

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if but_st.collidepoint(mouse_pos):
                        shuru.play()
                        game()
                    elif but_rl.collidepoint(mouse_pos):
                        rules_screen()
                    elif but_qt.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit(0)
                    elif event.key == pygame.K_RETURN:
                        shuru.play()
                        game()

            hover(but_st, (0, 255, 0), (0, 128, 0))
            hover(but_rl, (255, 255, 0), (180, 180, 0))
            hover(but_qt, (255, 0, 0), (128, 0, 0))
            pygame.draw.rect(screen, (0, 0, 50), but_tt, border_radius=10)

            screen.blit(tt, (but_tt.x + screen_width * 0.04, but_tt.y + screen_height * 0.02))
            screen.blit(st, (but_st.x + screen_width * 0.1, but_st.y + screen_height * 0.01))
            screen.blit(rl, (but_rl.x + screen_width * 0.1, but_rl.y + screen_height * 0.01))
            screen.blit(qt, (but_qt.x + screen_width * 0.1, but_qt.y + screen_height * 0.01))

            pygame.display.update()
            clock.tick(fps)


    main_menu()
    await asyncio.sleep(0)
    
asyncio.run(main())
