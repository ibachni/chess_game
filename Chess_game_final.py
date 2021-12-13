'''
Move log, valid moves and game state
'''
class Game_state:
    def __init__(self):
        self.location = [
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
        ]
        self.white_to_move = True
        self.checkmate = False
        self.stalemate = False


gamestate = Game_state()
current_location = gamestate.location

class moving:
    def __init__(self):
        self.general_validity = True
        self.piece_valid_moves = []

        self.starting_square = []
        self.ending_square = []

        self.starting_color = []
        self.ending_color = []

        self.selected_piece = []
        self.target_piece = []

    def determine_color(self):

        if current_location[self.starting_square[1]][self.starting_square[0]][0] == "w":
            self.starting_color = "w"
        elif current_location[self.starting_square[1]][self.starting_square[0]][0] == "b":
            self.starting_color = "b"
        if current_location[self.ending_square[1]][self.ending_square[0]][0] == "w":
            self.ending_color = "w"
        elif current_location[self.ending_square[1]][self.ending_square[0]][0] == "b":
            self.ending_color = "b"


    def determine_piece(self):
        self.target_piece = current_location[self.ending_square[1]][self.ending_square[0]]

    def gen_validity(self):
        '''
        Determines general validity (You cannot attack your own piece and you can only move if its your turn)
        Validity is also only possible, if end square is in valid moves
        :return: Bool for general_validity
        '''
        self.determine_color()
        self.determine_piece()

        #print(self.general_validity, "gen valid1")

        if self.starting_color == self.ending_color:
            self.general_validity = False

        if self.starting_color == "w" and gamestate.white_to_move == False:
            self.general_validity = False

        elif self.starting_color == "b" and gamestate.white_to_move == True:
            self.general_validity = False

    def pawn_moves(self):
        # clear cache after move
            #  Can move two squares, if starting position

        if self.selected_piece == "wp":
            if self.starting_square[1] == 6 and self.target_piece == "--":
                self.piece_valid_moves.append((self.starting_square[0], 4))
                self.piece_valid_moves.append((self.starting_square[0], 3))
                print(self.piece_valid_moves, "version 1")

                if current_location[self.starting_square[1]-1][self.starting_square[0]-1][0] == "b":
                    print("enemy_piece to the left")

                    self.piece_valid_moves.append((self.starting_square[1]-1, self.starting_square[0]-1))
                if current_location[self.starting_square[1]-1][self.starting_square[0]+1][0] == "b":
                    print("enemy_piece to the right")
                    self.piece_valid_moves.append((self.starting_square[1]-1, self.starting_square[0]+1))

            # can move only one afterwards
            if self.starting_square[1] != 6 and self.target_piece == "--":
                self.piece_valid_moves.append((self.starting_square[0], self.starting_square[1]-1))
                print(self.piece_valid_moves, "version 2")

                # if there is a black piece left or right forward of it
                if current_location[self.starting_square[1]-1][self.starting_square[0]-1][0] == "b":
                    print("enemy_piece to the left")
                    self.piece_valid_moves.append((self.starting_square[1]-1, self.starting_square[0]-1))
                if current_location[self.starting_square[1]-1][self.starting_square[0]+1][0] == "b":
                    print("enemy_piece to the right")
                    self.piece_valid_moves.append((self.starting_square[1]-1, self.starting_square[0]+1))

            # valid moves:
            # 2 nach vorne if ausgangsposition
            # 1 nach vorne
            # 1 nach vorne links und vorne rechts if enemy
        elif self.selected_piece == "bp":
            print("bp")

moves = moving()
