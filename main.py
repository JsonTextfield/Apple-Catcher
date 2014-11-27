from __future__ import division
import math
import random
import sys
import pygame
import os
import time

class Apple(object):
    def __init__(self, position, direction, image):
        self.position = position
        self.direction = direction
        self.image = image

    def update(self):
        self.position = self.position[0]+self.direction[0], \
                        self.position[1]+self.direction[1]
        self.direction = self.direction[0], self.direction[1] + 1/5

    def draw(self, surface):
        rect = self.image.get_rect()
        rect = rect.move(int(self.position[0]) - rect.width//2, \
                         int(self.position[1]) - rect.height//2)
        surface.blit(self.image, rect)

    def radius(self):
        return self.image.get_height()

class MyGame(object):        
    
    REFRESH, START, RESTART, TIMEREVENT, TIMEOUTEVENT = \
    range(pygame.USEREVENT, pygame.USEREVENT+5)
    
    PLAYING, DYING, GAME_OVER, STARTING, HIGHSCORES = range(5)
        
        
    def __init__(self):
        """Initialize a new game"""
        mixer.init()
        mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()

        info = pygame.display.Info()        
        if android:
            self.size = (info.current_w, info.current_h)
        else:
            self.size = (500, 700)
        self.width, self.height = self.size
        self.screen = pygame.display.set_mode(self.size)
        self.bg_color = ((random.randint(0,255)),(random.randint(0,255)),
                        (random.randint(0,255)))
        if self.bg_color[0] > 200 and self.bg_color[1] > 200 \
        and self.bg_color[2] > 200 or self.bg_color[0] > 230 \
        and self.bg_color[1] < 40 and self.bg_color[2] < 40:
            self.bg_color = ((random.randint(0,255)),(random.randint(0,255)),
                        (random.randint(0,255)))
        self.score = 0
        self.level = 1
        
        #loads fonts
        self.font = pygame.font.SysFont(None, 50)
        self.gamefont = pygame.font.Font("webster.ttf", 20)
        self.game_over_font = pygame.font.Font("webster.ttf", 50)
        self.title_font = pygame.font.Font("Alpha Romanie G98.ttf", 80)
        self.score_font = pygame.font.Font("Alpha Romanie G98.ttf", 20)
        
        # load images
        self.apple = pygame.image.load('apple1.png')
        self.apples = set()      
        self.basket = pygame.image.load("basket2.png")
        
        #load sounds
        
        self.bgm = mixer.Sound("bgm.wav")
        self.basket_snd = mixer.Sound("basketed.wav")
        self.levelup = mixer.Sound("LevelUp.wav")
        self.gameover = mixer.Sound("gameover.wav")
        self.bgm.set_volume(.3)
        #self.bgm.play(-1, 0, 2000)
        
        self.title = self.title_font.render("Apple Catcher", True, \
                                           (255,200,100))
        self.playgame_txt = self.gamefont.render('Click to Play', 
        True, (255,255,255))
        self.high_txt = self.gamefont.render('High Scores', 
        True, (255,255,255))
        
        self.start_time = pygame.time.get_ticks()
        self.state = MyGame.STARTING
        self.timeout = 30
        self.quota = 25
        self.quota_inc = 27

        # Setup a timer to refresh the display FPS times per second
        self.FPS = 30
        self.x = 4000
        pygame.time.set_timer(pygame.USEREVENT+6, self.x)
        pygame.time.set_timer(MyGame.REFRESH, 1000//self.FPS)
        
        self.recttext = self.playgame_txt.get_rect()
        self.hs = self.high_txt.get_rect()
        self.title_rect = self.title.get_rect()
        
        self.scores = self.score_font.render("%s" %(str(open("scores.txt","r").read().upper().split("-")).replace("\"]","")), True, (255,255,255))
        #self.scores = self.score_font.render("-Tommy 145\n-Billy 152\n-Mandy 139\n-Bobby 172-",True,(255,255,255))
        #.replace("[",""),True, (255,255,255))
        
    
        self.myrect = self.scores.get_rect()
        self.sell = self.gamefont.render('Main Menu', 
                    True, (255,255,255))
        self.retrect = self.sell.get_rect()
    def restart(self):
        self.level = 1
        self.score = 0
        self.timeout = 30
        self.quota = 25
        self.quota_inc = 27
        self.start()
        return self.timeout
        
    def start(self):
        self.apples = set()
        self.new_apple()
        """Start playing (again)"""
        self.bgm.play(-1)
        self.start_time = pygame.time.get_ticks()
        self.state = MyGame.PLAYING
        
        
    def run(self):
        """Loop forever processing events"""
        running = True

        while running:
            if self.bg_color[0] > 200 and self.bg_color[1] > 200 \
            and self.bg_color[2] > 200 or self.bg_color[0] > 230 \
            and self.bg_color[1] < 40 and self.bg_color[2] < 40:
                self.bg_color = ((random.randint(0,255)),(random.randint(0,255)),
                        (random.randint(0,255)))
            event = pygame.event.wait()
            
            if android:
                if android.check_pause():
                    android.wait_for_resume()
            
            if event.type == pygame.USEREVENT+6:
                self.new_apple()
            # time to draw a new frame
            elif event.type == MyGame.REFRESH and\
            self.state != MyGame.GAME_OVER:
                self.draw()

            # player is asking to quit
            elif event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN and self.recttext.collidepoint(pygame.mouse.get_pos()) \
                    and self.state == MyGame.STARTING:
                self.restart()
                
            elif event.type == pygame.MOUSEBUTTONDOWN and self.hs.collidepoint(pygame.mouse.get_pos()):
                self.state = MyGame.HIGHSCORES
               
            elif event.type == pygame.MOUSEBUTTONDOWN and self.retrect.collidepoint(pygame.mouse.get_pos()):
                self.state = MyGame.STARTING
                    
            elif event.type == MyGame.RESTART:
                pygame.time.set_timer(MyGame.RESTART, 0) # turn this timer off
                self.state = MyGame.STARTING
                    
            
            else:
                pass # an event type we don't handle 
    def game_over(self):
        """Player is out of lives

        Play game over sound and wait for it to end before restarting.
        """
        self.state = MyGame.GAME_OVER
        self.screen.fill(0)
        game_over =  self.game_over_font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over.get_rect()
        game_over_rect.center = self.width//2, self.height//2
        
        img = self.gamefont.render("Final Score: %d"%self.score, True,\
                                  (255,255,255))
        rect2 = img.get_rect()
        rect2.center = self.width//2, self.height - rect2.height
        self.screen.blit(img, rect2)
        
        self.screen.blit(img, rect2)
        self.screen.blit(game_over, game_over_rect)
        
        
        self.gameover.play()
        delay = 2000
        self.bgm.stop()
        pygame.time.set_timer(MyGame.RESTART, delay+2000)
        
    
    def new_apple(self):
        direction = 0,0
        position = (random.randint(35, self.width - 35), -35)
        self.apples.add(Apple(position, direction, self.apple))
    
    def new_level(self):
        self.bg_color = ((random.randint(0,255)),(random.randint(0,255)),(random.randint(0,255)))
        self.levelup.play()
        self.x /= 2
        self.timeout += 30
        self.new_apple()
        self.quota += self.quota_inc
        self.quota_inc += 48
        self.level += 1
        
    def draw(self):
        """Update the display"""
        # everything we draw now is to a buffer that is not displayed
        self.screen.fill(self.bg_color)
        
        
        if self.state == MyGame.STARTING:
            
            self.title_rect.center = self.width//2, self.title_rect.height
            
            self.recttext.center = self.width//2, self.height//2 + self.recttext.height
            self.screen.blit(self.title, self.title_rect)
            if self.recttext.collidepoint(pygame.mouse.get_pos()):
                self.playgame_txt = self.gamefont.render('Click to Play', 
                    True, (255,0,0))
            else: 
                self.playgame_txt = self.gamefont.render('Click to Play', 
                    True, (255,255,255))
            self.screen.blit(self.playgame_txt, self.recttext)
            if self.hs.collidepoint(pygame.mouse.get_pos()):
                self.high_txt = self.gamefont.render('High Scores', 
                    True, (255,0,0))
            else: self.high_txt = self.gamefont.render('High Scores', 
                    True, (255,255,255))
            self.screen.blit(self.high_txt, self.hs)
        elif self.state == MyGame.HIGHSCORES:
            
            
            
            self.retrect.bottom = self.height
            self.myrect.center = (self.width//2,self.height//2)
            if self.retrect.collidepoint(pygame.mouse.get_pos()):
                self.sell = self.gamefont.render('Main Menu', 
                    True, (255,0,0))
            else: self.sell = self.gamefont.render('Main Menu', 
                    True, (255,255,255))
            self.screen.blit(self.sell, self.retrect)
            self.screen.blit(self.scores, self.myrect)
         
        else:
            rect = self.basket.get_rect()
            rect.center = (pygame.mouse.get_pos()[0], \
                           self.height - rect.height/2)
            self.screen.blit(self.basket, rect)

            for apple in list(self.apples):
                
                apple.draw(self.screen)
                apple.update()
                
                if apple.position[1] > rect.top and\
                apple.position[0] > rect.left and\
                apple.position[0] < rect.right and\
                apple.position[1] < rect.bottom:
                    self.apples.remove(apple)
                    self.basket_snd.play()
                    self.score += 1
                    self.new_apple()
                    
                if apple.position[1] > self.height:
                    self.apples.remove(apple)
                    
        if self.state == MyGame.PLAYING:
            img = self.gamefont.render("score: %d"%self.score, True, \
                                      (255,255,255))
            rect2 = img.get_rect()
            self.screen.blit(img, rect2)
            
            lev = self.gamefont.render("level: %d"%self.level, True, \
                                      (255,255,255))
            lev_rect = lev.get_rect()
            lev_rect.center = self.width//2, lev_rect.height//2
            self.screen.blit(lev, lev_rect)
            
            many_left = self.quota - self.score
            apples_left = self.gamefont.render("catch %d more apples" \
                                              %many_left, True, (255,0,0))
            if many_left == 1:
                apples_left = self.gamefont.render("catch %d more apple" \
                                                  %many_left, True, (255,0,0))
            apples_left_rect = apples_left.get_rect()
            apples_left_rect.center = (self.width//2, self.height//2)
            
            if many_left > 0:
                self.screen.blit(apples_left,apples_left_rect)
                    
            elapsed = (pygame.time.get_ticks() - self.start_time)/1000
            timeleft = max(0, self.timeout-elapsed)
            text = self.gamefont.render("time left: %.0f" % timeleft, True,\
                                       (255,255,255))
            rect_timeleft = text.get_rect()
            rect_timeleft = rect_timeleft.move\
                           (self.width - rect_timeleft.width, 0)
            self.screen.blit(text, rect_timeleft)
            
            if timeleft == 0:
                
                if self.score < self.quota:
                    self.game_over()
                else:
                    self.new_level()

        # flip buffers so that everything we have drawn gets displayed
        pygame.display.flip()
try:
    import android
except ImportError:
    android = None
if android:
    android.init()
    android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
try:
    import pygame.mixer as mixer
except ImportError:
    import android.mixer as mixer

MyGame().run()
pygame.quit()
sys.exit()
