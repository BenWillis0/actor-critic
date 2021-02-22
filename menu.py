import globalVars as g
import pygame
import os

def endScreen():
    pygame.draw.rect(g.screen,(255,255,255),((0,0),(g.screenWidth,g.screenHeight)))

    pygame.font.init()
    font = pygame.font.SysFont('Arial', 60)
        
    if g.loss:
        textSurface = font.render('You Lose', False, (0,0,0))
    if g.win:
        textSurface = font.render('You Win', False, (0,0,0))
    g.screen.blit(textSurface,(g.screenWidth/2-textSurface.get_width()/2,g.screenHeight/2 - 100))
        
    font = pygame.font.SysFont('Arial', 30)
    textSurface = font.render('Zombies killed: ' + str(g.zombiesDead), False, (0,0,0))
    g.screen.blit(textSurface,(g.screenWidth/2-textSurface.get_width()/2,g.screenHeight/2))

    textSurface = font.render('Humans killed: ' + str(g.humansDead), False, (0,0,0))
    g.screen.blit(textSurface,(g.screenWidth/2-textSurface.get_width()/2,g.screenHeight/2 + 35))

    textSurface = font.render('Humans infected: ' + str(g.humansToZombie), False, (0,0,0))
    g.screen.blit(textSurface,(g.screenWidth/2-textSurface.get_width()/2,g.screenHeight/2 + 70))
    g.main_screen.blit(g.screen, (0,0))
    pygame.display.update()
    

def startScreen(play_button, train_button, load_button):
    pygame.draw.rect(g.screen,(255,255,255),((0,0),(g.screenWidth,g.screenHeight)))
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 60)
    textSurface = font.render('Menu', False, (0,0,0))
    g.screen.blit(textSurface,(g.screenWidth/2-textSurface.get_width()/2,g.screenHeight/2 - 200))


    pygame.draw.rect(g.screen, (192,192,192), play_button)
    pygame.draw.rect(g.screen, (192,192,192), train_button)
    pygame.draw.rect(g.screen, (192,192,192), load_button)

    font = pygame.font.SysFont('Arial', 40)
    textSurface = font.render('Play', False, (0,0,0))
    g.screen.blit(textSurface,(g.screenWidth/2-textSurface.get_width()/2 - 150 - train_button.w/2,g.screenHeight/2-50-textSurface.get_height()/2+play_button.h/2))

    textSurface = font.render('Train', False, (0,0,0))
    g.screen.blit(textSurface,(g.screenWidth/2-textSurface.get_width()/2,g.screenHeight/2-50-textSurface.get_height()/2+train_button.h/2))

    textSurface = font.render('Load', False, (0, 0, 0))
    g.screen.blit(textSurface, (g.screenWidth / 2 - textSurface.get_width() / 2 + 150 + train_button.w/2, g.screenHeight / 2 - 50 - textSurface.get_height() / 2 + load_button.h / 2))

    g.main_screen.blit(g.screen, (0,0))
    pygame.display.update()

def training_screen(save_button, evaluate_button):
    g.button_screen.fill((255,255,255))
    pygame.draw.rect(g.button_screen, (192, 192, 192), save_button)
    pygame.draw.rect(g.button_screen, (192, 192, 192), evaluate_button)

    pygame.font.init()
    font = pygame.font.SysFont('Arial', 40)
    text_surface = font.render('Save', False, (0,0,0))
    g.button_screen.blit(text_surface,(g.button_surface_width/2-text_surface.get_width()/2,save_button.h/2-text_surface.get_height()/2+25))

    text_surface = font.render('Evaluate', False, (0,0,0))
    g.button_screen.blit(text_surface,(g.button_surface_width/2-text_surface.get_width()/2,evaluate_button.h/2-text_surface.get_height()/2+125))

    g.main_screen.blit(g.button_screen, (0, 0))
    g.main_screen.blit(g.button_screen, (0, 0))
    pygame.display.update()


def load_model():
    g.screen.fill((255,255,255))
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 60)
    textSurface = font.render('Choose model to load', False, (0, 0, 0))
    g.screen.blit(textSurface, (g.screenWidth / 2 - textSurface.get_width() / 2, 40))
    font = pygame.font.SysFont('Arial', 40)
    buttons = []
    dirs = os.listdir('models')
    for i in range(len(dirs)):
        button = pygame.Rect(150 + (i%6)*225, 150 + (i // 6) * 150, 150, 75)
        pygame.draw.rect(g.screen, (192, 192, 192), button)
        buttons.append(button)
        text_surface = font.render(dirs[i], False, (0,0,0))
        g.screen.blit(text_surface, (150 + (i%6)*225 + button.w/2 - text_surface.get_width()/2, 150 + (i // 6) * 150 + button.h/2 - text_surface.get_height()/2))
    g.main_screen.blit(g.screen, (0, 0))
    pygame.display.update()
    return buttons

def train_test():
    g.screen.fill((255,255,255))
    train_button = pygame.Rect(g.screenWidth/2 - 350, g.screenHeight/2-38, 200, 75)
    test_button = pygame.Rect(g.screenWidth/2 + 50, g.screenHeight/2-38, 200, 75)
    pygame.draw.rect(g.screen, (192, 192, 192), train_button)
    pygame.draw.rect(g.screen, (192, 192, 192), test_button)

    pygame.font.init()
    font = pygame.font.SysFont('Arial', 40)
    textSurface = font.render('Train', False, (0, 0, 0))
    g.screen.blit(textSurface, (g.screenWidth/2 - 350 + train_button.w/2 - textSurface.get_width()/2, g.screenHeight/2-38 + train_button.h/2 - textSurface.get_height()/2))
    textSurface = font.render('Test', False, (0, 0, 0))
    g.screen.blit(textSurface, (g.screenWidth/2 + 50 + test_button.w/2 - textSurface.get_width()/2, g.screenHeight/2-38 + test_button.h/2 - textSurface.get_height()/2))
    g.main_screen.blit(g.screen, (0, 0))
    pygame.display.update()
    return [train_button, test_button]
