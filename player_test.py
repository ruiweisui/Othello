from player import Player
from board import Board

board = Board(800, 800, 8)
p = Player(0, board)


def test_first_two_tile():
    p.first_two_tile()
    assert p.grid[(4, 3)].color == 0
    assert p.grid[(3, 4)].color == 0
