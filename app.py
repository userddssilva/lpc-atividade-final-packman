import sys

from enemy import *
from player import *

pygame.init()


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.running = True
        self.state = 'menu'

        self.cell_width = MAZE_WIDTH//COLS
        self.cell_height = MAZE_HEIGHT//ROWS

        self.walls = []
        self.coins = []
        self.enemies = []

        self.e_pos = []
        self.p_pos = None

        self.load()
        self.player = Player(self, Vector2(self.p_pos))
        self.make_enemies()

    def run(self):
        while self.running:
            if self.state == 'menu':
                self.menu_events()
                self.menu_draw()
            elif self.state == 'credit':
                self.credits_draw()
                self.credits_events()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            else:
                file = open("highscore.txt", "w")
                file.write('0')
                file.close()
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    ''' helper functions '''

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.Font(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

    def load(self):
        self.background = pygame.image.load('Sprites/maze.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        # Opening walls file
        # Creating walls list with co-ords of walls
        # stored as a Vector2
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(Vector2(xidx, yidx))
                    elif char == "C":
                        self.coins.append(Vector2(xidx, yidx))
                    elif char == "P":
                        self.p_pos = [xidx, yidx]
                    elif char in ["2", "3", "4", "5"]:
                        self.e_pos.append([xidx, yidx])
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xidx * self.cell_width, yidx * self.cell_height,
                                                                  self.cell_width, self.cell_height))

    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, Vector2(pos), idx))

    def draw_grid(self):
        for x in range(WIDTH // self.cell_width):
            pygame.draw.line(self.background, GREY, (x * self.cell_width, 0),
                             (x * self.cell_width, HEIGHT))
        for x in range(HEIGHT // self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x * self.cell_height),
                             (WIDTH, x * self.cell_height))

    def reset(self):
        self.player.lives = 3
        self.player.current_score = 0

        file = open("highscore.txt")
        highscore = int(file.readline())
        file.close()

        self.player.high_score = highscore
        self.player.grid_pos = Vector2(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0

        for enemy in self.enemies:
            enemy.grid_pos = Vector2(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.coins = []
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(Vector2(xidx, yidx))
        self.state = "playing"

    ''' intro functions '''

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PUSH SPACE BAR', self.screen, [
                       WIDTH // 2, HEIGHT // 2 - 50], FONT_SIZE, (255, 255, 0), FONT, centered=True)
        self.draw_text('1 PLAYER ONLY', self.screen, [
                       WIDTH // 2, HEIGHT // 2 + 50], FONT_SIZE, (0, 255, 255), FONT, centered=True)
        pygame.display.update()

    def menu_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PACMAN', self.screen, [
            WIDTH // 2, HEIGHT // 2 - 200], FONT_SIZE, (0, 255, 255), FONT, centered=True)
        self.draw_text('START', self.screen, [
                       WIDTH // 2, HEIGHT // 2 - 50], FONT_SIZE, (255, 255, 0), FONT, centered=True)
        self.draw_text('CREDIT', self.screen, [
            WIDTH // 2, HEIGHT // 2], FONT_SIZE, (255, 255, 0), FONT, centered=True)
        self.draw_text('QUIT', self.screen, [
            WIDTH // 2, HEIGHT // 2 + 50], FONT_SIZE, (255, 255, 0), FONT, centered=True)
        pygame.display.update()

    def menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if (255 <= pos[0] <= 353) and (270 <= pos[1] <= 295):
                    self.state = 'playing'
                elif (255 <= pos[0] <= 353) and (326 <= pos[1] <= 348):
                    self.state = 'credit'
                elif (255 <= pos[0] <= 353) and (376 <= pos[1] <= 395):
                    sys.exit()

    def credits_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('Authors', self.screen, [
            WIDTH // 2, HEIGHT // 2 - 200], FONT_SIZE, (0, 255, 255), FONT, centered=True)
        self.draw_text('Carlos Martins', self.screen, [
            WIDTH // 2, HEIGHT // 2 - 50], FONT_SIZE, (255, 255, 0), FONT, centered=True)
        self.draw_text('Dayvson Silva', self.screen, [
            WIDTH // 2, HEIGHT // 2], FONT_SIZE, (255, 255, 0), FONT, centered=True)
        self.draw_text('Elikson Tavares', self.screen, [
            WIDTH // 2, HEIGHT // 2 + 50], FONT_SIZE, (255, 255, 0), FONT, centered=True)
        self.draw_text('Fabio Ono', self.screen, [
            WIDTH // 2, HEIGHT // 2 + 100], FONT_SIZE, (255, 255, 0), FONT, centered=True)
        self.draw_text('Gustavo Fadel', self.screen, [
            WIDTH // 2, HEIGHT // 2 + 150], FONT_SIZE, (255, 255, 0), FONT, centered=True)
        self.draw_text('Back', self.screen, [
            80, 30], FONT_SIZE, (255, 255, 0), FONT, centered=True)
        pygame.display.update()

    def credits_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if (45 <= pos[0] <= 120) and (20 <= pos[1] <= 46):
                    self.state = 'menu'

    ''' playing functions '''

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(Vector2(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(Vector2(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(Vector2(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(Vector2(0, 1))

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER // 2, TOP_BOTTOM_BUFFER // 2))
        self.draw_coins()
        self.draw_text('CURRENT SCORE: {}'.format(self.player.current_score),
                       self.screen, [60, 0], 20, (222, 222, 255), FONT)
        self.draw_text('HIGH SCORE: %d' % self.player.high_score, self.screen, [WIDTH // 2 + 60, 0], 20, (222, 222, 255), FONT)
        self.player.draw()

        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            sound = pygame.mixer.Sound('Sounds/death_1.wav')
            sound.play()
            self.state = "game over"
        else:
            self.player.grid_pos = Vector2(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = Vector2(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    def draw_coins(self):
        IMG = pygame.image.load('Sprites/coin.png')
        img_radius = IMG.get_width() / 2

        for coin in self.coins:
            self.screen.blit(IMG, ((int(coin.x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2) - img_radius, 
                                    (int(coin.y * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2) - img_radius))

    ''' game over functions '''

    def game_over_events(self):
        file = open("highscore.txt")
        highscore = int(file.readline())
        file.close()

        if self.player.current_score > highscore:
            highscore = self.player.current_score

        file = open("highscore.txt", "w")
        file.write(str(highscore))
        file.close()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_update(self):
        pass

    def game_over_draw(self):
        self.screen.fill(BLACK)
        quit_text = "Press the ESC button to QUIT"
        again_text = "Press SPACE bar to PLAY AGAIN"
        self.draw_text("GAME OVER", self.screen, [WIDTH // 2, 100],  40, RED, FONT, centered=True)
        self.draw_text(again_text, self.screen, [
                       WIDTH // 2, HEIGHT // 2], 20, (255, 255, 255), FONT, centered=True)
        self.draw_text(quit_text, self.screen, [
                       WIDTH // 2, HEIGHT // 1.5], 20, (255, 255, 255), FONT, centered=True)
        pygame.display.update()
