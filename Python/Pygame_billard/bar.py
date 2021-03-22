import pygame

def bar():
    #pygame.init()

    screen = pygame.display.set_mode((300, 200))
    clock = pygame.time.Clock()
    FONT = pygame.font.Font(None, 36)
    BACKGROUND_COLOR = (237, 225, 192)
    LIGHT_GRAY = (0, 120, 120)
    GRAY = (30, 30, 30)

    # Button variables.
    button_rect = pygame.Rect(50, 100, 200, 80)
    max_width = 200  # Maximum width of the rect.
    max_time = 10  # Time after which the button should be filled.
    # Coefficient to calculate the width of the rect for a given time.
    coefficient = max_width / max_time
    time = 0

    dt = 0
    done = False
    col=False
    #while not done:
     #   for event in pygame.event.get():
      #      if event.type == pygame.QUIT:
       #         done = True
            

    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        # If mouse is over the button, increase the timer.
        if pygame.mouse.get_pressed()[2]:
            return time
        if time < max_time:  # Stop increasing if max_time is reached.
            time += dt
            
            if time >= max_time:
                time = 0

    else:  # If not colliding, reset the time.
        time=0
            

    width = time * coefficient

    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, LIGHT_GRAY, (51, 100, width, 80))
    pygame.draw.rect(screen, GRAY, button_rect, 2)
    txt = FONT.render(str(round(time, 2)), True, GRAY)
    screen.blit(txt, (20, 20))

    pygame.display.flip()
    dt = 0.01

    #pygame.quit()
    
#a=bar()
#print(a)
