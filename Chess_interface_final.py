'''
Chess Game: Main file, controlling the interface
'''

import pygame
import sys
import Chess_game_final as cg



pygame.init()

# title and icon
pygame.display.set_caption("Chess Game")
icon = pygame.image.load("strategy.png")
pygame.display.set_icon(icon)

'''
Set major attributes of the board
'''

width = 800  # in px
dimensions = 8
square_size = width // dimensions  # calculate square size based on width and dimensions
max_fps = 15
white, black = (227, 227, 230), (140, 162, 173)  # color of "white" and "black" squares
focus_color = (155, 155 , 155)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((width, width))  # width, height
screen.fill(black)

# load images
pieces = ["bp", "br", "bn", "bb", "bq", "bk", "wp", "wr", "wn", "wb", "wq", "wk"]
image_dict = {}


def load_pieces():
    '''
    Load images of pieces into a image dictionary.
    Only done once before the game
    '''
    for piece in pieces:
        image_dict[piece] = pygame.transform.scale(pygame.image.load(piece + ".png"), (square_size, square_size))


load_pieces()


def draw_tiles():
    """
    Draw tiles. If number is even, then start with white tile, else: start with black.
    Only done once before the game
    """
    for x in range(0, 8, 2):
        for y in range(0, 8, 1):
            if (y % 2) == 0:  # even numbers
                pygame.draw.rect(screen, white, pygame.Rect(square_size * x, square_size * y, square_size, square_size))
            else:  # uneven numbers
                pygame.draw.rect(screen, white, pygame.Rect(square_size * (x + 1), square_size * y, square_size, square_size))
            pygame.display.update()


draw_tiles()

piece_object_dict = {}



nums = []
List = []

piece_information_dict = {}


'''
Creating instances of pieces
'''
rect_dict = {}
for y in range(len(cg.current_location)):  # rows
    for x in range(len(cg.current_location)):  # columns
        if cg.current_location[y][x] in pieces:
            if cg.current_location[y][x] not in rect_dict.keys():
                rect_dict[cg.current_location[y][x]] = screen.blit(image_dict[cg.current_location[y][x]],
                                                                   (x * square_size, y * square_size))
            else:
                rect_dict[cg.current_location[y][x] + str(x)] = screen.blit(image_dict[cg.current_location[y][x]],
                                                                            (x * square_size, y * square_size))
            pygame.display.update()


def starting_square_funct(beg_cursor_point):
    '''

    :param beg_cursor_point: location of the mouse click
    :return: starting_square of mouse click, starting_square_color of mouse click
    '''

    global starting_square
    global starting_square_color

    beg_clicked_row = beg_cursor_point[0] // square_size  # gives row
    beg_clicked_col = beg_cursor_point[1] // square_size  # gives column
    starting_square = [beg_clicked_row, beg_clicked_col]

    cg.moves.starting_square = starting_square

    #black_or_white_tile("start", starting_square, [0, 0])

    if (starting_square[0] + 1) % 2 == 0 and (starting_square[1]) % 2 == 0:
        starting_square_color = black
    elif (starting_square[0] + 1) % 2 == 1 and (starting_square[1]) % 2 == 1:
        starting_square_color = black
    else:
        starting_square_color = white



def ending_square_funct(end_cursor_point):
    '''
    :param end_cursor_point: location of the mouse click
    :return: ending_square of mouse click, ending_square_color of mouse click
    '''

    global ending_square
    global ending_square_color

    end_clicked_row = end_cursor_point[0] // square_size  # gives row
    end_clicked_col = end_cursor_point[1] // square_size  # gives column
    ending_square = [end_clicked_row, end_clicked_col]

# doesnt quite work
    cg.moves.ending_square = ending_square

    if (ending_square[0] + 1) % 2 == 0 and (ending_square[1]) % 2 == 0:
        ending_square_color = black
    elif (ending_square[0] + 1) % 2 == 1 and (ending_square[1]) % 2 == 1:
        ending_square_color = black
    else:
        ending_square_color = white


def remove_piece(x, y, color):
    '''

    :param x:
    :param y:
    :param color:
    :return:
    '''
    pygame.draw.rect(screen, color, pygame.Rect(square_size * x, square_size * y, square_size, square_size))
    pygame.display.update()

def implement_clicks():
    '''

    :return:
    '''
    cg.moves.gen_validity()

    if cg.moves.general_validity == True:

        remove_piece(ending_square[0], ending_square[1], ending_square_color)
        remove_piece(starting_square[0], starting_square[1], starting_square_color)
        screen.blit(image_dict[cg.current_location[starting_square[1]][starting_square[0]]], (ending_square[0] * square_size, ending_square[1] * square_size))
        cg.current_location[ending_square[1]][ending_square[0]] = cg.current_location[starting_square[1]][ starting_square[0]]


        if cg.current_location[starting_square[1]][starting_square[0]][0] == "w":
            cg.gamestate.white_to_move = False
        if cg.current_location[starting_square[1]][starting_square[0]][0] == "b":
            cg.gamestate.white_to_move = True

        cg.current_location[starting_square[1]][starting_square[0]] = "--"

    else:
        #highlight_click(focus_color, False)
        cg.moves.general_validity = True
        cg.moves.starting_color = ""
        cg.moves.ending_color = ""

def highlight_click(highlight_color, highlight):
    '''
    Currently not active, because results in a "lag"
    :param highlight_color:
    :param highlight:
    :return:
    '''

    if highlight == False:
        if (starting_square[0] + 1) % 2 == 0 and (starting_square[1]) % 2 == 0:
            highlight_color = black
        elif (starting_square[0] + 1) % 2 == 1 and (starting_square[1]) % 2 == 1:
            highlight_color = black
        else:
            highlight_color = white
    if cg.current_location[starting_square[1]][starting_square[0]] in pieces:
        remove_piece(starting_square[0], starting_square[1], highlight_color)
        screen.blit(image_dict[cg.current_location[starting_square[1]][starting_square[0]]],(starting_square[0] * square_size, starting_square[1] * square_size))


piece_picked_up = False
piece_selected = False
running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and piece_picked_up == False and piece_selected == False:
                starting_square_funct(pygame.mouse.get_pos()) # i know the starting square
                #highlight_click(focus_color, True)

                # noinspection PyUnboundLocalVariable
                if cg.current_location[starting_square[1]][starting_square[0]] in pieces:
                    piece_picked_up = True


        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and piece_picked_up == True and piece_selected == False:
                ending_square_funct(pygame.mouse.get_pos()) # Know the ending square

                # noinspection PyUnboundLocalVariable
                if starting_square != ending_square:

                    implement_clicks()
                    piece_picked_up = False


                elif starting_square == ending_square:

                    piece_selected = True
                    which_piece_selected = cg.current_location[starting_square[1]][starting_square[0]]
                    cg.moves.selected_piece = which_piece_selected


            elif event.button == 1 and piece_selected == True:
                ending_square_funct(pygame.mouse.get_pos())

                if starting_square != ending_square:

                    implement_clicks()
                    piece_selected = False
                    which_piece_selected = ""
                    cg.moves.selected_piece = ""
                    piece_picked_up = False

                elif starting_square == ending_square:

                    piece_selected = False
                    piece_picked_up = False
                    #highlight_click(focus_color, False)


    clock.tick(max_fps)
    pygame.display.update()