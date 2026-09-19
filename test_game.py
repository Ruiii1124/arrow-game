from game import Game


def make_empty():
    return [
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
    ]


def test_can_fly_no_block():
    g = Game(make_empty())
    g.grid[1][1] = 1
    assert g.can_fly(1, 1) is True


def test_can_fly_block():
    g = Game(make_empty())
    g.grid[1][1] = 1
    g.grid[1][3] = 0
    assert g.can_fly(1, 1) is False


def test_click_fly_and_remaining():
    g = Game(make_empty())
    g.grid[0][0] = 1
    g.remaining = 1
    assert g.click(0, 0) == "fly"
    assert g.remaining == 0
    assert g.is_win()


def test_click_block_adds_mistake():
    g = Game(make_empty(), max_mistakes=3)
    g.grid[0][0] = 1
    g.grid[0][3] = 0
    g.remaining = 2
    assert g.click(0, 0) == "block"
    assert g.mistakes == 1


def test_lose():
    g = Game(make_empty(), max_mistakes=1)
    g.grid[0][0] = 1
    g.grid[0][3] = 0
    g.remaining = 2
    g.click(0, 0)
    assert g.is_lose()