import pygame
import time
from random import randint 

screen_size_x = 720 ### Can be changed but value must be an multiples of 40
screen_size_y = 600 ### Can be changed but value must be an multiples of 40

SIZE_OF_BLOCK = 40
origin = SIZE_OF_BLOCK * 1

workable_screen_x = screen_size_x - SIZE_OF_BLOCK
workable_screen_y = screen_size_y - SIZE_OF_BLOCK

class Apple:
    def __init__(self,surface):
        self.surface = surface
        self.img = pygame.image.load("resources/apple.png").convert()

        self.lim_x = workable_screen_x / SIZE_OF_BLOCK
        self.lim_y = workable_screen_y / SIZE_OF_BLOCK

        self.x = randint(0,self.lim_x) * SIZE_OF_BLOCK # makes sure the snake and the apple align
        self.y = randint (0 ,self.lim_y) * SIZE_OF_BLOCK
        self.surface.blit(self.img,(self.x,self.y))
        pygame.display.update()
    
    def draw_a(self):
        self.surface.blit(self.img,(self.x,self.y))
        pygame.display.update()
    
    def change(self):
        self.x = randint(0,self.lim_x) * SIZE_OF_BLOCK # This makes sure apple and snake can align
        self.y = randint (0 ,self.lim_y) * SIZE_OF_BLOCK

class Snake:
    def __init__(self, surface,length):
        self.surface = surface
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [origin] * length
        self.y = [origin] * length
        self.direction = 'down'
        self.length = length

    def draw(self):
        for i in range(self.length):
            self.surface.blit(self.block,(self.x[i], self.y[i]))
            pygame.display.update(self.x[i], self.y[i], 40, 40)

    def up(self):
        if self.direction == 'down': # prevents mistake collisions
            pass
        else:
            self.direction = 'up'
        
    def down(self):
        if self.direction == 'up':
            pass
        else:
            self.direction ='down'
        
    def left(self):
        if self.direction == 'right':
            pass
        else:
            self.direction ='left'
        
    def right(self):
        if self.direction == 'left':
            pass
        else:
            self.direction ='right'

    def move(self):
        for i in range(self.length - 1, 0 , -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        
        if self.direction == 'up':
            self.y[0] -= SIZE_OF_BLOCK 
            self.draw()

        elif self.direction == 'down':
            self.y[0] += SIZE_OF_BLOCK 
            self.draw()

        elif self.direction == 'left':
            self.x[0] -= SIZE_OF_BLOCK 
            self.draw()

        elif self.direction == 'right':
            self.x[0] += SIZE_OF_BLOCK 
            self.draw()
        
        
class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((screen_size_x, screen_size_y))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw_a()

    def ate(self, x1, y1, x2, y2):
        if x1 == x2 :
            if y1 == y2 :
                return True
        return False
    
    def collision(self, x, y):
        for i in range(1, self.snake.length):
            if (x[0] == x[i]) and (y[0] == y[i]):
                return True
        return False
    
    def score(self):
        font = pygame.font.SysFont('arial', 20)
        score = font.render(f"Score: {self.snake.length}", True, (235,255,255))
        self.surface.blit(score, (workable_screen_x - 60, 0))
        pygame.display.update(workable_screen_x - 60,0, 50, 40)

    def restart(self):
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw_a()
        self.surface.fill((58, 153, 72))
        pygame.display.flip()

    def in_bounds(self, x, y, direction):
        if (x[0] < 0) or (y[0] < 0) or (x[0] > workable_screen_x) or (y[0] > workable_screen_y):
            if (x[0] < 0):
                x[0] += screen_size_x
                return 'left'
            elif (x[0] > workable_screen_x):
                x[0] -= screen_size_x
                return 'right'
            elif (y[0] < 0):
                y[0] += screen_size_y
                return 'up'
            elif (y[0] > workable_screen_y):
                y[0] -= screen_size_y
                return 'down'
        else:
            return direction


    def collision_protocol(self):
        self.surface.fill((0, 0, 0))
        font = pygame.font.SysFont('arial', 50)
        font2 = pygame.font.SysFont('arial', 30)
        display = font.render("Game Over!", True, (235,255,255))
        self.surface.blit(display, (10, 10))
        display2 = font2.render("Press ESC to exit", True, (255,255,255))
        self.surface.blit(display2, (10, 80))
        display3 = font2.render("Press RETURN to try again!", True, (255,255,255))
        self.surface.blit(display3, (10, 160))
        pygame.display.flip()
        return True
        

    def run(self):
        running = True
        over = False

        while running:
            if not over:
                over = self.more()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif over:
                        if event.key == pygame.K_RETURN:
                            over = False
                            self.restart()
                        pass
                    else:        
                        if event.key == pygame.K_UP:
                            self.snake.up()
                        elif event.key == pygame.K_DOWN:
                            self.snake.down()
                        elif event.key == pygame.K_LEFT:
                            self.snake.left()
                        elif event.key == pygame.K_RIGHT:
                            self.snake.right()
                elif event.type == pygame.QUIT:
                    running = False



    
    def more(self):
        self.surface.fill((58, 153, 72))

        self.snake.direction  = self.in_bounds(self.snake.x, self.snake.y, self.snake.direction)
        
        if self.ate(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.apple.change()
            for i in range(0, self.snake.length):
                while (self.apple.x == self.snake.x[i]) and (self.apple.y == self.snake.y[i]):
                    self.apple.change()
            self.apple.draw_a()
            self.snake.x.append(self.snake.x[self.snake.length  - 1])
            self.snake.y.append(self.snake.y[self.snake.length  - 1])
            self.snake.length += 1

        self.snake.move()
        self.apple.draw_a()
        self.score()
        if self.collision(self.snake.x, self.snake.y):
            return(self.collision_protocol())
        time.sleep(.3)
        return False



if __name__ == "__main__":
    game = Game()
    game.run()

