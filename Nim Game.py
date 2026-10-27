import pygame
import sys
import time
import math
import random

pygame.init()
WIDTH, HEIGHT = 1100, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NIM GAME — Minimax vs Alpha-Beta")
clock = pygame.time.Clock()

BG        = (10, 12, 20)
PANEL     = (18, 22, 36)
ACCENT    = (0, 220, 180)
ACCENT2   = (255, 80, 120)
GOLD      = (255, 200, 60)
WHITE     = (240, 245, 255)
GRAY      = (80, 90, 110)
DARK_GRAY = (30, 36, 52)
GREEN     = (50, 220, 100)
RED       = (220, 60, 80)
BLUE      = (60, 140, 255)
PURPLE    = (160, 80, 255)
STONE_COL = [(0, 200, 160), (255, 100, 130), (255, 200, 60), (160, 80, 255)]

try:
    FONT_BIG  = pygame.font.SysFont("vcr osd mono", 42, bold=True)
    FONT_MED  = pygame.font.SysFont("vcr osd mono", 22, bold=True)
    FONT_SM   = pygame.font.SysFont("vcr osd mono", 16)
except:     
    FONT_BIG  = pygame.font.SysFont("consolas", 42)
    FONT_MED  = pygame.font.SysFont("consolas", 22)
    FONT_SM   = pygame.font.SysFont("consolas", 16)

# Level config: (heaps, max_depth, label)
LEVELS = [
    ([2, 3],       4, "EASY"),
    ([3, 4, 5],    6, "NORMAL"),
    ([4, 5, 6],    7, "HARD"),
    ([3, 5, 7],    7, "EXPERT"),
    ([4, 6, 8],    8, "MASTER"),
]


