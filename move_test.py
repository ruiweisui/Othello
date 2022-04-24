from move import Move
from board import Board

board = Board(800, 800, 8)
move = Move(0, board)


def test_constructor():
    assert move.board == board
    assert move.color == 0
    assert move.grid == move.board.grid()


def test_add_disk():
    move.add_disk(0, 0)
    assert move.board.tiles[0].color == 0
    move.add_disk(0, 1)
    assert move.board.tiles[1].color == 0
    for i in range(64):
        if i != 0 and i != 1:
            assert move.board.tiles[i].color is None


def test_swap_color():
    for r in range(5):
        move.grid[(r, 0)].color = 0
    move.swap_color([move.grid[(0, 0)], move.grid[(1, 0)], move.grid[(2, 0)],
                     move.grid[(3, 0)], move.grid[(4, 0)]])
    for r in range(5):
        assert move.grid[(r, 0)].color == 225


def test_one_full_move():
    move.board.reset_board()
    move.grid[(0, 0)].color = 0
    move.grid[(0, 1)].color = 225
    move.grid[(0, 2)].color = 225
    move.grid[(0, 3)].color = 225
    move.one_full_move(move.grid[(0, 4)])
    for i in range(5):
        assert move.grid[(0, i)].color == 0


def test_is_inside_board():
    assert move.is_inside_board(0, 0) is True
    assert move.is_inside_board(7, 7) is True
    assert move.is_inside_board(5, 3) is True
    assert move.is_inside_board(0, -1) is False
    assert move.is_inside_board(-1, 0) is False
    assert move.is_inside_board(8, 7) is False


def test_tiles_to_swap():
    move.board.reset_board()
    move.grid[(0, 0)].color = 0
    move.grid[(0, 1)].color = 225
    move.grid[(0, 2)].color = 225
    move.grid[(0, 3)].color = 225
    assert move.tiles_to_swap(move.grid[(0, 4)]) == [
        move.grid[(0, 3)], move.grid[(0, 2)], move.grid[(0, 1)]
        ]


def test_is_valid_move():
    move.board.reset_board()
    move.grid[(0, 0)].color = 0
    move.grid[(0, 1)].color = 225
    move.grid[(0, 2)].color = 225
    move.grid[(0, 3)].color = 225
    assert move.is_valid_move(move.grid[(0, 4)]) is True
    for r in range(8):
        for c in range(8):
            if not (c == 4 and r == 0):
                assert move.is_valid_move(move.grid[(r, c)]) is False


def test_is_out_of_move():
    move.board.reset_board()
    move.grid[(0, 0)].color = 225
    move.grid[(0, 1)].color = 0
    assert move.is_out_of_move() is True
    move.grid[(0, 0)].color = 0
    move.grid[(0, 1)].color = 225
    assert move.is_out_of_move() is False
    move.board.reset_board()
    assert move.is_out_of_move() is True
