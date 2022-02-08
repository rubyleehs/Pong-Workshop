import random # For RNG
import sys

# Useful library for making games
# In our case, we be using it to draw stuff on screen, 
# handle events and dealing with time.
import pygame 


# Create Paddle Class that inherits from pygame.Rect
class Paddle(pygame.Rect):
  # Define __init__() that takes in a velocity, up/down keys and extras for pygame.Rect 
  def __init__(self, velocity, up_key, down_key,*args, **kwargs):
    # Assign velocity and keys variables in class INSTANCE
    self.velocity = velocity
    self.up_key = up_key
    self.down_key = down_key
    self.score = 0
 
    # Call superclass __init__()
    super().__init__(*args, **kwargs)


  # Declare move_paddle() that takes in the screen height
  def move_paddle(self, screen_height):
    # Get which keys are pressed
    keys_pressed = pygame.key.get_pressed()

    # Check if the up/down key is pressed and move the paddle position
    if(keys_pressed[self.up_key] and self.y - self.velocity > 0):
      self.y = self.y - self.velocity

    if(keys_pressed[self.down_key] and self.y + self.height + self.velocity < screen_height):
      self.y += self.velocity


# Create a Ball Class that inherits from pygame.Rect
class Ball(pygame.Rect):
  # Define __init__() that takes in a velocity and extras for pygame.Rect
  def __init__(self, x_velocity, y_velocity, *args, **kwargs):
    # Assign starting x and y velocity to class INSTANCE
    self.x_velocity = x_velocity
    self.y_velocity = y_velocity

    # Call superclass __init__()
    super().__init__(*args, **kwargs)

  # Define a function to move the ball
  def move_ball(self):
    # Add the velocity to the position of the ball
    self.x += self.x_velocity
    self.y += self.y_velocity
    

# Create a Pong Class.
class Pong:
  # Declare some constants.
  HEIGHT = 200
  WIDTH = 400

  PADDLE_WIDTH = 5
  PADDLE_HEIGHT = 80
  PADDLE_MOVE_SPEED = 4

  BALL_WIDTH = 8
  BALL_HEIGHT = 8
  BALL_X_VELOCITY = 3
  BALL_MAX_Y_SPEED = 4

  COLOUR = (255, 255, 255)

  # Define __init__()
  def __init__(self):
    # Start pygame instance with pygame.init()
    pygame.init()
    # Setup/Assign the screen and clock in Pong instance
    self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
    self.clock = pygame.time.Clock()

    # Assign an array of Paddle instances in Pong instance
    self.paddles = []

    self.paddles.append(Paddle( # Left Paddle
      self.PADDLE_MOVE_SPEED,                 # velocity
      pygame.K_w,                             # up_key
      pygame.K_s,                             # down_key
      0,                                      # x position of top left of rectangle
      (self.HEIGHT - self.PADDLE_HEIGHT)/2,   # y position of top left of rectangle
      self.PADDLE_WIDTH,                      # width of rectangle
      self.PADDLE_HEIGHT                      # height of rectangle
    ))

    self.paddles.append(Paddle( # Right Paddle
      self.PADDLE_MOVE_SPEED,
      pygame.K_UP,
      pygame.K_DOWN,
      self.WIDTH - self.PADDLE_WIDTH,
      (self.HEIGHT - self.PADDLE_HEIGHT)/2,
      self.PADDLE_WIDTH,
      self.PADDLE_HEIGHT
    ))

    # Assign an array of Ball instances in Pong instance
    self.balls = []

    self.balls.append(Ball(
      self.BALL_X_VELOCITY,                     # x velocity            
      self.BALL_MAX_Y_SPEED,                    # y velocity
      (self.WIDTH - self.BALL_WIDTH)/2,         # x position
      (self.HEIGHT - self.BALL_WIDTH)/2,        # y position
      self.BALL_WIDTH,                          # width of ball
      self.BALL_HEIGHT                          # height of ball
    ))

    # Assign a central line for decoration puposes
    self.central_line = pygame.Rect(self.WIDTH/2, 0, 1, self.HEIGHT)
    self.game_started = False
       
  # Define a function to check if the ball have hit a paddle
  def ball_hit_paddle(self):
    # Loop through all the balls
    for ball in self.balls:
      # Loop through all the paddles
      for paddle in self.paddles:
        # If the ball collided, flip the x velocity and randomize the y velocity
        if(ball.colliderect(paddle)):
          ball.x_velocity *= -1
          ball.y_velocity = random.randint(-self.BALL_MAX_Y_SPEED, self.BALL_MAX_Y_SPEED)
          break

  # Define a function to start the game loop
  def game_loop(self):
    # Add Loop till the game ends
    while(True):
      # Check if player want Force Quit Game?
      for event in pygame.event.get():
        if(event.type == pygame.KEYDOWN):
          self.game_started = True
          if(pygame.key == pygame.K_ESCAPE):
            # Quit the game normally sys.exit(1)
            sys.exit(0)
          
      # Call functions that checks ball collisions
      self.ball_hit_paddle()
      
      # Loop through all the balls
      for ball in self.balls:
        # Check if it has touched the left or right edges of the screen 
        if (ball.x > self.WIDTH):
          self.paddles[1].score += 1
          ball.x = (self.WIDTH - self.BALL_WIDTH)/2
          ball.y = (self.HEIGHT - self.BALL_WIDTH)/2
          self.game_started = False;
          
        if (ball.x < 0):
          ball.x = (self.WIDTH - self.BALL_WIDTH)/2
          ball.y = (self.HEIGHT - self.BALL_WIDTH)/2
          self.paddles[0].score += 1
          self.game_started = False;

        # Check if it has touched the top or bottom edges of the screen        
        if (ball.y < 0 or ball.y + ball.height > self.HEIGHT):
          # If so, bounce the ball
          ball.y_velocity *= -1

      # Redraw the screen.
      self.screen.fill((0,0,0))

      # Loop through all the paddles, move then draw them
      for paddle in self.paddles:
        paddle.move_paddle(self.HEIGHT)
        pygame.draw.rect(self.screen, self.COLOUR, paddle)
        # pygame.draw.blit(self.screen, textthing....)

      # Loop through all the balls, move then draw them      
      for ball in self.balls:
        if(self.game_started):
          ball.move_ball()
        pygame.draw.rect(self.screen, self.COLOUR, ball)

      # Draw decorational stuff
      pygame.draw.rect(self.screen, self.COLOUR, self.central_line)

      # Update the display with pygame.display.flip
      pygame.display.flip()

      # Limit FPS with self.clock.tick(value)
      self.clock.tick(60)


if __name__ == '__main__':
  # Create a Pong Instance
  pong = Pong()

  # Start the game loop
  pong.game_loop()
