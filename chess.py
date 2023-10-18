from typing import List, Optional


class Figure:
    def __init__(self, color, fig_name='Pawn'):
        self.fig_name = fig_name
        self.fig_color = color
        self.image = f'static/img/Chess Pieces/{self.fig_color}{self.fig_name}.png'
        self.x = 0
        self.y = 0

    def __copy__(self):
        new_instance = self.__class__(self.fig_color)
        new_instance.fig_name = self.fig_name
        new_instance.image = self.image
        new_instance.x = self.x
        new_instance.y = self.y
        return new_instance

    def my_copy(self):
        return self.__copy__()

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def attacks(self, x, y):
        return True

    def moves(self, x, y):
        return True


class Pawn(Figure):
    def __init__(self, color):
        super().__init__(color, 'Pawn')

    def set_pos(self, x, y):
        super().set_pos(x, y)

    def attacks(self, x, y):
        if self.fig_color == 'White':
            return self.y == y - 1 and abs(self.x - x) == 1
        else:
            return self.y == y + 1 and abs(self.x - x) == 1

    def moves(self, x, y):
        if self.x != x:
            return False
        if self.fig_color == 'White':
            if self.y == y - 1 or (self.y == 1 and y == 3):
                return True
            return False
        else:
            if self.y == y + 1 or (self.y == 6 and y == 4):
                return True
            return False


class Knight(Figure):
    def __init__(self, color):
        super().__init__(color, 'Knight')

    def attacks(self, x, y):
        delta_x = abs(self.x - x)
        delta_y = abs(self.y - y)
        if (delta_x == 1 and delta_y == 2) or (delta_y == 1 and delta_x == 2):
            return True
        return False

    def moves(self, x, y):
        return self.attacks(x, y)


class Bishop(Figure):
    def __init__(self, color):
        super().__init__(color, 'Bishop')

    def attacks(self, x, y):
        delta_x = abs(self.x - x)
        delta_y = abs(self.y - y)
        if delta_x == delta_y:
            return True
        return False

    def moves(self, x, y):
        return self.attacks(x, y)


class Rook(Figure):
    def __init__(self, color):
        super().__init__(color, 'Rook')

    def attacks(self, x, y):
        delta_x = abs(self.x - x)
        delta_y = abs(self.y - y)
        if delta_x == 0 or delta_y == 0:
            if delta_x == delta_y:
                return False
            return True
        return False

    def moves(self, x, y):
        return self.attacks(x, y)


class Queen(Figure):
    def __init__(self, color):
        super().__init__(color, 'Queen')

    def attacks(self, x, y):
        delta_x = abs(self.x - x)
        delta_y = abs(self.y - y)
        if delta_x == delta_y:
            if delta_x == 0:
                return False
            return True
        if delta_x == 0 or delta_y == 0:
            return True
        return False

    def moves(self, x, y):
        return self.attacks(x, y)


class King(Figure):
    def __init__(self, color):
        super().__init__(color, 'King')

    def attacks(self, x, y):
        delta_x = abs(self.x - x)
        delta_y = abs(self.y - y)
        if delta_x == 0 and delta_y == 0:
            return False
        if delta_x <= 1 and delta_y <= 1:
            return True
        return False

    def moves(self, x, y):
        return self.attacks(x, y)


class Board:
    def __init__(self):
        self.board: List[List[Optional[Figure]]] = [
            [None for _ in range(8)] for _ in range(8)
        ]

    def start_game(self):
        for x in range(0, 8):
            self.board[x][1] = Pawn('White')
            self.board[x][6] = Pawn('Black')
            self.board[x][1].set_pos(x, 1)
            self.board[x][6].set_pos(x, 6)
        for x in range(0, 8):
            if x == 0 or x == 7:
                self.board[x][0] = Rook('White')
                self.board[x][7] = Rook('Black')
            elif x == 1 or x == 6:
                self.board[x][0] = Knight('White')
                self.board[x][7] = Knight('Black')
            elif x == 2 or x == 5:
                self.board[x][0] = Bishop('White')
                self.board[x][7] = Bishop('Black')
            elif x == 3:
                self.board[x][0] = Queen('White')
                self.board[x][7] = Queen('Black')
            elif x == 4:
                self.board[x][0] = King('White')
                self.board[x][7] = King('Black')
            self.board[x][0].set_pos(x, 0)
            self.board[x][7].set_pos(x, 7)

    def get_fig(self, i, j):
        if i < 0 or i >= 8 or j < 0 or j >= 8:
            return None
        return self.board[i][j]

    def set_fig(self, i, j, fig):
        if fig is not None:
            self.board[i][j] = fig.my_copy()
        else:
            self.board[i][j] = None


