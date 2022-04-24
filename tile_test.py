from tile import Tile

tile = Tile(3, 3)


def test_constructor():
    assert tile.row == 3
    assert tile.column == 3
    assert tile.WHITE == 225
    assert tile.BLACK == 0
    assert tile.DIAMETER == 85
    assert tile.color is None


def test_change_color():
    tile.color = 0
    tile.change_color()
    assert tile.color == 225

# display_tile is processing function so it won't be tested
