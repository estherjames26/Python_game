# Python game
import pygame
from pygame.locals import *



class Player:
    #ddddd
    x = 10
    # x axis
    y = 10
    # y axis
    speed = 0.3
    direction = 0
    def update(self):
        if self.direction == 0:
            self.x = self.x + self.speed
        if self.direction == 1:
            self.x = self.x - self.speed
        if self.direction == 2:
            self.y = self.y - self.speed
        if self.direction == 3:
            self.y = self.y + self.speed
        

    def move_right(self):
        self.direction = 0
    def move_left(self):
        self.direction = 1
    def move_up(self):
        self.direction = 2
    def move_down(self):
        self.direction = 3
    

class App: 
    window_width = 800
    window_height= 600
    player=0

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self.player = Player()
        self.clock = pygame.time.Clock()
    
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.window_width,self.window_height),pygame.HWSURFACE)
        pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        self._image_surf = pygame.Surface((25, 25))
        self._image_surf.fill((255, 0, 0))

    def on_event(self, event):
        if event.type == QUIT:
            self._running  = False
    
    def on_loop(self):
        self.player.update()

    def on_render(self):
        self._display_surf.fill((0,0,0))
        self._display_surf.blit(self._image_surf,(self.player.x,self.player.y))
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
    
    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while(self._running):
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if (keys[K_RIGHT]):
                self.player.move_right()

            if (keys[K_LEFT]):
                self.player.move_left()

            if (keys[K_UP]):
                self.player.move_up()

            if (keys[K_DOWN]):
                self.player.move_down()

            if (keys[K_ESCAPE]):
                self._running =  False
            self.on_loop()
            self.on_render()

        self.clock.tick(60)
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()


            
        
        
