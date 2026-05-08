# Python game
import pygame
from pygame.locals import *



class Player:
    #ddddd
    x = 10
    # x axis
    y = 10
    # y axis
    speed = 1
    def move_right(self):
        self.x = self.x + self.speed
    def move_left(self):
        self.x = self.x-self.speed
    def move_up(self):
        self.y = self.y-self.speed
    
    def move_down(self):
        self.y = self.y+self.speed
    

class App: 
    window_width = 800
    window_height= 600
    player=0

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self.player = Player()
    
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.window_width,self.window_height),pygame.HWSURFACE)
        pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        self._image_surf = pygame.Surface((50, 50))
        self._image_surf.fill((255, 0, 0))

    def on_event(self, event):
        if event.type == QUIT:
            self._running  = False
    
    def on_loop(self):
        pass

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
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()


            
        
        
