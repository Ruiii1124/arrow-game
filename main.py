# main.py - 一箭又一箭主程序
import sys
import math
import pygame
from game import Game
from levels import LEVELS

pygame.init()
WIDTH, HEIGHT = 640, 760
CELL = 80
BOARD_X, BOARD_Y = 120, 180

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("一箭又一箭")
clock = pygame.time.Clock()

def get_font(size):
    for name in ("simhei", "microsoftyahei", "pingfang", "notosanscjk", None):
        try:
            return pygame.font.SysFont(name, size)
        except Exception:
            continue
    return pygame.font.Font(None, size)

font = get_font(26)
big_font = get_font(52)
small_font = get_font(20)

BG = (250, 250, 250)
CELL_BG = (240, 240, 240)
ARROW_COLOR = (50, 120, 220)
TEXT = (40, 40, 40)
BTN = (80, 160, 240)
BTN_HOVER = (60, 130, 210)

STATE_START = "start"
STATE_PLAY = "play"
STATE_RESULT = "result"

state = STATE_START
level_index = 0
game = None
result_text = ""

fly_anims = []
shake_anims = []
restart_rect = pygame.Rect(20, 20, 120, 44)


def draw_arrow_shape(surface, cx, cy, d, color=ARROW_COLOR, size=22):
    points = {
        0: [(cx, cy - size), (cx - size, cy + size // 2), (cx + size, cy + size // 2)],
        1: [(cx + size, cy), (cx - size // 2, cy - size), (cx - size // 2, cy + size)],
        2: [(cx, cy + size), (cx - size, cy - size // 2), (cx + size, cy - size // 2)],
        3: [(cx - size, cy), (cx + size // 2, cy - size), (cx + size // 2, cy + size)],
    }[d]
    pygame.draw.polygon(surface, color, points)


def draw_start(surface):
    surface.fill(BG)
    title = big_font.render("一 箭 又 一 箭", True, TEXT)
    surface.blit(title, (WIDTH // 2 - title.get_width() // 2, 220))
    tip = font.render("点击箭头，让它飞出棋盘", True, TEXT)
    surface.blit(tip, (WIDTH // 2 - tip.get_width() // 2, 320))
    tip2 = small_font.render("前方有箭头阻挡时会消耗失误次数", True, (120, 120, 120))
    surface.blit(tip2, (WIDTH // 2 - tip2.get_width() // 2, 370))
    btn = pygame.Rect(WIDTH // 2 - 100, 480, 200, 60)
    mx, my = pygame.mouse.get_pos()
    color = BTN_HOVER if btn.collidepoint(mx, my) else BTN
    pygame.draw.rect(surface, color, btn, border_radius=12)
    text = font.render("开始游戏", True, (255, 255, 255))
    surface.blit(text, (btn.centerx - text.get_width() // 2,
                        btn.centery - text.get_height() // 2))
    return btn


def draw_play(surface, g, lvl):
    surface.fill(BG)
    info1 = font.render("关卡：" + str(lvl + 1) + " / " + str(len(LEVELS)), True, TEXT)
    surface.blit(info1, (180, 30))
    info2 = font.render(
        "剩余箭头：" + str(g.remaining) + "    失误：" + str(g.mistakes) + "/" + str(g.max_mistakes),
        True, TEXT,
    )
    surface.blit(info2, (180, 68))

    mx, my = pygame.mouse.get_pos()
    color = BTN_HOVER if restart_rect.collidepoint(mx, my) else BTN
    pygame.draw.rect(surface, color, restart_rect, border_radius=8)
    btn_text = small_font.render("重新开始", True, (255, 255, 255))
    surface.blit(btn_text, (restart_rect.centerx - btn_text.get_width() // 2,
                            restart_rect.centery - btn_text.get_height() // 2))

    board_w = g.cols * CELL
    board_h = g.rows * CELL
    pygame.draw.rect(surface, (230, 230, 230),
                     (BOARD_X - 6, BOARD_Y - 6, board_w + 12, board_h + 12),
                     border_radius=10)

    for r in range(g.rows):
        for c in range(g.cols):
            d = g.grid[r][c]
            pygame.draw.rect(
                surface, CELL_BG,
                (BOARD_X + c * CELL + 4, BOARD_Y + r * CELL + 4,
                 CELL - 8, CELL - 8),
                border_radius=8,
            )
            if d is None:
                continue
            cx = BOARD_X + c * CELL + CELL // 2
            cy = BOARD_Y + r * CELL + CELL // 2
            offset_x = 0
            for anim in shake_anims:
                if anim["row"] == r and anim["col"] == c:
                    offset_x = int(8 * math.sin(anim["t"] * 40))
            draw_arrow_shape(surface, cx + offset_x, cy, d)

    for anim in fly_anims:
        dr, dc = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}[anim["dir"]]
        cx = BOARD_X + anim["col"] * CELL + CELL // 2 + dc * anim["t"] * 500
        cy = BOARD_Y + anim["row"] * CELL + CELL // 2 + dr * anim["t"] * 500
        draw_arrow_shape(surface, int(cx), int(cy), anim["dir"], color=(120, 180, 240))


def draw_result(surface, text):
    surface.fill(BG)
    t = big_font.render(text, True, TEXT)
    surface.blit(t, (WIDTH // 2 - t.get_width() // 2, 300))
    tip = font.render("点击任意位置返回开始界面", True, (120, 120, 120))
    surface.blit(tip, (WIDTH // 2 - tip.get_width() // 2, 400))


def main():
    global state, game, level_index, result_text

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                if state == STATE_START:
                    btn = pygame.Rect(WIDTH // 2 - 100, 480, 200, 60)
                    if btn.collidepoint(mx, my):
                        level_index = 0
                        game = Game(LEVELS[0])
                        fly_anims.clear()
                        shake_anims.clear()
                        state = STATE_PLAY

                elif state == STATE_PLAY and game is not None:
                    if restart_rect.collidepoint(mx, my):
                        game = Game(LEVELS[level_index])
                        fly_anims.clear()
                        shake_anims.clear()
                        continue

                    col = (mx - BOARD_X) // CELL
                    row = (my - BOARD_Y) // CELL
                    if 0 <= row < game.rows and 0 <= col < game.cols:
                        d = game.grid[row][col]
                        res = game.click(row, col)
                        if res == "fly" and d is not None:
                            fly_anims.append({"row": row, "col": col, "dir": d, "t": 0.0})
                        elif res == "block":
                            shake_anims.append({"row": row, "col": col, "t": 0.0})

                        if game.is_win():
                            if level_index + 1 < len(LEVELS):
                                level_index += 1
                                game = Game(LEVELS[level_index])
                                fly_anims.clear()
                                shake_anims.clear()
                            else:
                                result_text = "恭喜通关全部关卡！"
                                state = STATE_RESULT
                        elif game.is_lose():
                            result_text = "失败！失误次数用尽"
                            state = STATE_RESULT

                elif state == STATE_RESULT:
                    state = STATE_START

        for anim in fly_anims[:]:
            anim["t"] += dt
            if anim["t"] > 1.2:
                fly_anims.remove(anim)

        for anim in shake_anims[:]:
            anim["t"] += dt
            if anim["t"] > 0.25:
                shake_anims.remove(anim)

        if state == STATE_START:
            draw_start(screen)
        elif state == STATE_PLAY and game is not None:
            draw_play(screen, game, level_index)
        else:
            draw_result(screen, result_text)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()