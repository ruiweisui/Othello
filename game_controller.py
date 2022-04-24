from board import Board
from player import Player
from computer import Computer
from time import time
import re

BLACK = 0
WHITE = 225
PROMPT_DELAY_TIME = 3
SPACE = 25
SCORE_BOARD_SIZE = (350, 200)
MESSAGE_BOARD_SIZE = (350, 410)
TEXT_SIZE = 42
SCORE_COORD = (850, 540)
HIGH_SCORE_COORD = (850, 95)
MESSAGE_COORD = (850, 270)


class GameController:
    """A game controller for Othello"""

    def __init__(self, WIDTH, HEIGHT, GRID_NUMBER):
        """GameController constructor"""
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.GRID_NUMBER = GRID_NUMBER
        self.SPACE = WIDTH/GRID_NUMBER
        self.board = Board(WIDTH, HEIGHT, GRID_NUMBER)
        self.grid = self.board.grid()
        self.player = Player(BLACK, self.board)
        self.computer = Computer(WHITE, self.board)
        self.player_number = 1
        self.COMPUTER_NUMBER = 2
        self.HUMAN_NUMBER = 1
        self.game_over = False
        self.end_everything = False
        self.finish_prompt = False
        self.last_turn_time = time()
        self.prompt_time = time()
        self.message = "Game start\nPlayer's turn"
        self.high_score_message = ""
        self.name = ""
        self.score_file = "scores.txt"

    def player_move(self, x, y):
        """Player move"""
        column = x//self.SPACE
        row = y//self.SPACE

        if row < self.GRID_NUMBER and column < self.GRID_NUMBER:
            tile = self.grid[(row, column)]
            # player only make move when it is player's turn, and there is a
            # valid move
            if self.player_number == self.HUMAN_NUMBER and\
               self.player.is_valid_move(tile):
                self.player.one_full_move(tile)
                # change player number to computer
                self.player_number = self.COMPUTER_NUMBER
                self.last_turn_time = time()
                self.message = "Compuater's\nturn"

    def computer_move(self):
        """Computer move"""
        # computer only make move when it is player's turn, and there is a
        # valid move
        if self.game_over is False and\
           self.player_number == self.COMPUTER_NUMBER:
            best_tile = self.computer.best_move()[0]
            self.computer.one_full_move(best_tile)
            # change player number to player
            self.player_number = self.HUMAN_NUMBER
            self.message = "Player's\nturn"

    def update(self):
        """Update that should happen every frame"""
        # display all the occupied tile
        for tile in self.board.tiles:
            if tile.color is not None:
                tile.display_tile()

        # once it is computer's turn, remove any hint
        if self.player_number == self.COMPUTER_NUMBER:
            self.player.remove_hint()

        # update the player number if one is out of move
        self.update_turn()
        # update the score
        self.show_score()

        # check if game is over and prompt player to enter name if so
        if self.game_over is True and self.end_everything is False:
            self.end_game_message()
            self.end_everything = True
            self.prompt_time = time() + PROMPT_DELAY_TIME

        # check if player has entered the name and record if so
        if self.end_everything is True and self.finish_prompt is False:
            if self.is_high_score():
                self.high_score_message = "You are the\nhighest score"
            if time() > self.prompt_time:
                self.name = self.enter_name()
                if self.name:
                    self.record(self.name)
                self.finish_prompt = True

    def update_turn(self):
        """Change turns and end the game if one is out of move"""
        if self.game_over is False:
            # if both are out of move
            if self.player.is_out_of_move() and self.computer.is_out_of_move():
                self.message = "Game over"
                self.game_over = True
            # if it is computer's turn and computer is out of move
            elif self.player_number == self.COMPUTER_NUMBER and\
                    self.computer.is_out_of_move() is True:
                self.message = "Computer is\nout of move\nplayer's turn"
                self.player_number = self.HUMAN_NUMBER
            # if it is player's turn and player is out of move
            elif self.player_number == self.HUMAN_NUMBER and\
                    self.player.is_out_of_move() is True:
                self.message = "Player is\nout of move\ncomputer's turn"
                self.player_number = self.COMPUTER_NUMBER
                self.last_turn_time = time()

    def count_score(self):
        """Count the score at the end of the game"""
        self.black_total = 0
        self.white_total = 0
        for tile in self.board.tiles:
            if tile.color == BLACK:
                self.black_total += 1
            elif tile.color == WHITE:
                self.white_total += 1
        return (self.black_total, self.white_total)

    def show_score(self):
        """Show real time score"""
        self.count_score()
        fill(50, 100, 100)
        rect(self.board.WIDTH + SPACE, MESSAGE_BOARD_SIZE[1] + SPACE + SPACE,
             SCORE_BOARD_SIZE[0], SCORE_BOARD_SIZE[1])
        score_message = "Player: %s\nComputer: %s"\
                        % (self.black_total, self.white_total)
        fill(BLACK)
        textSize(TEXT_SIZE)
        text(score_message, SCORE_COORD[0], SCORE_COORD[1])

    def end_game_message(self):
        """Update the end game message"""
        if self.white_total > self.black_total:
            result = "Computer win"
        elif self.black_total > self.white_total:
            result = "You win"
        else:
            result = "It is a tie"

        self.message = "%s" % (result)

    def display_message(self):
        """Display message with processing functionss"""
        stroke(BLACK)
        # this color is dark cyan
        fill(40, 150, 150)
        rect(self.WIDTH + SPACE, SPACE,
             MESSAGE_BOARD_SIZE[0], MESSAGE_BOARD_SIZE[1])
        fill(BLACK)
        textSize(TEXT_SIZE)
        # display game info
        text(self.message, MESSAGE_COORD[0], MESSAGE_COORD[1])
        # display high score info
        text(self.high_score_message, HIGH_SCORE_COORD[0], HIGH_SCORE_COORD[1])

    def high_score_info(self):
        """Show the current high score info"""
        with open(self.score_file, "r") as f:
            top_player = f.readline()
            current_best = re.findall(r'(\d+$)', top_player)
            if not current_best:
                current_best = [0]
            self.high_score_message = "Current high\nscore is %s" \
                                      % (current_best[0])

    def enter_name(self):
        """Prompt the user to enter the name"""
        player_name = self.input("Enter your name")
        return player_name

    def record(self, name):
        """Record high score after the game"""
        new_score = name + " " + str(self.black_total)
        with open(self.score_file, "r") as f:
            current_scores = f.read()

        # if the score is the new highest score, write new score first,
        # then previous score
        if self.is_high_score():
            with open(self.score_file, "w") as f:
                f.write(new_score + "\n")
                f.write(current_scores)
        # if the score is not the new highest score, write previous score
        # first, then new score
        else:
            with open(self.score_file, "w") as f:
                f.write(current_scores)
                f.write(new_score + "\n")

    def is_high_score(self):
        """Check if this score is the highest score"""
        with open(self.score_file, "r") as f:
            top_player = f.readline()
            current_best = re.findall(r'(\d+$)', top_player)

            if current_best == []:
                current_best = "0"
            else:
                current_best = current_best[-1]

            if self.black_total <= int(current_best):
                return False
        return True

    def input(self, message=''):
        from javax.swing import JOptionPane
        return JOptionPane.showInputDialog(frame, message)
