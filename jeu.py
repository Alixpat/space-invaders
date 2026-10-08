#!/usr/bin/env python3
"""Space Invaders façon Atari 2600 (1980).

Tout est généré par le code : sprites, police et sons. Aucun fichier externe.
Lancement : .venv/bin/python jeu.py
"""

import math
import random
from array import array
from pathlib import Path

import pygame

# --- Écran ---------------------------------------------------------------
# On dessine sur une petite surface « logique » puis on l'agrandit avec des
# pixels plus larges que hauts, comme une Atari 2600 branchée sur une télé.
W, H = 160, 200
SX, SY = 5, 3
WIN_W, WIN_H = W * SX, H * SY
FPS = 60

# --- Palette -------------------------------------------------------------
BLACK = (0, 0, 0)
WHITE = (236, 236, 236)
PLAYER_COLOR = (162, 162, 42)
RECORD_COLOR = (84, 138, 210)
BUNKER_COLOR = (180, 122, 48)
GROUND_COLOR = (136, 146, 62)
UFO_COLOR = (200, 72, 72)
ROW_COLORS = [
    (214, 92, 214),
    (200, 72, 72),
    (232, 204, 99),
    (80, 200, 120),
    (84, 138, 210),
    (66, 200, 200),
]

# --- Disposition (en pixels logiques) ------------------------------------
ROWS, COLS = 6, 6
COL_GAP, ROW_GAP = 16, 12
ALIEN_W = ALIEN_H = 8
STEP_X, STEP_DOWN = 2, 6
FORMATION_Y = 26
UFO_Y = 15
UFO_SPEED = 30
PLAYER_Y = 168
PLAYER_W, PLAYER_H = 9, 5
PLAYER_SPEED = 70
GROUND_Y = 178
BUNKER_Y = 144
BULLET_SPEED = 190
BOMB_SPEED = 65
START_LIVES = 3

RECORD_FILE = Path(__file__).with_name("record.txt")

# --- Sprites ("#" = pixel allumé) ----------------------------------------
SQUID = [
    [
        "...##...",
        "..####..",
        ".######.",
        "##.##.##",
        "########",
        "..#..#..",
        ".#.##.#.",
        "#.#..#.#",
    ],
    [
        "...##...",
        "..####..",
        ".######.",
        "##.##.##",
        "########",
        ".#.##.#.",
        "#......#",
        ".#....#.",
    ],
]
CRAB = [
    [
        "..#..#..",
        "...##...",
        "..####..",
        ".#.##.#.",
        "########",
        "#.####.#",
        "#.#..#.#",
        "..#..#..",
    ],
    [
        "..#..#..",
        "#..##..#",
        "#.####.#",
        "##.##.##",
        "########",
        ".######.",
        "..#..#..",
        ".#....#.",
    ],
]
OCTOPUS = [
    [
        "..####..",
        ".######.",
        "########",
        "##.##.##",
        "########",
        "..#..#..",
        ".#.##.#.",
        "#......#",
    ],
    [
        "..####..",
        ".######.",
        "########",
        "##.##.##",
        "########",
        ".##..##.",
        "##....##",
        ".#....#.",
    ],
]
# Deux rangées de chaque type, du haut vers le bas.
ALIEN_TYPES = [SQUID, SQUID, CRAB, CRAB, OCTOPUS, OCTOPUS]

ALIEN_EXPLOSION = [
    "#..#...#",
    ".#.#..#.",
    "..#..#..",
    "##....##",
    "..#..#..",
    ".#..#.#.",
    "#...#..#",
    "........",
]
PLAYER = [
    "....#....",
    "...###...",
    ".#######.",
    "#########",
    "#########",
]
PLAYER_EXPLOSION = [
    [
        "..#..#...",
        "#...#..#.",
        "..#####..",
        ".#######.",
        "#########",
    ],
    [
        "#...#...#",
        ".#.....#.",
        "...#.#...",
        ".##.###.#",
        "#########",
    ],
]
UFO = [
    "...####...",
    ".########.",
    "##.#..#.##",
    "##########",
    "..#....#..",
]
BUNKER = [
    "..########..",
    ".##########.",
    "############",
    "############",
    "############",
    "############",
    "############",
    "####....####",
    "###......###",
    "###......###",
]