class Chess:
    fig_names = {'Pawn': '', 'Knight': 'N', 'Bishop': 'B', 'Rook': 'R', 'Queen': 'Q', 'King': 'K'}

    def __init__(self):
        self.board = Board()
        self.turn = 'White'
        self.game_over = False
        self.winner = ''
        self.white_king_moved = False
        self.black_king_moved = False

    def move_possible(self, fig: Figure, x, y, f: bool):
        if fig is None:
            return False
        if fig.fig_color != self.turn and not f:
            return False
        f2 = self.board.get_fig(x, y) is None or self.board.get_fig(x, y).fig_color != fig.fig_color
        if not f2:
            return False
        if x < 0 or x >= 8 or y < 0 or y >= 8:
            return False
        if fig.fig_name == 'Pawn':
            if f:
                return fig.attacks(x, y)
            if fig.attacks(x, y) and self.board.get_fig(x, y) is not None:
                return True
            if not fig.moves(x, y):
                return False
            if self.board.get_fig(x, y) is None:
                if fig.fig_color == 'White':
                    if self.board.get_fig(x, fig.y + 1) is None:
                        return True
                    return False
                else:
                    if self.board.get_fig(x, fig.y-1) is None:
                        return True
                    return False
            return False

        if not fig.moves(x, y):
            return False
        if fig.fig_name == 'Knight':
            return True
        if fig.fig_name == 'King':
            return True

        delta_x = 0
        delta_y = 0
        if x - fig.x > 0:
            delta_x = 1
        elif x - fig.x < 0:
            delta_x = -1
        if y - fig.y > 0:
            delta_y = 1
        elif y - fig.y < 0:
            delta_y = -1
        cur_x = fig.x + delta_x
        cur_y = fig.y + delta_y
        while cur_x != x or cur_y != y:
            if self.board.get_fig(cur_x, cur_y) is not None:
                return False
            cur_x += delta_x
            cur_y += delta_y
        return True

    def is_attacked(self, x, y, color):
        for x2 in range(0, 8):
            for y2 in range(0, 8):
                fig = self.board.get_fig(x2, y2)
                if fig is not None and fig.fig_color != color:
                    if self.move_possible(fig, x, y, True):
                        # print(f"{fig.fig_name} {x2} {y2} {fig.x} {fig.y}")
                        return True
        return False

    def make_move(self, fig: Figure, x, y):
        if self.move_possible(fig, x, y, False):
            self.board.set_fig(fig.x, fig.y, None)
            prev_fig = self.board.get_fig(x, y)
            if prev_fig is not None:
                prev_fig = prev_fig.my_copy()
            self.board.set_fig(x, y, fig)
            if not self.is_check():
                opposite_color = 'White'
                if self.turn == 'White':
                    opposite_color = 'Black'
                self.board.get_fig(x, y).set_pos(x, y)
                if self.is_mate(opposite_color):
                    print(777)
                    self.game_over = True
                    self.winner = self.turn
                self.turn = opposite_color
                if fig.fig_name == 'King':
                    if fig.fig_color == 'White':
                        self.white_king_moved = True
                    else:
                        self.black_king_moved = True
                return True
            self.board.set_fig(fig.x, fig.y, fig)
            self.board.set_fig(x, y, prev_fig)
            return False
        return False

    def get_king_coord(self, color):
        for x in range(0, 8):
            for y in range(0, 8):
                fig = self.board.get_fig(x, y)
                if fig is not None and fig.fig_name == 'King' and fig.fig_color == color:
                    return x, y
        return 0, 0

    def is_check(self):
        x, y = self.get_king_coord(self.turn)
        return self.is_attacked(x, y, self.turn)

    def is_mate(self, color):
        # return False
        x, y = self.get_king_coord(color)
        if not self.is_attacked(x, y, color):
            return False
        king = self.board.get_fig(x, y)
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                cur_x = x + dx
                cur_y = y + dy
                # if color == 'Black':
                #     print(f"{color}  {self.get_king_coord(color)}")
                if cur_x < 0 or cur_x >= 8 or cur_y < 0 or cur_y >= 8:
                    continue
                prev_fig = self.board.get_fig(cur_x, cur_y)
                if prev_fig is not None and prev_fig.fig_color == color:
                    continue
                if prev_fig is not None:
                    prev_fig = prev_fig.my_copy()
                self.board.set_fig(x, y, None)
                self.board.set_fig(cur_x, cur_y, king.my_copy())
                if not self.is_attacked(cur_x, cur_y, color):
                    self.board.set_fig(cur_x, cur_y, prev_fig)
                    self.board.set_fig(x, y, king.my_copy())
                    return False
                self.board.set_fig(cur_x, cur_y, prev_fig)
                self.board.set_fig(x, y, king.my_copy())
        return True
