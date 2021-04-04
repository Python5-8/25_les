import pygame as pg

BLACK = (0,) * 3
GRAY = (100,) * 3
WHITE = (255,) * 3
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHTGREEN = (0, 200, 200)

CROSS = '#046582'
CIRCLE = '#e4bad4'

class Board:
    def __init__(self, w, h, W, H, left, top, size):
        '''setting parameters and attributes'''
        self.w, self.h = w, h # size of the map
        self.W, self.H = W, H # size ot the win
        self.board = [[0] * w for _ in range(h)]
        self.l = left # leftmost point of the map
        self.t = top # topmost point of the map
        self.size = size # cell size on the map
        self.move = 1 # move order

    def render(self, sc):
        '''render the map'''
        def draw_circle(sc, x, y):
            '''draw circle inside the cell with coordinates x, y'''
            x = self.l + (x + .5) * self.size
            y = self.t + (y + .5) * self.size
            pg.draw.circle(sc, CIRCLE, (x, y), (self.size - 3) // 2, 3)
        def draw_cross(sc, x, y):
            '''draw cross inside the cell with coordinates x, y'''
            x = self.l + x * self.size + 3
            y = self.t + y * self.size + 3
            pg.draw.line(sc, CROSS, (x, y), (x + self.size - 3, y + self.size - 3), 3)
            pg.draw.line(sc, CROSS, (x + self.size - 3, y - 3), (x, y + self.size - 3), 3)

        for y in range(1, self.h + 1):
            pg.draw.line(sc, GRAY,
             (self.l, self.t + y * self.size),
             (self.l + self.size * self.w, self.t + y * self.size), 3)
        for x in range(1, self.w + 1):
            pg.draw.line(sc, GRAY,
             (self.l + x * self.size, self.t),
             (self.l + x * self.size, self.t + self.size * self.h), 3)
        for y in range(self.h):
            for x in range(self.w):
                if self.board[y][x] == 1:                   
                    draw_cross(sc, x, y) 
                elif self.board[y][x] == -1:
                    draw_circle(sc, x, y)

    def get_cells_coords(self, mouse_pos):
        '''get cell's coords (x, y of the cell on the map)'''
        x = (mouse_pos[0] - self.l) // self.size
        y = (mouse_pos[1] - self.t) // self.size
        if 0 <= x <= self.w and 0 <= y <= self.h:
            return x, y 
        else:
            None

    def click(self, mouse_pos):
        cell_coords = self.get_cells_coords(mouse_pos)
        if not self.board[cell_coords[1]][cell_coords[0]]:
            self.board[cell_coords[1]][cell_coords[0]] = self.move
            self.move = -self.move

    def check_end(self, screen):
        '''rendering winning'''
        def is_end():
            '''
            checking whether the end or not
            return (num_1, num_2), where num_1 - kind of winning:
            num_1 == 1 & num_2 == i -> ith column
            num_1 == 2 & num_2 == i-> ith line
            num_1 == 3 -> diags (num_2 == 1 -> main | num_2 == 2 -> secondary)
            if there's no winning returns None
            '''
            check_i_line = lambda x, i: True if x[i][0] == x[i][1] == x[i][2] != 0 else False 
            check_i_col = lambda x, i: True if x[0][i] == x[1][i] == x[2][i] != 0 else False
            check_main_diag = lambda x: True if x[0][0] == x[1][1] == x[2][2] != 0 else False 
            check_secondary_diag = lambda x: True if x[0][2] == x[1][1] == x[2][0] != 0 else False

            for i in range(3):
                if check_i_col(self.board, i):
                    return 1, i
                if check_i_line(self.board, i):
                    return 2, i
            if check_main_diag(self.board):
                return 3, 1 
            if check_secondary_diag(self.board):
                return 3, 2 
            return None
        
        is_end = is_end()
        shift = self.W // 10
        if is_end is not None:
            if is_end[0] == 1:
                x0, y0 = self.l + (is_end[1] + .5) * self.size, self.t + shift
                x1, y1 = self.l + (is_end[1] + .5) * self.size, self.t + self.size * self.h - shift
            elif is_end[0] == 2:
                x0, y0 = self.l + shift, self.t + (is_end[1] + .5) * self.size
                x1, y1 = self.l + self.w * self.size - shift, self.t + (is_end[1] + .5) * self.size
            elif is_end[0] == 3:
                if is_end[1] == 1:
                    x0, y0 = self.l + shift, self.t + shift
                    x1, y1 = self.l + self.w * self.size - shift, self.t + self.h * self.size - shift
                else:
                    x0, y0 = self.l + self.w * self.size - shift, self.t + shift
                    x1, y1 = self.l + shift, self.t + self.h * self.size - shift
            pg.draw.line(screen, RED, (x0, y0), (x1, y1), 10)
            pg.display.update()
            pg.time.delay(3000)
            return True
        else:
            return False
def test():
    print(__name__)

if __name__ == '__main__':
    pg.init()
    size = W, H = 600, 600
    screen = pg.display.set_mode(size)
    board = Board(3, 3, W, H, 0, 0, 200)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
                
            if event.type == pg.MOUSEBUTTONDOWN:
                board.click(event.pos)

        screen.fill(WHITE)
        board.render(screen)
        pg.display.update()

        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            pg.quit()
            exit()

        if board.check_end(screen):
            pg.quit()
            exit()

    
            