import sys
from pgzhelper import *
import pygame

joystick = pygame.joystick.Joystick(1) #Joystick 1 is the left side of our arcade
joystick.init()

WIDTH=800
HEIGHT=600

runner = Actor('run__000')
run_images = ['run__000', 'run__001', 'run__002', 'run__003', 'run__004', 'run__005', 'run__006', 'run__007', 'run__008', 'run__009']
runner.images = run_images
runner.x = 100
runner.y = 400

velocity_y = 0
gravity = 1

obstacles = []
obstacles_timeout = 0

score = 0
game_over = False

def update():
  global velocity_y, obstacles_timeout, score, game_over
  runner.next_image()

  if not game_over:
    obstacles_timeout += 1
    if obstacles_timeout > 50:
        actor = Actor('cactus')
        actor.x = 850
        actor.y = 430
        obstacles.append(actor)
        obstacles_timeout = 0

    for actor in obstacles:
        actor.x -= 8
        if actor.x < -50:
            obstacles.remove(actor)
            score += 1
  else:
    if joystick.get_button(1)==1:
      game_over = False
      score = 0
  
  if runner.y == 400 and (keyboard.up or joystick.get_button(1)==1 or joystick.get_axis(1) < -0.1):
    velocity_y = -15
    sounds.jump_sound.play()
  if keyboard.escape or joystick.get_button(7)==1: #button 7 is the start button up top
        sys.exit()

  runner.y += velocity_y
  velocity_y += gravity
  if runner.y > 400:
    velocity_y = 0
    runner.y = 400

  if runner.collidelist(obstacles) != -1:
    game_over = True

def draw():
  screen.draw.filled_rect(Rect(0,0,800,400), (163, 232, 254))
  screen.draw.filled_rect(Rect(0,400,800,200), (88, 242, 152))
  if game_over:
    screen.draw.text('Game Over', centerx=400, centery=270, color=(255,255,255), fontsize=60)
    screen.draw.text('Score: ' + str(score), centerx=400, centery=330, color=(255,255,255), fontsize=60)
  else:
    runner.draw()
    for actor in obstacles:
      actor.draw()
    screen.draw.text('Score: ' + str(score), (15,10), color=(0,0,0), fontsize=30)