class NimGame:
    def __init__(self, level=0):
        self.level = max(0, min(level, len(LEVELS) - 1))
        self.reset()

    def reset(self):
        heaps, depth, _     = LEVELS[self.level]
        self.heaps          = list(heaps)
        self.max_depth      = depth
        self.current_player = 0   # 0=Human, 1=AI
        self.selected_heap  = None
        self.game_over      = False
        self.winner         = None
        self.stats = {
            "minimax":   {"time": 0.0, "nodes": 0, "depth": 0},
            "alphabeta": {"time": 0.0, "nodes": 0, "depth": 0},
        }
        self.last_ai_move    = None
        first               = "AI duluan!" if self.current_player == 1 else "Kamu duluan!"
        self.message         = f"{first} Pilih heap lalu pilih jumlah batu."
        self.particles       = []
        self.show_comparison = False
        self.ai_thinking     = self.current_player == 1

    # MINIMAX 
    def minimax(self, heaps, is_max, depth, counter):
        counter[0] += 1
        counter[1]  = max(counter[1], depth)
        if all(h == 0 for h in heaps):
            # last stone taken by the previous player (not is_max)
            return -1 if is_max else 1
        if depth >= self.max_depth:
            ns = 0
            for h in heaps:
                ns ^= h
            # nim-value: non-zero XOR = current player wins
            return 0.5 if ns != 0 else -0.5
        best = -math.inf if is_max else math.inf
        for i, h in enumerate(heaps):
            for take in range(1, h + 1):
                nh = heaps[:]
                nh[i] -= take
                val = self.minimax(nh, not is_max, depth + 1, counter)
                best = max(best, val) if is_max else min(best, val)
        return best

    def best_move_minimax(self):
        counter = [0, 0]
        t0 = time.perf_counter()
        best_val, best_move = -math.inf, None
        for i, h in enumerate(self.heaps):
            for take in range(1, h + 1):
                nh = self.heaps[:]
                nh[i] -= take
                val = self.minimax(nh, False, 1, counter)
                if val > best_val:
                    best_val, best_move = val, (i, take)
        self.stats["minimax"] = {
            "time":  round((time.perf_counter() - t0) * 1000, 3),
            "nodes": counter[0],
            "depth": counter[1],
        }
        return best_move

    #ALPHA-BETA 
    def alphabeta(self, heaps, is_max, alpha, beta, depth, counter):
        counter[0] += 1
        counter[1]  = max(counter[1], depth)
        if all(h == 0 for h in heaps):
            return -1 if is_max else 1
        if depth >= self.max_depth:
            ns = 0
            for h in heaps:
                ns ^= h
            return 0.5 if ns != 0 else -0.5
        best = -math.inf if is_max else math.inf
        for i, h in enumerate(heaps):
            for take in range(1, h + 1):
                nh = heaps[:]
                nh[i] -= take
                val = self.alphabeta(nh, not is_max, alpha, beta, depth + 1, counter)
                if is_max:
                    best  = max(best, val)
                    alpha = max(alpha, best)
                else:
                    best = min(best, val)
                    beta = min(beta, best)
                if beta <= alpha:
                    break
        return best

    def best_move_alphabeta(self):
        counter = [0, 0]
        t0 = time.perf_counter()
        best_val, best_move = -math.inf, None
        for i, h in enumerate(self.heaps):
            for take in range(1, h + 1):
                nh = self.heaps[:]
                nh[i] -= take
                val = self.alphabeta(nh, False, -math.inf, math.inf, 1, counter)
                if val > best_val:
                    best_val, best_move = val, (i, take)
        self.stats["alphabeta"] = {
            "time":  round((time.perf_counter() - t0) * 1000, 3),
            "nodes": counter[0],
            "depth": counter[1],
        }
        return best_move

    def do_ai_turn(self):
        self.best_move_minimax()          # untuk statistik
        move = self.best_move_alphabeta() # AI pakai alpha-beta
        if move:
            hi, take = move
            self.last_ai_move = move
            self._spawn(hi, take)
            self.heaps[hi] -= take
            self.message = (
                f"AI ambil {take} batu dari Heap {hi+1}  |  "
                f"MM: {self.stats['minimax']['nodes']} nodes  "
                f"AB: {self.stats['alphabeta']['nodes']} nodes"
            )
        self.show_comparison = True
        self.ai_thinking     = False
        self._check_win()

    def player_remove(self, hi, take):
        if take < 1 or take > self.heaps[hi]:
            return
        self._spawn(hi, take)
        self.heaps[hi]      -= take
        self.selected_heap   = None
        self._check_win()
        if not self.game_over:
            self.current_player = 1
            self.ai_thinking    = True
            self.message        = "AI thinking"

    def _check_win(self):
        if all(h == 0 for h in self.heaps):
            self.game_over = True
            self.winner    = self.current_player
            _, _, lbl      = LEVELS[self.level]
            if self.current_player == 0:
                next_lv = min(self.level + 1, len(LEVELS) - 1)
                suffix  = f" → Naik ke Level {next_lv+1} {LEVELS[next_lv][2]}!" if next_lv > self.level else " MAX LEVEL!"
                self.message = f"Kamu menang! Selamat!{suffix}"
            else:
                prev_lv = max(self.level - 1, 0)
                suffix  = f" → Turun ke Level {prev_lv+1} {LEVELS[prev_lv][2]}" if prev_lv < self.level else ""
                self.message = f"AI menang! Coba lagi.{suffix}"
        elif self.current_player == 1:
            self.current_player = 0
            self.message        = "Giliran kamu! Pilih heap dan ambil batu."

    def _spawn(self, hi, take):
        col = STONE_COL[hi % len(STONE_COL)]
        for _ in range(take * 5):
            self.particles.append({
                "x": 70 + hi * 200 + random.randint(-20, 60),
                "y": 155 + random.randint(-10, 60),
                "vx": random.uniform(-3, 3),
                "vy": random.uniform(-6, -2),
                "life": 1.0,
                "color": col,
                "r": random.randint(4, 9),
            })

    def update_particles(self):
        alive = []
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.3
            p["life"] -= 0.025
            if p["life"] > 0:
                alive.append(p)
        self.particles = alive


