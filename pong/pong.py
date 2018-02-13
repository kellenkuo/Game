#!/home/kevin/Desktop/SelfDrivingCar/keras/bin/python
import pygame
import numpy as np
from skimage.transform import resize
from skimage.io import imread
import os

# statment
Display_width = 800
Display_height = 600
restart = False
running = True
# color
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
# object - ball
ball_size = np.array([ 50, 50 ], dtype = 'int' )
google_position = np.array([ 400, 300 ], dtype = 'int' )
move_direction = np.array([ 5, 5 ], dtype = 'int' )
# object - paddle
PADDLE_SIZE = np.array([ 20, 100 ], dtype = 'int' )
PADDLE_X = 100
PADDLE_position = np.array([ PADDLE_X, 100 ], dtype = 'int' )
# other score
Score = 0

pygame.init()
gameDisplay = pygame.display.set_mode(( Display_width, Display_height ))
## title
pygame.display.set_caption('Tic Tac Toe')
## game clock
clock = pygame.time.Clock()
## font type
myfont = pygame.font.SysFont( "monospace", 35 )
## ball image
google = pygame.image.load( os.path.join('google.png') )
google = pygame.transform.scale( google, ball_size )

def QuitGame():
    pygame.display.quit()
    pygame.quit()
    exit()

def google_icon( position ):
    position = ( position[0] - 20, position[1] - 20 )
    gameDisplay.blit( google, position )

def Paddle( Y ):
    global PADDLE_position
    gameDisplay.fill( black )
    PADDLE_position[1] = Y
    paddle = pygame.Rect( PADDLE_X, Y, PADDLE_SIZE[0], PADDLE_SIZE[1] )
    pygame.draw.rect( gameDisplay, white, paddle )

def print_text( text ):
    label = myfont.render( text, 1, white )
    gameDisplay.blit( label, ( 400, 10 ) )

def init():
    global google_position, move_direction, restart, Score
    google_position[0] = 300
    google_position[1] = 400
    move_direction[0] = 5
    move_direction[1] = 5
    Score = 0
    restart = False

def sweet( action ):
    global restart, google_position, move_direction, Score
    if restart:
        init()
        sweet( action )
    else:
        Paddle( action )
        # Rules
        if google_position[0] - PADDLE_position[0] < 20 and google_position[0] - PADDLE_position[0] > 0 and google_position[1] - PADDLE_position[1] < 100 and google_position[1] - PADDLE_position[1] > 0:
            move_direction[0] = -move_direction[0]
            Score += 1


        if google_position[0] + move_direction[0] <= 20:
            restart = True
        if google_position[0] + move_direction[0] >= 780:
            move_direction[0] = -move_direction[0]
        if google_position[1] + move_direction[1] <= 20:
            move_direction[1] = -move_direction[1]
        if google_position[1] + move_direction[1] >= 580:
            move_direction[1] = -move_direction[1]

        google_position[0] += move_direction[0]
        google_position[1] += move_direction[1]

        google_icon( google_position )

        pygame.display.update()
        # get games image
        image_data = pygame.surfarray.array3d( pygame.display.get_surface() )
        return Score, np.asarray( image_data ), restart



def Main():
    global running, restart, google_position, move_direction, Score
    try:
        while True:
            init()
            while not restart:
                # backend setting for game
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                if pygame.key.get_pressed()[113] == 1:
                    QuitGame()

                mouse_position = pygame.mouse.get_pos()
                Paddle( mouse_position[1] )

                # Rules
                if google_position[0] - PADDLE_position[0] < 20 and google_position[0] - PADDLE_position[0] > 0 and google_position[1] - PADDLE_position[1] < 100 and google_position[1] - PADDLE_position[1] > 0:
                    move_direction[0] = -move_direction[0]
                    Score += 1


                if google_position[0] + move_direction[0] <= 20:
                    restart = True
                if google_position[0] + move_direction[0] >= 780:
                    move_direction[0] = -move_direction[0]
                if google_position[1] + move_direction[1] <= 20:
                    move_direction[1] = -move_direction[1]
                if google_position[1] + move_direction[1] >= 580:
                    move_direction[1] = -move_direction[1]

                google_position[0] += move_direction[0]
                google_position[1] += move_direction[1]

                google_icon( google_position )
                print_text( str( Score ) )

                pygame.display.update()
                # get games image
                image_data = pygame.surfarray.array3d( pygame.display.get_surface() )
                # FPS
                clock.tick(10)

    except KeyboardInterrupt:
        QuitGame()

if __name__ == '__main__':
    Main()
