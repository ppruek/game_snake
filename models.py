import arcade.key
from random import randint
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4
DIR_OFFSET = { DIR_UP: (0,1),
               DIR_RIGHT: (1,0),
               DIR_DOWN: (0,-1),
               DIR_LEFT: (-1,0) }

class Snake:
    MOVE_WAIT = 0.2
    BLOCK_SIZE = 16
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.wait_time = 0
        self.direction = DIR_RIGHT
        self.body = [(x,y),
                     (x-Snake.BLOCK_SIZE, y),
                     (x-2*Snake.BLOCK_SIZE, y)]
        self.length = 3
        self.has_eaten = False

    def update(self, delta):
        self.wait_time += delta
        if self.wait_time < Snake.MOVE_WAIT:
            return
        if self.x > self.world.width:
            self.x = 0
        if self.x < 0:
            self.x = self.world.width
        if self.y > self.world.height:
            self.y = 0
        if self.y < 0:
            self.y = self.world.height

        self.x += DIR_OFFSET[self.direction][0]*Snake.BLOCK_SIZE
        self.y += DIR_OFFSET[self.direction][1]*Snake.BLOCK_SIZE
        
        if self.has_eaten:
            self.body.insert(0,(self.x,self.y))
            self.has_eaten = False

        self.wait_time = 0
        self.body = [(self.x,self.y)] + self.body
        self.body.pop()

    def can_eat(self,heart):
        if(self.x == heart.x and self.y == heart.y):
            return True

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.snake = Snake(self, width // 2, height // 2)
        self.heart = Heart(self)
        self.heart.random_position()

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.UP:
            self.snake.direction = DIR_UP
        if key == arcade.key.DOWN:
            self.snake.direction = DIR_DOWN
        if key == arcade.key.LEFT:
            self.snake.direction = DIR_LEFT 
        if key == arcade.key.RIGHT:
            self.snake.direction = DIR_RIGHT

    def update(self, delta):
        self.snake.update(delta)
        if self.snake.can_eat(self.heart):
            self.heart.random_position()
            self.snake.has_eaten = True

class Heart:
    def __init__(self, world):
        self.world = world
        self.x = 0
        self.y = 0
 
    def random_position(self):
        centerx = self.world.width // 2
        centery = self.world.height // 2
 
        self.x = centerx + randint(-15,15) * Snake.BLOCK_SIZE
        self.y = centerx + randint(-15,15) * Snake.BLOCK_SIZE