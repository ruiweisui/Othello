from game_controller import GameController
from time import time

SIZE = 800
GRID_NUMBER = SIZE/100
COMPUTER_DELAY_TIME = 1.5
DISPLAY_WINDOW_SIZE = 400

gc = GameController(SIZE, SIZE, GRID_NUMBER)


def setup():
    size(SIZE + DISPLAY_WINDOW_SIZE, SIZE)
    gc.board.display_board()
    gc.high_score_info()
    gc.computer.first_two_tile()
    gc.player.first_two_tile()


def draw():
    gc.update()
    if time() > gc.last_turn_time + COMPUTER_DELAY_TIME:
        gc.computer_move()
    gc.display_message()


def mousePressed():
    if (825 <= mouseX <= 1175) and (685 <= mouseY <= 770):
        gc.player.give_hint()
    gc.player_move(mouseX, mouseY)
