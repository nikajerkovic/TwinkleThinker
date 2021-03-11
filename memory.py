import pygame
import random
import os
from settings import *

game_folder = os.path.dirname(__file__)
image_folder = os.path.join(game_folder,"img")


pos = [(x,y) for x in range (1, 8) for y in range (1, 8)]
screen= pygame.display.set_mode((WIDTH, HEIGHT)) 

def game_init():
    global font
    pygame.init()
    pygame.mixer.init()                        
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()                 
    font = pygame.font.SysFont("Arial", 16)

class Stars(pygame.sprite.Sprite):
    def __init__(self, number):
        super(Stars, self).__init__()
        self.number = number
        self.make_image()

    def make_image(self):
        self.x, self.y = self.random_pos()
        self.image = pygame.image.load(os.path.join(image_folder,"thestar.png")).convert()
        self.image = pygame.transform.scale(self.image,(50,50))                                                    
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.number = str(self.number)
        self.text = font.render(self.number, 1, (0, 0, 0))
        text_rect = self.text.get_rect(center=(50 // 2, 50 // 2))                                                    
        self.image.blit(self.text, text_rect)

    def random_pos(self):
        global pos
        position = random.choice(pos)
        x, y = position
        del pos[pos.index(position)]            
        x = x * 50
        y = y * 50
        return x, y


           
def game_over_screen(score):
        
        
    maxscore = get_maxscore()
    #pygame.font.init()
    font = pygame.font.SysFont("Arial", 16)
    font_GO = pygame.font.Font('freesansbold.ttf', 60)
    font_NG = pygame.font.Font('freesansbold.ttf', 20)
            
    text_HighScore = font.render(''f"High score: {maxscore}", True, LIGHT_YELLOW, BLUE)
    text_GameOver = font_GO.render('GAME OVER', True, LIGHT_YELLOW,BLUE)
    text_Score = font.render(''f"Score: {score}", True, LIGHT_YELLOW, BLUE)
    text_NewGame = font_NG.render('Click anywhere to start new game', True, LIGHT_YELLOW, BLUE)
                
    textRect_HS = text_HighScore.get_rect() 
    textRect_GO = text_GameOver.get_rect()
    textRect_S = text_Score.get_rect()
    textRect_NG = text_NewGame.get_rect() 

    textRect_HS.center = (WIDTH// 2, (3*HEIGHT) // 4)
    textRect_GO.center = (WIDTH// 2, HEIGHT // 3)
    textRect_S.center = (WIDTH// 2, (5*HEIGHT) // 8)  
    textRect_NG.center = (WIDTH//2, (4*HEIGHT) // 8)
  
    screen.fill(BLUE) 
    screen.blit(text_HighScore, textRect_HS)
    screen.blit(text_GameOver, textRect_GO)
    screen.blit(text_Score, textRect_S)  
    screen.blit(text_NewGame, textRect_NG)
                        
            
def hide_stars():                                                   
    global pos
                        
    for sprite in g: 
        bgd = pygame.image.load(os.path.join(image_folder,"thestar.png")).convert()                                                        
        bgd = pygame.transform.scale(bgd,(50,50)) 
        sprite.image.blit(bgd,(0,0)) 

   
    pos = [(x, y) for x in range(1, 8) for y in range(1, 8)]

def clear_screen():  
        global num_order, counter_on, stars_visible
        num_order = []
        counter_on = 1
        stars_visible = 1

def mouse_collision(sprite):
    global num_order, score, maxscore
    global counter_on, max_count

    x, y = pygame.mouse.get_pos() 

    if sprite.rect.collidepoint(x, y):  
        click.play()
        num_order.append(sprite.number)
        
        sprite.rect = pygame.Rect(-50, -50, 50, 50)
           
        if sprite.number != str(len(num_order)):                   
            clear_screen()
            game_over_screen(score)                                       
            loop = 1

            while loop :                                                          
                   
                for event in pygame.event.get() :                                
                    
                    if event.type == pygame.QUIT : 
                        
                        pygame.quit()
                        quit() 

                    elif event.type == pygame.MOUSEBUTTONDOWN:                           

                        score = 0
                        counter = 0
                        num_order = []
                        game_init()
                        max_count = 100
                        
                      
                        for s in g:                                                
                            g.remove(s)
                        stars_init()         
                        [s.make_image() for s in g]
                        pos = [(x, y) for x in range(1, 8) for y in range(1, 8)]

                        loop = 0
                            
                    else:
                        loop = 1
                        
                pygame.display.update()         

        else:
            score += 10
            if len(num_order) == len(g):
                score += 100
                if score > int(maxscore):
                    maxscore = score
                    set_score(maxscore)
                            
                g.add(Stars(len(g) + 1))
                max_count = max_count + 10
                clear_screen()
                [s.make_image() for s in g]
                


g = pygame.sprite.Group()
num_order = []
score = 0
bgd = pygame.Surface((50, 50))

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(22050, -16, 2, 512)
pygame.mixer.set_num_channels(32)
click = pygame.mixer.Sound("audio/click.wav")

def stars_init():
    for i in range(1, 4):
        g.add(Stars(i))


counter = 0
counter_on = 1
max_count = 80
stars_visible = 1
    

def get_maxscore() -> int:
    filename = "maxscore.txt"
    if filename in os.listdir():
        with open(filename, "r") as file:
            val = file.read()
            if val == "":
                maxscore = 0
            else:
                maxscore = int(val)
    else:
        maxscore = 0
    return maxscore

def set_score(maxscore) -> None:

    with open("maxscore.txt", "w") as file:
        file.write(str(maxscore))


maxscore = get_maxscore()



def main():
    global counter_on, counter, max_count, stars_visible
    global click, score, g

    game_init()
    stars_init()
    clock = pygame.time.Clock()
    loop = 1
    stars = pygame.image.load("img/starfield2.png")
    

    while loop:
        screen.blit(pygame.transform.scale(stars, (WIDTH, HEIGHT)), (0, 0))
        if counter_on:
            text = font.render("time: " + str(max_count - counter), 1, (255, 244, 0))
            screen.blit(text, (300, 0))
            text = font.render("Memory: " + str(score), 1, (255, 244, 0))
            record = font.render("Record: " + str(maxscore), 1, (255, 244, 0))
            screen.blit(text, (0, 0))
            screen.blit(record, (150, 0))
            counter += 1
            if counter % 4 == 0:
                click.play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop = 0
                if event.key == pygame.K_r:
                    num_order = []
                    for s in g:
                        g.remove(s)
                    screen.fill((0,0,0))
                    pos = [(x, y) for x in range(1, 8) for y in range(1, 8)]
                    couter = 0
                    counter_on = 1
                    score = 0
                    main()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if stars_visible:
                    hide_stars()
                    stars_visible = 0
                    counter_on = 0
                    counter = 0
                for s in g:
                    mouse_collision(s)    

        g.draw(screen)
        if counter == max_count:
            hide_stars()
            counter = 0
            counter_on = 0

        pygame.display.update()
        clock.tick(50)

    pygame.quit()

def start_menu(screen):
    font_title = pygame.font.Font('freesansbold.ttf',40)
    font_start = pygame.font.Font('freesansbold.ttf',20)

    text_title = font_title.render('TWINKLE THINKER', True, LIGHT_YELLOW)
    text_start = font_start.render('Click anywhere to start game', True, LIGHT_YELLOW)

    textRect_title= text_title.get_rect()
    textRect_start = text_start.get_rect() 

    textRect_title.center = (WIDTH// 2, HEIGHT // 3)
    textRect_start.center = (WIDTH// 2, (5*HEIGHT) // 8)

    run=True
    while run:
        
        pygame.display.set_caption(TITLE) 
        screen.fill(BLUE)
        screen.blit(text_title, textRect_title)
        screen.blit(text_start, textRect_start)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                main()

start_menu(screen)