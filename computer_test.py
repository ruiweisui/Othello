from copy import deepcopy
from computer import Computer
from board import Board

board = Board(800, 800, 8)
c = Computer(225, board)


def test_first_two_tile():
    c.first_two_tile()
    assert c.grid[(3, 3)].color == 225
    assert c.grid[(4, 4)].color == 225


def test_greedy():
    board.reset_board()
    board.grid()[(1, 1)].color = 0
    board.grid()[(1, 2)].color = 0
    board.grid()[(1, 3)].color = 0
    board.grid()[(1, 4)].color = 225
    board.grid()[(0, 3)].color = 225
    assert c.greedy(board.grid()[(1, 0)]) == 3
    assert c.greedy(board.grid()[(2, 3)]) == 1
    assert c.greedy(board.grid()[(2, 1)]) == 1


def test_weight_greedy():
    board.reset_board()
    board.grid()[(1, 1)].color = 0
    board.grid()[(1, 2)].color = 0
    board.grid()[(1, 3)].color = 0
    board.grid()[(1, 4)].color = 225
    board.grid()[(0, 3)].color = 225
    assert c.weight_greedy(board.grid()[(1, 0)]) == -20-40-5-5
    assert c.weight_greedy(board.grid()[(2, 3)]) == -5+3
    assert c.weight_greedy(board.grid()[(2, 1)]) == -5-5


def test_minimax():
    board.reset_board()
    board.grid()[(3, 3)].color = 0
    board.grid()[(4, 4)].color = 225
    board.grid()[(3, 4)].color = 0
    board.grid()[(4, 3)].color = 0
    board.grid()[(2, 3)].color = 0
    temp_board = deepcopy(board)
    c.score_list = []
    assert c.minimax(board.grid()[(2, 2)], 3, temp_board, -1000) == 5
    temp_board = deepcopy(board)
    c.score_list = []
    assert c.minimax(board.grid()[(2, 4)], 3, temp_board, -1000) == 2
    temp_board = deepcopy(board)
    c.score_list = []
    assert c.minimax(board.grid()[(4, 2)], 3, temp_board, -1000) == 2


def test_minimax_score():
    board.reset_board()
    board.grid()[(1, 1)].color = 0
    board.grid()[(1, 2)].color = 0
    board.grid()[(1, 4)].color = 225
    assert c.minimax_score(board) == -1


def test_best_move():
    board.reset_board()
    board.grid()[(1, 1)].color = 0
    board.grid()[(1, 2)].color = 0
    board.grid()[(1, 3)].color = 0
    board.grid()[(1, 4)].color = 225
    board.grid()[(0, 3)].color = 225
    assert c.best_move("easy")[0].row == 1
    assert c.best_move("easy")[0].column == 0
    assert c.best_move("median")[0].row == 2
    assert c.best_move("median")[0].column == 3
    assert c.best_move("hard")[0].row == 2
    assert c.best_move("hard")[0].column == 3
