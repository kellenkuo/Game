#!/home/kevin/Desktop/SelfDrivingCar/keras/bin/python
import pygame
import numpy as np
from scipy import signal
from skimage.transform import resize
from skimage.io import imread
import os

Display_Size = np.array([ 500, 500 ], dtype = 'int' )
Piece_Size = np.array([ 30, 30 ], dtype = 'int' )

## filter ( for checking winner )
Filter = []
Filter.append( np.array([[1,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]]) )
Filter.append( np.array([[0,0,0,0,1],[0,0,0,1,0],[0,0,1,0,0],[0,1,0,0,0],[1,0,0,0,0]]) )
Filter.append( np.array([[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0]]) )
Filter.append( np.array([[0,0,0,0,0],[0,0,0,0,0],[1,1,1,1,1],[0,0,0,0,0],[0,0,0,0,0]]) )

## COLOR
black = (0,0,0)
white = (255,255,255)

class GoBang( object ):

    def __init__( self, Hold ):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode( Display_Size )
        pygame.display.set_caption('GoBang')
        self.clock = pygame.time.Clock()

        if Hold == 'white':
            self.hold = 1
        elif Hold == 'black':
            self.hold = -1

        ## statement
        self.board_status = np.zeros( ( 15, 15 ), dtype = 'int' )
        self.winner = 0
        self.turn = self.hold

        ## board
        self.board = pygame.image.load( os.path.join('board.jpg') )
        self.board = pygame.transform.scale( self.board, Display_Size )
        ## piece white
        self.piece_white = pygame.image.load( os.path.join('white.png') )
        self.piece_white = pygame.transform.scale( self.piece_white, Piece_Size )
        ## piece black
        self.piece_black = pygame.image.load( os.path.join('black.png') )
        self.piece_black = pygame.transform.scale( self.piece_black, Piece_Size )

    def QuitGame( self ):
        pygame.display.quit()
        pygame.quit()
        exit()
    def RestartGame( self ):
        self.board_status.fill(0)
        self.winner = 0
        self.turn = self.hold

    def Rules( self ):
        for i in range(4):
            result = signal.convolve2d( self.board_status, Filter[i], boundary='fill', mode='same' )
            if 5 in result:
                self.winner = 1
            if -5 in result:
                self.winner = -1

    def PRINT_SURFACE( self ):
        self.gameDisplay.blit( self.board, ( 0, 0 ) )
        ## x
        for i in range(15):
            x = np.round( i * 32.875 ) + 20 - ( Piece_Size[0] / 2 )
            ## y
            for k in range(15):
                y = np.round( k * 32.875 ) + 20 - ( Piece_Size[0] / 2 )
                if self.board_status[i][k] == 1:
                    self.gameDisplay.blit( self.piece_white, ( x, y ) )
                if self.board_status[i][k] == -1:
                    self.gameDisplay.blit( self.piece_black, ( x, y ) )

    def mouse_to_board( self, click_position ):
        x = np.round( click_position[0] - 20 + 25 ) / 32.875
        y = np.round( click_position[1] - 20 + 25 ) / 32.875
        self.board_status[ int( x ) ][ int( y ) ] = self.turn
        self.turn = -self.turn

    def Play( self ):
        try:
            while True:
                if self.winner != 0:
                    if self.winner == 1:
                        print('White is WINNER')
                    elif self.winner == -1:
                        print('Black is WINNER')
                    self.RestartGame()

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        mouse_position = pygame.mouse.get_pos()
                        self.mouse_to_board( mouse_position )
                        print('Mouse Click on ', mouse_position )
                if pygame.key.get_pressed()[113] == 1:
                    self.QuitGame()

                ## rule -> check if is five
                self.Rules()

                self.PRINT_SURFACE()
                ## change player

                pygame.display.update()
                self.clock.tick(10)

        except KeyboardInterrupt:
            self.QuitGame()




if __name__ == '__main__':
    google = GoBang('black')
    google.Play()




