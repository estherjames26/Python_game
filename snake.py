# Python game
import pygame
from pygame.locals import *
import pygame_menu
import random


# --------------------------------------------------------------Player
class Player:
    """Creates the player snake, and contains its controls
    Output:"""

    def __init__(self,length):

        self.length = length
        self.x = []
        # x axis
        self.y = []
        # y axis
        self.step = 27
        self.direction = 0
        self.update_count_max = 2
        self.update_count = 0
        self.start_x=300
        self.start_y=300
        for i in range(0,length):
            self.x.append(self.start_x)
            self.y.append(self.start_y-(i*self.step))

    def update(self):
        """The snake by default will move in a direction unless a key is pressed to change the direction"""
        self.update_count += 1
        # It will be checked every 2 moves if the direction has changed, 
        # so that the body of the snake will move according to the direction
        if self.update_count> self.update_count_max:

            for i in range(self.length-2,0,-1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]


            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step
        
            self.update_count = 0

    def move_right(self):
        """Sets direction to the right of the screen"""
        self.direction = 0
    def move_left(self):
        """Sets direction to the left of the screen"""
        self.direction = 1
    def move_up(self):
        """Sets direction to the up of the screen"""
        self.direction = 2
    def move_down(self):
        """Sets direction to the down of the screen"""
        self.direction = 3

    def draw(self,surface,image,image2):
        """Draws the head as orange and the rest of the body as red"""
        surface.blit(image,(self.x[0],self.y[0]))
        for i in range(1, self.length - 1):
            surface.blit(image2,(self.x[i],self.y[i]))

class Apple:
    """Creates the objective of the game: get as many apples as possible without any collision"""
    x = 0
    y = 0
    step = 27  

    def __init__(self, x, y):
        self.x = x * self.step 
        self.y = y * self.step

    def draw(self, surface, image):
        surface.blit(image,(self.x, self.y)) 

class Game:
    """Sets up the game's physics"""
    def is_collision(self, x1, x2, y1, y2, bsize):
            """Detects if the coordinates of x1 y1(player) 
            overlap with the coordinates of x2 y2(an apple/the player itself)
            Input:
                    x1=Integer
                    x2=Integer
                    y1=Integer
                    y2=Integer
                    bsize=Integer"""
            if x1 >= x2 and x1 <= x2 + bsize:
                if y1 >= y2 and y1 <= y2 + bsize:
                    return True
            return False

    def out_of_bounds_check(self, w_width, w_height, x, y):
        """Detects if the coordinates of the snake go past the dimensions of the game window
        """
        if x > w_width or x < 0:
            return True
        if y > w_height or y < 0:
            return True
        return False

class App: 

    def __init__(self):
        self.window_width = 800
        self.window_height= 600
        self.player=0
        self._running = True
        self._display_surf = None
        self._body_surf = None
        self._apple_surf = None
        self._head_surf = None
        self.score=0
        self.game = Game()
        self.player = Player(10)
        self.apple = Apple(5,5)
        self.clock = pygame.time.Clock()
    
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.window_width,self.window_height),pygame.HWSURFACE)
        pygame.display.set_caption('Snake Game')
        self._running = True
        self._head_surf = pygame.Surface((25, 25))
        self._head_surf.fill((255, 153, 28))
        self._body_surf = pygame.Surface((25, 25))
        self._body_surf.fill((255, 0, 0))
        self._apple_surf = pygame.Surface((25, 25))
        self._apple_surf.fill((0, 255, 0))

    def setup_menu(self):
        """Creates the menu for the game"""
        self.menu = pygame_menu.Menu('Snake', self.window_width, self.window_height,
                                    theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.label("How to play:\nW=Up, A=Left, S=Down, D=Right\n Aim for green squares (apples) for points\n" \
        "Avoid the edges of the screen and colliding with yourself")
        self.menu.add.button('Play', self.start_the_game)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
        

    def start_the_game(self):
        self.menu.disable()

    def reset(self):
        self.player = Player(10)
        self.apple = Apple(5,5)
        self._running = True


    def on_event(self, event):
        if event.type == QUIT:
            self._running  = False
    
    def on_loop(self):
        self.player.update()

        # Detects if the snake has reached an apple
        for i in range(0,self.player.length):
            if self.game.is_collision(self.player.x[i], self.apple.x, self.player.y[i], self.apple.y, 25):
                self.apple.x = random.randint(2,9) * 25
                self.apple.y = random.randint(2,9) * 25
                self.player.length = self.player.length + 1
                # Another block will be added to the snake
                self.player.x.append(self.player.x[self.player.length-2])
                self.player.y.append(self.player.y[self.player.length-2])
                self.score+=100
                
 
        # Detects is the snake has collided with itself (game ends)
        for i in range(4,self.player.length):
            if self.game.is_collision(self.player.x[0],self.player.x[i],self.player.y[0], self.player.y[i],25):
                print("You lose! Collision: ")
                print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
                print("x[" + str(i) + "] (" + str(self.player.x[i]) + "," + str(self.player.y[i]) + ")")
                self._running = False
                

        # Detects if the snake has touched the game window boarders (game ends)
        if self.game.out_of_bounds_check(self.window_width, self.window_height, self.player.x[0], self.player.y[0]):
            print("You have collided with the wall, game over")
            self._running = False
            
 




    def on_render(self):
        """Runs when the game opens"""
        self._display_surf.fill((0,0,0))
        self.player.draw(self._display_surf, self._head_surf,self._body_surf)
        self.apple.draw(self._display_surf,self._apple_surf)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        self._display_surf.blit(score_text, (10, 10))
        pygame.display.flip()

    """def on_cleanup(self):
        pygame.quit()"""
    
    def game_over_screen(self):
        font_big = pygame.font.Font(None,72)
        font_small = pygame.font.Font(None,36)
        self._display_surf.fill((0,0,0))
        game_over_text = font_big.render('GAME OVER',True, (255,0,0))
        score_text = font_small.render(f"Final Score: {self.score}",True,(255,255,255))
        self._display_surf.blit(game_over_text, (self.window_width//2 - game_over_text.get_width()//2, 200))
        self._display_surf.blit(score_text, (self.window_width//2 - score_text.get_width()//2, 300))
        pygame.display.flip()
        pygame.time.wait(2000)
        self.score=0
    
    def on_execute(self):

        if self.on_init() == False:
            self._running = False
            return
        self.setup_menu()

        while True:
            self.reset()
            self.menu.enable()
            self.menu.mainloop(self._display_surf)

            while(self._running):
                pygame.event.pump()
                keys = pygame.key.get_pressed()

                if (keys[K_d]):
                    self.player.move_right()

                if (keys[K_a]):
                    self.player.move_left()

                if (keys[K_w]):
                    self.player.move_up()

                if (keys[K_s]):
                    self.player.move_down()

                if (keys[K_ESCAPE]):
                    self._running =  False
                self.on_loop()
                self.on_render()
                self.clock.tick(30)
            self.game_over_screen()




if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()


            
        
        
