from game_controller import GameController

gc = GameController(800, 800, 8)
gc.score_file = "scores_test.txt"
BLACK = 0
WHITE = 225
PROMPT_DELAY_TIME = 3


def test_constructor():
    assert gc.WIDTH == 800
    assert gc.HEIGHT == 800
    assert gc.GRID_NUMBER == 8
    assert gc.SPACE == 100
    assert gc.player_number == 1
    assert gc.game_over is False
    assert gc.end_everything is False
    assert gc.finish_prompt is False
    assert gc.score_file == "scores_test.txt"


def test_player_move():
    gc.player.add_disk(3, 4)
    gc.computer.add_disk(4, 4)
    # test occupied tile
    gc.player_move(401, 401)
    assert gc.player_number == 1
    assert gc.grid[(4, 4)].color == 225
    # test invalid move
    gc.player_move(701, 701)
    assert gc.player_number == 1
    # test out of bound
    gc.player_move(901, 901)
    assert gc.player_number == 1
    # test valid move
    gc.player_move(401, 501)
    assert gc.player_number == 2


def test_computer_move():
    gc.player.add_disk(3, 4)
    gc.computer.add_disk(4, 4)
    gc.player_number = 2
    gc.computer_move()
    assert gc.grid[(2, 4)].color == 225
    for r in range(8):
        for c in range(8):
            if not(r == 2 or c == 4) and\
               not(r == 3 or c == 4) and\
               not(r == 4 or c == 4):
                assert gc.grid[(r, c)].color is None
    assert gc.player_number == 1


# update has processing functions


def test_update_turn():
    # test player out of move
    gc.board.reset_board()
    gc.grid[(0, 0)].color = 225
    gc.grid[(0, 1)].color = 0
    assert gc.player_number == 1
    gc.update_turn()
    assert gc.player_number == 2
    # test computer out of move
    gc.grid[(0, 0)].color = 0
    gc.grid[(0, 1)].color = 225
    assert gc.player_number == 2
    gc.update_turn()
    assert gc.player_number == 1
    # test game over
    gc.board.reset_board()
    assert gc.game_over is False
    gc.update_turn()
    assert gc.game_over is True


def test_count_score():
    gc.board.reset_board()
    gc.player.add_disk(3, 4)
    gc.computer.add_disk(4, 4)
    gc.player.add_disk(1, 4)
    assert gc.count_score()[0] == 2
    assert gc.count_score()[1] == 1


# show score has processing function in


def test_end_game_message():
    gc.white_total = 1
    gc.black_total = 2
    gc.end_game_message()
    assert gc.message == "You win"
    gc.white_total = 2
    gc.black_total = 1
    gc.end_game_message()
    assert gc.message == "Computer win"
    gc.white_total = 1
    gc.black_total = 1
    gc.end_game_message()
    assert gc.message == "It is a tie"


def test_is_high_score():
    with open(gc.score_file, "w") as f:
        f.write("R R 10\n")

    gc.black_total = 63
    assert gc.is_high_score() is True
    gc.black_total = 9
    assert gc.is_high_score() is False


def test_high_score_info():
    gc.high_score_info()
    assert gc.high_score_message == "Current high\nscore is 10"


def test_record():
    with open(gc.score_file, "w") as f:
        f.write("")

    gc.black_total = 10
    gc.record("R R")
    with open(gc.score_file, "r") as f:
        assert f.read() == "R R 10\n"
    gc.black_total = 15
    gc.record("Ruiwei!!!")
    with open(gc.score_file, "r") as f:
        assert f.read() == "Ruiwei!!! 15\nR R 10\n"
    gc.black_total = 7
    gc.record("RS")
    with open(gc.score_file, "r") as f:
        assert f.read() == "Ruiwei!!! 15\nR R 10\nRS 7\n"
    gc.black_total = 50
    gc.record("Rbest")
    with open(gc.score_file, "r") as f:
        assert f.read() == "Rbest 50\nRuiwei!!! 15\nR R 10\nRS 7\n"
    gc.black_total = 49
    gc.record("Rnotbest")
    with open(gc.score_file, "r") as f:
        a = "Rbest 50\nRuiwei!!! 15\nR R 10\nRS 7\nRnotbest 49\n"
        assert f.read() == a