# --- Police 3x5 ----------------------------------------------------------
FONT = {
    "0": ["###", "#.#", "#.#", "#.#", "###"],
    "1": [".#.", "##.", ".#.", ".#.", "###"],
    "2": ["###", "..#", "###", "#..", "###"],
    "3": ["###", "..#", "###", "..#", "###"],
    "4": ["#.#", "#.#", "###", "..#", "..#"],
    "5": ["###", "#..", "###", "..#", "###"],
    "6": ["###", "#..", "###", "#.#", "###"],
    "7": ["###", "..#", "..#", ".#.", ".#."],
    "8": ["###", "#.#", "###", "#.#", "###"],
    "9": ["###", "#.#", "###", "..#", "###"],
    "A": [".#.", "#.#", "###", "#.#", "#.#"],
    "B": ["##.", "#.#", "##.", "#.#", "##."],
    "C": ["###", "#..", "#..", "#..", "###"],
    "D": ["##.", "#.#", "#.#", "#.#", "##."],
    "E": ["###", "#..", "##.", "#..", "###"],
    "F": ["###", "#..", "##.", "#..", "#.."],
    "G": ["###", "#..", "#.#", "#.#", "###"],
    "H": ["#.#", "#.#", "###", "#.#", "#.#"],
    "I": ["###", ".#.", ".#.", ".#.", "###"],
    "J": ["..#", "..#", "..#", "#.#", "###"],
    "K": ["#.#", "#.#", "##.", "#.#", "#.#"],
    "L": ["#..", "#..", "#..", "#..", "###"],
    "M": ["#.#", "###", "###", "#.#", "#.#"],
    "N": ["##.", "#.#", "#.#", "#.#", "#.#"],
    "O": ["###", "#.#", "#.#", "#.#", "###"],
    "P": ["###", "#.#", "###", "#..", "#.."],
    "Q": ["###", "#.#", "#.#", "###", "..#"],
    "R": ["##.", "#.#", "##.", "#.#", "#.#"],
    "S": ["###", "#..", "###", "..#", "###"],
    "T": ["###", ".#.", ".#.", ".#.", ".#."],
    "U": ["#.#", "#.#", "#.#", "#.#", "###"],
    "V": ["#.#", "#.#", "#.#", "#.#", ".#."],
    "W": ["#.#", "#.#", "###", "###", "#.#"],
    "X": ["#.#", "#.#", ".#.", "#.#", "#.#"],
    "Y": ["#.#", "#.#", ".#.", ".#.", ".#."],
    "Z": ["###", "..#", ".#.", "#..", "###"],
    " ": ["...", "...", "...", "...", "..."],
    "-": ["...", "...", "###", "...", "..."],
    "=": ["...", "###", "...", "###", "..."],
    ":": ["...", ".#.", "...", ".#.", "..."],
    "!": [".#.", ".#.", ".#.", "...", ".#."],
    "?": ["###", "..#", ".#.", "...", ".#."],
}

_glyph_cache = {}


def make_sprite(rows, color):
    surf = pygame.Surface((len(rows[0]), len(rows)), pygame.SRCALPHA)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == "#":
                surf.set_at((x, y), color)
    return surf


def glyph(ch, color, scale):
    key = (ch, color, scale)
    if key not in _glyph_cache:
        surf = pygame.Surface((3 * scale, 5 * scale), pygame.SRCALPHA)
        for y, row in enumerate(FONT.get(ch, FONT["?"])):
            for x, px in enumerate(row):
                if px == "#":
                    surf.fill(color, (x * scale, y * scale, scale, scale))
        _glyph_cache[key] = surf
    return _glyph_cache[key]


def text_width(text, scale=1):
    return max(0, len(text) * 4 * scale - scale)


def draw_text(surf, text, x, y, color, scale=1, center=False):
    if center:
        x = (W - text_width(text, scale)) // 2
    for i, ch in enumerate(text.upper()):
        surf.blit(glyph(ch, color, scale), (x + i * 4 * scale, y))


# --- Sons synthétisés ----------------------------------------------------
class Sfx:
    def __init__(self, sound=None):
        self.sound = sound

    def play(self, loops=0):
        if self.sound:
            self.sound.play(loops=loops)

    def stop(self):
        if self.sound:
            self.sound.stop()