class Button:
    def __init__(self, x, y, w, h, text, color, tc=BG):
        self.rect    = pygame.Rect(x, y, w, h)
        self.text    = text
        self.color   = color
        self.tc      = tc
        self.hovered = False

    def draw(self, surf):
        c = tuple(min(255, x + 30) for x in self.color) if self.hovered else self.color
        pygame.draw.rect(surf, c,     self.rect, border_radius=8)
        pygame.draw.rect(surf, WHITE, self.rect, 1, border_radius=8)
        lbl = FONT_SM.render(self.text, True, self.tc)
        surf.blit(lbl, lbl.get_rect(center=self.rect.center))

    def update(self, pos):
        self.hovered = self.rect.collidepoint(pos)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


def rr(s, c, rect, r=10, bw=0, bc=None):
    pygame.draw.rect(s, c, rect, border_radius=r)
    if bw and bc:
        pygame.draw.rect(s, bc, rect, bw, border_radius=r)

def tc(s, t, f, c, cx, cy):
    lbl = f.render(t, True, c)
    s.blit(lbl, lbl.get_rect(center=(cx, cy)))

def tl(s, t, f, c, x, y):
    lbl = f.render(t, True, c)
    s.blit(lbl, (x, y))


def draw(game, b_reset, b_both, b_next, b_prev):
    screen.fill(BG)
    for gx in range(0, WIDTH, 60):
        pygame.draw.line(screen, (20, 26, 40), (gx, 0), (gx, HEIGHT))
    for gy in range(0, HEIGHT, 60):
        pygame.draw.line(screen, (20, 26, 40), (0, gy), (WIDTH, gy))

    # title
    _, _, lv_lbl = LEVELS[game.level]
    lv_colors    = [GREEN, ACCENT, GOLD, ACCENT2, RED]
    lv_col       = lv_colors[game.level]
    rr(screen, PANEL, pygame.Rect(20, 10, WIDTH - 40, 56), r=10)
    tc(screen, "N I M   G A M E", FONT_BIG, ACCENT, WIDTH // 2, 28)
    # level badge
    rr(screen, lv_col, pygame.Rect(30, 42, 130, 18), r=4)
    tc(screen, f"LV {game.level+1}  {lv_lbl}", FONT_SM, BG, 95, 51)
    tl(screen, f"Heaps: {game.heaps}   Depth: {game.max_depth}", FONT_SM, GRAY, 175, 44)

    # level progress dots
    for i in range(len(LEVELS)):
        col = lv_colors[i] if i <= game.level else DARK_GRAY
        pygame.draw.circle(screen, col, (WIDTH - 40 - (len(LEVELS) - 1 - i) * 22, 38), 7)
        if i == game.level:
            pygame.draw.circle(screen, WHITE, (WIDTH - 40 - (len(LEVELS) - 1 - i) * 22, 38), 7, 2)

    # heap panel
    rr(screen, PANEL, pygame.Rect(20, 78, 755, 298), r=12, bw=1, bc=DARK_GRAY)
    tl(screen, "HEAPS", FONT_MED, GRAY, 36, 86)

    n_heaps = len(game.heaps)
    gap_x   = 755 // (n_heaps + 1)
    COLS_N, GAP, SR = 4, 38, 14
    for hi, count in enumerate(game.heaps):
        hx     = 20 + gap_x * (hi + 1) - 30
        hy     = 152
        col    = STONE_COL[hi % len(STONE_COL)]
        is_sel = (game.selected_heap == hi)
        rr(screen, col if is_sel else DARK_GRAY,
           pygame.Rect(hx - 10, hy - 44, 120, 28), r=7)
        tc(screen, f"H{hi+1} [{count}]", FONT_SM,
           BG if is_sel else GRAY, hx + 50, hy - 30)
        for si in range(count):
            sx = hx + (si % COLS_N) * GAP
            sy = hy + (si // COLS_N) * GAP
            pygame.draw.circle(screen, col, (sx, sy), SR)
            pygame.draw.circle(screen, WHITE, (sx, sy), SR, 2)
            pygame.draw.circle(screen, tuple(min(255, c + 60) for c in col),
                               (sx - 3, sy - 3), SR // 3)
            if is_sel and game.current_player == 0 and not game.game_over:
                pygame.draw.circle(screen, ACCENT, (sx, sy), SR + 4, 2)

    # message
    mr = pygame.Rect(20, 388, 755, 42)
    bc = GOLD if game.game_over else (ACCENT2 if game.ai_thinking else ACCENT)
    rr(screen, DARK_GRAY, mr, r=8, bw=1, bc=bc)
    mc = GOLD if game.game_over else (ACCENT2 if game.ai_thinking else WHITE)
    tc(screen, game.message[:90], FONT_SM, mc, mr.centerx, mr.centery)

    # remove buttons
    if game.current_player == 0 and not game.game_over and game.selected_heap is not None:
        rr(screen, PANEL, pygame.Rect(20, 440, 755, 50), r=8)
        mt = game.heaps[game.selected_heap]
        tl(screen, f"Ambil dari Heap {game.selected_heap+1}:", FONT_SM, GRAY, 36, 453)
        for i in range(1, mt + 1):
            bx = 260 + (i - 1) * 46
            rr(screen, ACCENT, pygame.Rect(bx, 450, 38, 28), r=6)
            tc(screen, str(i), FONT_SM, BG, bx + 19, 464)

    # turn indicator
    if not game.game_over:
        ic = BLUE if game.current_player == 0 else RED
        it = "GILIRAN KAMU" if game.current_player == 0 else "GILIRAN AI"
        rr(screen, ic, pygame.Rect(20, 502, 148, 28), r=6)
        tc(screen, it, FONT_SM, WHITE, 94, 516)

    b_reset.draw(screen)
    b_both.draw(screen)
    b_next.draw(screen)
    b_prev.draw(screen)

    # side panel
    sx, sy = 793, 78
    for idx, (key, lbl, col) in enumerate([
            ("minimax",   "MINIMAX",    ACCENT),
            ("alphabeta", "ALPHA-BETA", ACCENT2)]):
        py = sy + idx * 150
        rr(screen, PANEL, pygame.Rect(sx, py, 290, 138), r=10, bw=2, bc=col)
        tl(screen, lbl, FONT_MED, col, sx + 12, py + 10)
        s = game.stats[key]
        for ri, (k, v) in enumerate([
                ("Waktu (ms)", f'{s["time"]:.3f}'),
                ("Nodes",      str(s["nodes"])),
                ("Max Depth",  str(s["depth"]))]):
            tl(screen, k, FONT_SM, GRAY,  sx + 16,  py + 46 + ri * 28)
            tl(screen, v, FONT_SM, WHITE, sx + 170, py + 46 + ri * 28)

    if game.show_comparison:
        smm = game.stats["minimax"]
        sab = game.stats["alphabeta"]
        if smm["nodes"] > 0 and sab["nodes"] > 0:
            pct   = round((1 - sab["nodes"] / smm["nodes"]) * 100, 1)
            badge = pygame.Rect(sx, sy + 306, 290, 62)
            rr(screen, DARK_GRAY, badge, r=10, bw=2, bc=GOLD)
            tc(screen, "PRUNING SAVINGS", FONT_SM, GOLD,  badge.centerx, badge.y + 20)
            tc(screen, f"{pct}% less nodes", FONT_MED, GREEN,
               badge.centerx, badge.y + 46)

    info_y = sy + 382
    rr(screen, DARK_GRAY, pygame.Rect(sx, info_y, 290, 96), r=8)
    for i, ln in enumerate([
            "Kedua algoritma jalan tiap",
            "giliran AI untuk perbandingan.",
            f"Heaps sekarang: {game.heaps}",
            "AI menggunakan Alpha-Beta"]):
        tl(screen, ln, FONT_SM, GRAY, sx + 10, info_y + 10 + i * 22)

    for p in game.particles:
        a    = max(0, int(p["life"] * 255))
        surf = pygame.Surface((p["r"] * 2, p["r"] * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*p["color"], a), (p["r"], p["r"]), p["r"])
        screen.blit(surf, (int(p["x"] - p["r"]), int(p["y"] - p["r"])))

    pygame.display.flip()


def get_heap(pos, heaps):
    n_heaps = len(heaps)
    gap_x   = 755 // (n_heaps + 1)
    COLS_N, GAP = 4, 38
    for hi in range(n_heaps):
        hx, hy = 20 + gap_x * (hi + 1) - 30, 152
        if pygame.Rect(hx - 10, hy - 44, 120, 28).collidepoint(pos):
            return hi
        rows = max(1, math.ceil(heaps[hi] / COLS_N))
        if pygame.Rect(hx - 10, hy - 10, COLS_N * GAP + 10,
                       rows * GAP + 10).collidepoint(pos):
            return hi
    return None

def get_remove(pos, sel, heaps):
    if sel is None:
        return None
    for i in range(1, heaps[sel] + 1):
        if pygame.Rect(260 + (i - 1) * 46, 450, 38, 28).collidepoint(pos):
            return i
    return None


def main():
    current_level = 0
    game     = NimGame(current_level)
    ai_timer = 0
    b_reset  = Button(178, 502, 130, 28, "NEW GAME",     ACCENT,  BG)
    b_both   = Button(318, 502, 160, 28, "RUN BOTH NOW", PURPLE,  WHITE)
    b_next   = Button(488, 502, 130, 28, "NEXT LEVEL",   GREEN,   BG)
    b_prev   = Button(628, 502, 130, 28, "PREV LEVEL",   GOLD,    BG)

    while True:
        clock.tick(60)
        game.update_particles()

        mp = pygame.mouse.get_pos()
        b_reset.update(mp)
        b_both.update(mp)
        b_next.update(mp)
        b_prev.update(mp)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                p = event.pos

                if b_reset.clicked(p):
                    game     = NimGame(current_level)
                    ai_timer = 0
                    continue

                if b_next.clicked(p):
                    current_level = min(current_level + 1, len(LEVELS) - 1)
                    game     = NimGame(current_level)
                    ai_timer = 0
                    continue

                if b_prev.clicked(p):
                    current_level = max(current_level - 1, 0)
                    game     = NimGame(current_level)
                    ai_timer = 0
                    continue

                if b_both.clicked(p):
                    game.best_move_minimax()
                    game.best_move_alphabeta()
                    game.show_comparison = True
                    continue

                if game.current_player == 0 and not game.game_over:
                    take = get_remove(p, game.selected_heap, game.heaps)
                    if take is not None:
                        game.player_remove(game.selected_heap, take)
                        ai_timer = 60
                    else:
                        hi = get_heap(p, game.heaps)
                        if hi is not None and game.heaps[hi] > 0:
                            game.selected_heap = hi
                            game.message = (
                                f"Heap {hi+1} dipilih - "
                                f"ambil berapa? (1 - {game.heaps[hi]})"
                            )

        if game.current_player == 1 and not game.game_over:
            if ai_timer > 0:
                ai_timer -= 1
            else:
                game.do_ai_turn()
                ai_timer = 0
                if game.game_over:
                    if game.winner == 0:
                        current_level = min(current_level + 1, len(LEVELS) - 1)
                    else:
                        current_level = max(current_level - 1, 0)

        draw(game, b_reset, b_both, b_next, b_prev)


if __name__ == "__main__":
    main()