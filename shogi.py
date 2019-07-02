# TODO:
#       Make move rules for promoted pieces
#       Check for jumping over other pieces
#       Victory conditions
#       Ban moving under check
#       Implement all Komadai rules


import pygame

pygame.init()

win = pygame.display.set_mode((1000, 1000))

pygame.display.set_caption("Shogi 2 Players")

board = []
komadai_white = []
komadai_black = []


class Piece:
    def __init__(self, name, side, imgsrc, x, y):
        self.name = name
        self.x = x
        self.y = y
        board[x][y].player = self
        self.side = side
        self.img = pygame.image.load(imgsrc)
        self.promotable = False

    def promote(self):
        if self.promotable:
            x = self.name
            self.name = "+"
            self.name += x


class Square:
    def __init__(self, x, y):
        self.bg_colour = (255, 211, 155)
        self.click_colour = (139, 62, 47)
        self.pos_x = x
        self.pos_y = y
        self.print_x = (x+1)*60
        self.print_y = (y+1)*60
        self.width = 60
        self.height = 60
        self.player = None
        self.clicked = False

    def is_over(self, mouse_pos):
        if mouse_pos[0] in range(self.print_x, (self.print_x + self.width)) and mouse_pos[1] in range(self.print_y, (self.print_y + self.height)):
            return True
        return False

    def draw(self):
        if self.clicked:
            pygame.draw.rect(win, (0, 0, 0), (self.print_x, self.print_y, self.width, self.height))
            pygame.draw.rect(win, self.click_colour, (self.print_x+2, self.print_y+2, self.width+2, self.height+2))
        else:
            pygame.draw.rect(win, (0, 0, 0), (self.print_x, self.print_y, self.width, self.height))
            pygame.draw.rect(win, self.bg_colour, (self.print_x+2, self.print_y+2, self.width, self.height))
        if self.player is not None:
            win.blit(self.player.img, (self.print_x + (self.width/2 - self.player.img.get_width()/2), self.print_y + (self.height/2 - self.player.img.get_height()/2)))


for i in range(0, 9):
    ele = []
    for j in range(0, 9):
        ele.append(Square(i, j))
    board.append(ele)


for i in range(0, 9):
    white_pawn = Piece(name='P', side='WHITE', imgsrc='piece-pics/white_pawn.png', x=i, y=2)

white_rook = Piece('R', 'WHITE', 'piece-pics/white_rook.png', 1, 1)
white_bishop = Piece('B', 'WHITE', 'piece-pics/white_bishop.png', 7, 1)
white_lance1 = Piece('L', 'WHITE', 'piece-pics/white_lance.png', 0, 0)
white_lance2 = Piece('L', 'WHITE', 'piece-pics/white_lance.png', 8, 0)
white_knight1 = Piece('N', 'WHITE', 'piece-pics/white_knight.png', 1, 0)
white_knight2 = Piece('N', 'WHITE', 'piece-pics/white_knight.png', 7, 0)
white_silver1 = Piece('S', 'WHITE', 'piece-pics/white_silver.png', 2, 0)
white_silver2 = Piece('S', 'WHITE', 'piece-pics/white_silver.png', 6, 0)
white_gold1 = Piece('G', 'WHITE', 'piece-pics/white_gold.png', 3, 0)
white_gold2 = Piece('G', 'WHITE', 'piece-pics/white_gold.png', 5, 0)
white_king = Piece('K', 'WHITE', 'piece-pics/white_king.png', 4, 0)

for i in range(0, 9):
    black_pawn = Piece('P', 'BLACK', 'piece-pics/black_pawn.png', i, 6)

black_rook = Piece('R', 'BLACK', 'piece-pics/black_rook.png', 7, 7)
black_bishop = Piece('B', 'BLACK', 'piece-pics/black_bishop.png', 1, 7)
black_lance1 = Piece('L', 'BLACK', 'piece-pics/black_lance.png', 0, 8)
black_lance2 = Piece('L', 'BLACK', 'piece-pics/black_lance.png', 8, 8)
black_knight1 = Piece('N', 'BLACK', 'piece-pics/black_knight.png', 1, 8)
black_knight2 = Piece('N', 'BLACK', 'piece-pics/black_knight.png', 7, 8)
black_silver1 = Piece('S', 'BLACK', 'piece-pics/black_silver.png', 2, 8)
black_silver2 = Piece('S', 'BLACK', 'piece-pics/black_silver.png', 6, 8)
black_gold1 = Piece('G', 'BLACK', 'piece-pics/black_gold.png', 3, 8)
black_gold2 = Piece('G', 'BLACK', 'piece-pics/black_gold.png', 5, 8)
black_king = Piece('K', 'BLACK', 'piece-pics/black_king.png', 4, 8)