def build_sounds():
    init = pygame.mixer.get_init()
    if not init:
        silent = Sfx()
        return {
            "shoot": silent, "kill": silent, "die": silent,
            "ufo": silent, "ufo_hit": silent, "march": [silent] * 4,
        }
    rate, _, channels = init

    def render(samples, volume):
        buf = array("h")
        for s in samples:
            v = int(max(-1.0, min(1.0, s)) * 32767 * volume)
            buf.extend((v,) * channels)
        return Sfx(pygame.mixer.Sound(buffer=buf.tobytes()))

    def wave(dur, freq, env, shape="square"):
        out, phase = [], 0.0
        for i in range(int(dur * rate)):
            t = i / rate
            phase = (phase + freq(t) / rate) % 1.0
            if shape == "square":
                s = 1.0 if phase < 0.5 else -1.0
            else:
                s = 4.0 * abs(phase - 0.5) - 1.0
            out.append(s * env(t))
        return out

    def noise(dur, hold, env):
        # Bruit « échantillonné-bloqué » : plus hold est grand, plus c'est grave.
        out, v = [], 0.0
        for i in range(int(dur * rate)):
            t = i / rate
            if i % max(1, int(hold(t))) == 0:
                v = random.uniform(-1.0, 1.0)
            out.append(v * env(t))
        return out

    return {
        "shoot": render(wave(0.18, lambda t: 1400 - 6000 * t, lambda t: 1 - t / 0.18), 0.22),
        "kill": render(noise(0.25, lambda t: 2 + t * 40, lambda t: (1 - t / 0.25) ** 2), 0.35),
        "die": render(noise(1.2, lambda t: 3 + t * 30, lambda t: (1 - t / 1.2) ** 1.5), 0.45),
        "ufo": render(
            wave(1 / 3, lambda t: 700 + 250 * math.sin(2 * math.pi * 6 * t), lambda t: 1.0, "tri"),
            0.15,
        ),
        "ufo_hit": render(
            wave(0.7, lambda t: 900 - 900 * t + 150 * math.sin(2 * math.pi * 20 * t),
                 lambda t: 1 - t / 0.7),
            0.22,
        ),
        "march": [
            render(wave(0.09, lambda t, f=f: f, lambda t: 1 - t / 0.09), 0.4)
            for f in (98, 87, 78, 73)
        ],
    }


# --- Record --------------------------------------------------------------
def load_record():
    try:
        return int(RECORD_FILE.read_text().strip())
    except (OSError, ValueError):
        return 0


def save_record(value):
    try:
        RECORD_FILE.write_text(f"{value}\n")
    except OSError:
        pass


# --- Boucliers -----------------------------------------------------------
class Bunker:
    def __init__(self, cx):
        self.surf = make_sprite(BUNKER, BUNKER_COLOR)
        self.rect = self.surf.get_rect(midtop=(cx, BUNKER_Y))

    def hit(self, rect, from_below):
        """Renvoie True (et abîme le bouclier) si rect touche un pixel plein."""
        area = rect.clip(self.rect)
        if not area:
            return False
        if from_below:
            ys = range(area.bottom - 1, area.top - 1, -1)
        else:
            ys = range(area.top, area.bottom)
        for y in ys:
            for x in range(area.left, area.right):
                lx, ly = x - self.rect.x, y - self.rect.y
                if self.surf.get_at((lx, ly)).a:
                    self.damage(lx, ly)
                    return True
        return False

    def damage(self, lx, ly):
        w, h = self.surf.get_size()
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if abs(dx) + abs(dy) <= 1 or random.random() < 0.5:
                    x, y = lx + dx, ly + dy
                    if 0 <= x < w and 0 <= y < h:
                        self.surf.set_at((x, y), (0, 0, 0, 0))

    def erase(self, rect):
        area = rect.clip(self.rect)
        if area:
            self.surf.fill((0, 0, 0, 0), area.move(-self.rect.x, -self.rect.y))


# --- Jeu -----------------------------------------------------------------
class Game:
    def __init__(self):
        self.window = pygame.display.get_surface()
        self.screen = pygame.Surface((W, H))
        self.scanlines = pygame.Surface((WIN_W, WIN_H), pygame.SRCALPHA)
        for y in range(SY - 1, WIN_H, SY):
            self.scanlines.fill((0, 0, 0, 80), (0, y, WIN_W, 1))
        self.crt = True

        self.sfx = build_sounds()
        self.alien_frames = [
            [make_sprite(frame, ROW_COLORS[r]) for frame in ALIEN_TYPES[r]]
            for r in range(ROWS)
        ]
        self.alien_boom = make_sprite(ALIEN_EXPLOSION, WHITE)
        self.player_img = make_sprite(PLAYER, PLAYER_COLOR)
        self.player_boom = [make_sprite(f, PLAYER_COLOR) for f in PLAYER_EXPLOSION]
        self.ufo_img = make_sprite(UFO, UFO_COLOR)

        self.highscore = load_record()
        self.state = "title"
        self.state_timer = 0.0
        self.blink = 0.0
        self.paused = False
        self.score = 0
        self.lives = START_LIVES
        self.level = 1
        self.ufo = None
        self.new_wave()

    # -- mise en place --
    def new_game(self):
        self.score = 0
        self.lives = START_LIVES
        self.level = 1
        self.new_wave()
        self.set_state("playing")

    def new_wave(self):
        self.alive = [[True] * COLS for _ in range(ROWS)]
        self.fx = (W - ((COLS - 1) * COL_GAP + ALIEN_W)) // 2
        self.fy = FORMATION_Y + min(self.level - 1, 4) * STEP_DOWN
        self.dir = 1
        self.step_timer = 0.0
        self.anim = 0
        self.march_i = 0
        self.bunkers = [Bunker(W * i // 4) for i in (1, 2, 3)]
        self.px = (W - PLAYER_W) / 2
        self.bullet = None
        self.bombs = []
        self.explosions = []
        self.popups = []
        self.stop_ufo()
        self.ufo_timer = random.uniform(12, 22)
        self.bomb_timer = random.uniform(1.0, 2.0)

    def set_state(self, state):
        self.state = state
        self.state_timer = 0.0

    def stop_ufo(self):
        self.ufo = None
        self.sfx["ufo"].stop()

    # -- utilitaires --
    def alien_rect(self, r, c):
        return pygame.Rect(self.fx + c * COL_GAP, self.fy + r * ROW_GAP, ALIEN_W, ALIEN_H)

    def alive_cells(self):
        return [(r, c) for r in range(ROWS) for c in range(COLS) if self.alive[r][c]]

    def step_interval(self):
        n = len(self.alive_cells())
        return max(0.03, (0.05 + 0.018 * n) * 0.88 ** (self.level - 1))

    def ufo_rect(self):
        return pygame.Rect(int(self.ufo["x"]), UFO_Y, len(UFO[0]), len(UFO))

    def player_rect(self):
        return pygame.Rect(int(self.px), PLAYER_Y, PLAYER_W, PLAYER_H)

    # -- événements --
    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        start = event.key in (pygame.K_SPACE, pygame.K_RETURN)
        if event.key == pygame.K_c:
            self.crt = not self.crt
        elif self.state == "title" and start:
            self.new_game()
        elif self.state == "gameover" and start and self.state_timer > 1.0:
            self.new_game()
        elif self.state == "playing" and event.key == pygame.K_p:
            self.paused = not self.paused
            if pygame.mixer.get_init():
                if self.paused:
                    pygame.mixer.pause()
                else:
                    pygame.mixer.unpause()

    # -- mise à jour --
    def update(self, dt, keys):
        self.blink += dt
        if self.paused:
            return
        self.state_timer += dt
        self.explosions = [[x, y, t - dt] for x, y, t in self.explosions if t > dt]
        self.popups = [[x, y, t - dt, txt] for x, y, t, txt in self.popups if t > dt]

        if self.state == "playing":
            self.update_play(dt, keys)
        elif self.state == "dying" and self.state_timer >= 1.6:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over()
            else:
                self.px = (W - PLAYER_W) / 2
                self.set_state("playing")
        elif self.state == "interlude" and self.state_timer >= 1.5:
            self.new_wave()
            self.set_state("playing")

    def update_play(self, dt, keys):
        left = keys[pygame.K_LEFT] or keys[pygame.K_q] or keys[pygame.K_a]
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        fire = keys[pygame.K_SPACE] or keys[pygame.K_UP]

        self.px += (right - left) * PLAYER_SPEED * dt
        self.px = max(2, min(W - 2 - PLAYER_W, self.px))
        if fire and self.bullet is None:
            self.bullet = [self.px + PLAYER_W // 2, PLAYER_Y - 4.0]
            self.sfx["shoot"].play()

        self.step_timer += dt
        if self.step_timer >= self.step_interval():
            self.step_timer = 0.0
            self.step_formation()
            if self.state != "playing":
                return

        self.update_bullet(dt)
        self.update_bombs(dt)
        if self.state != "playing":
            return
        self.update_ufo(dt)

        if not self.alive_cells():
            self.level += 1
            self.stop_ufo()
            self.set_state("interlude")

    def step_formation(self):
        cells = self.alive_cells()
        if not cells:
            return
        cols = [c for _, c in cells]
        left = self.fx + min(cols) * COL_GAP
        right = self.fx + max(cols) * COL_GAP + ALIEN_W
        if (self.dir > 0 and right + STEP_X > W - 2) or (self.dir < 0 and left - STEP_X < 2):
            self.fy += STEP_DOWN
            self.dir = -self.dir
        else:
            self.fx += self.dir * STEP_X
        self.anim ^= 1
        self.sfx["march"][self.march_i].play()
        self.march_i = (self.march_i + 1) % 4

        # Les envahisseurs rongent les boucliers qu'ils traversent.
        for r, c in cells:
            rect = self.alien_rect(r, c)
            for bunker in self.bunkers:
                bunker.erase(rect)

        bottom = max(r for r, _ in cells)
        if self.fy + bottom * ROW_GAP + ALIEN_H >= PLAYER_Y:
            self.lives = 1  # invasion : la partie est finie
            self.player_hit()

    def update_bullet(self, dt):
        if self.bullet is None:
            return
        self.bullet[1] -= BULLET_SPEED * dt
        rect = pygame.Rect(int(self.bullet[0]), int(self.bullet[1]), 1, 4)
        if rect.bottom < 10:
            self.bullet = None
            return
        for bunker in self.bunkers:
            if bunker.hit(rect, from_below=True):
                self.bullet = None
                return
        for r, c in self.alive_cells():
            arect = self.alien_rect(r, c)
            if arect.colliderect(rect):
                self.alive[r][c] = False
                self.score += (ROWS - r) * 5
                self.explosions.append([arect.x, arect.y, 0.25])
                self.sfx["kill"].play()
                self.bullet = None
                return
        if self.ufo and self.ufo_rect().colliderect(rect):
            value = random.choice([50, 100, 150, 300])
            self.score += value
            urect = self.ufo_rect()
            self.popups.append([urect.x, urect.y, 1.2, str(value)])
            self.stop_ufo()
            self.sfx["ufo_hit"].play()
            self.bullet = None
            return
        for bomb in self.bombs:
            if pygame.Rect(int(bomb[0]) - 1, int(bomb[1]), 3, 5).colliderect(rect):
                self.bombs.remove(bomb)
                self.bullet = None
                return

    def drop_bomb(self):
        cells = self.alive_cells()
        cols = sorted({c for _, c in cells})
        if random.random() < 0.35:
            # Viser la colonne la plus proche du joueur.
            pcx = self.px + PLAYER_W / 2
            col = min(cols, key=lambda c: abs(self.fx + c * COL_GAP + ALIEN_W / 2 - pcx))
        else:
            col = random.choice(cols)
        row = max(r for r, c in cells if c == col)
        rect = self.alien_rect(row, col)
        self.bombs.append([float(rect.centerx), float(rect.bottom)])

    def update_bombs(self, dt):
        self.bomb_timer -= dt
        if self.bomb_timer <= 0:
            self.bomb_timer = random.uniform(0.5, 1.4) * 0.9 ** (self.level - 1)
            if self.alive_cells() and len(self.bombs) < min(2 + self.level // 2, 5):
                self.drop_bomb()

        speed = BOMB_SPEED + 5 * (self.level - 1)
        player = self.player_rect()
        for bomb in self.bombs[:]:
            bomb[1] += speed * dt
            rect = pygame.Rect(int(bomb[0]) - 1, int(bomb[1]), 3, 5)
            if rect.colliderect(player):
                self.player_hit()
                return
            if rect.bottom >= GROUND_Y or any(b.hit(rect, from_below=False) for b in self.bunkers):
                self.bombs.remove(bomb)

    def update_ufo(self, dt):
        if self.ufo is None:
            self.ufo_timer -= dt
            if self.ufo_timer <= 0:
                self.ufo_timer = random.uniform(15, 25)
                if len(self.alive_cells()) >= 6:
                    direction = random.choice([-1, 1])
                    x = -len(UFO[0]) if direction > 0 else W
                    self.ufo = {"x": float(x), "dir": direction}
                    self.sfx["ufo"].play(loops=-1)
        else:
            self.ufo["x"] += self.ufo["dir"] * UFO_SPEED * dt
            if self.ufo["x"] < -len(UFO[0]) - 1 or self.ufo["x"] > W + 1:
                self.stop_ufo()

    def player_hit(self):
        self.bullet = None
        self.bombs = []
        self.stop_ufo()
        self.sfx["die"].play()
        self.set_state("dying")

    def game_over(self):
        self.set_state("gameover")
        if self.score > self.highscore:
            self.highscore = self.score
            save_record(self.highscore)

    # -- affichage --
    def draw(self):
        s = self.screen
        s.fill(BLACK)
        draw_text(s, f"{self.score:04d}", 4, 2, PLAYER_COLOR, 2)
        record = f"{max(self.highscore, self.score):04d}"
        draw_text(s, record, W - 4 - text_width(record, 2), 2, RECORD_COLOR, 2)

        if self.state == "title":
            self.draw_title()
        else:
            self.draw_field()

        pygame.transform.scale(s, (WIN_W, WIN_H), self.window)
        if self.crt:
            self.window.blit(self.scanlines, (0, 0))
        pygame.display.flip()

    def draw_title(self):
        s = self.screen
        draw_text(s, "SPACE", 0, 20, ROW_COLORS[2], 3, center=True)
        draw_text(s, "INVADERS", 0, 40, ROW_COLORS[0], 3, center=True)
        for r in range(ROWS):
            y = 64 + r * 10
            s.blit(self.alien_frames[r][int(self.blink * 2) % 2], (56, y))
            draw_text(s, f"= {(ROWS - r) * 5} PTS", 70, y + 2, WHITE)
        s.blit(self.ufo_img, (55, 126))
        draw_text(s, "= ? PTS", 70, 126, WHITE)
        if int(self.blink * 2) % 2 == 0:
            draw_text(s, "ESPACE POUR JOUER", 0, 150, PLAYER_COLOR, center=True)
        draw_text(s, "FLECHES: BOUGER  ESPACE: TIRER", 0, 172, GROUND_COLOR, center=True)
        draw_text(s, "P: PAUSE  C: TELE  ECHAP: QUITTER", 0, 182, GROUND_COLOR, center=True)

    def draw_field(self):
        s = self.screen
        for r, c in self.alive_cells():
            s.blit(self.alien_frames[r][self.anim], self.alien_rect(r, c).topleft)
        for x, y, _ in self.explosions:
            s.blit(self.alien_boom, (x, y))
        if self.ufo:
            s.blit(self.ufo_img, self.ufo_rect().topleft)
        for x, y, _, txt in self.popups:
            draw_text(s, txt, x, y, UFO_COLOR)
        for bunker in self.bunkers:
            s.blit(bunker.surf, bunker.rect)

        if self.state == "dying":
            frame = int(self.state_timer * 10) % 2
            s.blit(self.player_boom[frame], (int(self.px), PLAYER_Y))
        elif self.state in ("playing", "interlude"):
            s.blit(self.player_img, (int(self.px), PLAYER_Y))

        if self.bullet:
            s.fill(WHITE, (int(self.bullet[0]), int(self.bullet[1]), 1, 4))
        for bx, by in self.bombs:
            zig = (0, 1, 0, -1, 0) if int(by / 3) % 2 else (0, -1, 0, 1, 0)
            for i, dx in enumerate(zig):
                s.set_at((int(bx) + dx, int(by) + i), WHITE)

        s.fill(GROUND_COLOR, (0, GROUND_Y, W, 2))
        draw_text(s, str(self.lives), 4, GROUND_Y + 6, PLAYER_COLOR)
        for i in range(max(0, self.lives - 1)):
            s.blit(self.player_img, (12 + i * 12, GROUND_Y + 6))
        vague = f"VAGUE {self.level}"
        draw_text(s, vague, W - 4 - text_width(vague), GROUND_Y + 6, GROUND_COLOR)

        if self.state == "interlude":
            draw_text(s, vague, 0, 90, WHITE, 2, center=True)
        elif self.state == "gameover":
            draw_text(s, "PARTIE TERMINEE", 0, 80, UFO_COLOR, 2, center=True)
            if self.state_timer > 1.0 and int(self.blink * 2) % 2 == 0:
                draw_text(s, "ESPACE POUR REJOUER", 0, 104, WHITE, center=True)
        if self.paused:
            draw_text(s, "PAUSE", 0, 90, WHITE, 2, center=True)


def main():
    pygame.mixer.pre_init(22050, -16, 1, 512)
    pygame.init()
    pygame.display.set_caption("Space Invaders")
    pygame.display.set_mode((WIN_W, WIN_H))
    game = Game()
    clock = pygame.time.Clock()

    running = True
    while running:
        dt = min(clock.tick(FPS) / 1000, 0.05)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                running = False
            else:
                game.handle_event(event)
        game.update(dt, pygame.key.get_pressed())
        game.draw()

    pygame.quit()


if __name__ == "__main__":
    main()