def move_rule_check(p1, p2):
    # Check for jumping over other pieces.
    # Set moving rules for promoted pieces
    if p1.player.side == 'WHITE':
        if p1.player.name == 'P':
            if p2.pos_y - p1.pos_y == 1 and p1.pos_x == p2.pos_x:
                return True
            else:
                return False
        if p1.player.name == 'L':
            if p2.pos_x == p1.pos_x:
                return True
            else:
                return False
        if p1.player.name == 'N':
            if abs(p1.pos_x - p2.pos_x) == 1 and p2.pos_y - p1.pos_y == 2:
                return True
            else:
                return False
        if p1.player.name == 'S':
            if abs(p1.pos_x - p2.pos_x) == 1:
                if abs(p1.pos_y - p2.pos_y) == 1:
                    return True
            if p2.pos_y - p1.pos_y == 1 and p1.pos_x == p2.pos_x:
                return True
            return False
        if p1.player.name == 'G':
            if abs(p2.pos_x - p1.pos_x) == 1:
                if p2.pos_y - p1.pos_y == 1:
                    return True
            if abs(p1.pos_x - p2.pos_x) == 1:
                if p1.pos_y == p2.pos_y:
                    return True
            if abs(p1.pos_y - p2.pos_y) == 1:
                if p1.pos_x == p2.pos_x:
                    return True
            return False
        if p1.player.name == 'K':
            if abs(p1.pos_x - p2.pos_x) == 1 and p1.pos_y == p2.pos_y:
                return True
            if abs(p1.pos_y - p2.pos_y) == 1 and p2.pos_x == p2.pos_x:
                return True
            if abs(p1.pos_y - p2.pos_y) == 1 and abs(p1.pos_x - p2.pos_x) == 1:
                return True
            return False
    else:
        if p1.player.name == 'P':
            if p1.pos_y - p2.pos_y == 1 and p1.pos_x == p2.pos_x:
                return True
            else:
                return False
        if p1.player.name == 'L':
            if p2.pos_x == p1.pos_x:
                return True
            else:
                return False
        if p1.player.name == 'N':
            if abs(p1.pos_x - p2.pos_x) == 1 and p1.pos_y - p2.pos_y == 2:
                return True
            else:
                return False
        if p1.player.name == 'S':
            if abs(p1.pos_x - p2.pos_x) == 1:
                if abs(p1.pos_y - p2.pos_y) == 1:
                    return True
            if p1.pos_y - p2.pos_y == 1 and p1.pos_x == p2.pos_x:
                return True
            return False
        if p1.player.name == 'G':
            if abs(p1.pos_x - p2.pos_x) == 1:
                if p1.pos_y - p2.pos_y == 1:
                    return True
            if abs(p1.pos_x - p2.pos_x) == 1:
                if p1.pos_y == p2.pos_y:
                    return True
            if abs(p1.pos_y - p2.pos_y) == 1:
                if p1.pos_x == p2.pos_x:
                    return True
            return False
        if p1.player.name == 'K':
            if abs(p1.pos_x - p2.pos_x) == 1 and p1.pos_y == p2.pos_y:
                return True
            if abs(p1.pos_y - p2.pos_y) == 1 and p2.pos_x == p2.pos_x:
                return True
            if abs(p1.pos_y - p2.pos_y) == 1 and abs(p1.pos_x - p2.pos_x) == 1:
                return True
            return False


def print_board():
    for row in board:
        for sq in row:
            sq.draw()


def change_turn():
    for row in board:
        for sq in row:
            if sq.clicked:
                sq.clicked = False


def refresh():
    win.fill((255, 255, 255))
    print_board()


run = True

black_turn = True

while run:
    refresh()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            for row in board:
                for s in row:
                    if s.is_over(pygame.mouse.get_pos()) and s.clicked:
                        s.clicked = False
                        break
                    elif s.is_over(pygame.mouse.get_pos()) and not s.clicked:
                        s.clicked = True
                        for r2 in board:
                            for s2 in r2:
                                if s2.clicked and s2 is not s:
                                    s2.clicked = False
                                    if s2.player is not None:
                                        if ((s2.player.side == 'BLACK' and black_turn) or (s2.player.side == 'WHITE' and not black_turn)) and ((s.player is None) or (s.player.side is not s2.player.side)):
                                            if move_rule_check(s2, s):
                                                p = s2.player
                                                s2.player = None
                                                if s.player is not None:
                                                    if black_turn:
                                                        komadai_black.append(s.player)
                                                    else:
                                                        komadai_white.append(s.player)
                                                s.player = p
                                                s.clicked = False
                                                black_turn = not black_turn
                                                break
