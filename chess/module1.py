WHITE = 1
BLACK = 2


def correct_coords(row, col):
    """Функция проверяет, что координаты (row, col) лежат
    внутри доски"""
    return 0 <= row < 8 and 0 <= col < 8


def opponent(color): # Удобная функция для вычисления цвета противника
    if color == WHITE:
        return BLACK
    return WHITE


def print_board(board): # Распечатать доску в текстовом виде
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(col, end='    ')
    print()
 

def main():
    # Создаём шахматную доску
    board = Board()

    # Цикл ввода команд игроков
    while True:

        # Выводим положение фигур на доске
        print_board(board)

        # Подсказка по командам
        print('Команды:')
        print('    exit                               -- выход')
        print('    move <row> <col> <row1> <col1>     -- ход из клетки (row, col)')
        print('                                          в клетку (row1, col1)')

        # Выводим приглашение игроку нужного цвета
        if board.current_player_color() == WHITE:
            print('Ход белых:')
        else:
            print('Ход черных:')
        command = input()

        if command == 'exit':
            break
        if command == '':
            continue
        move_type, row, col, row1, col1 = command.split()
        row, col, row1, col1 = int(row), int(col), int(row1), int(col1)

        if board.move_piece(row, col, row1, col1):
            print('Ход успешен')
        else:
            print('Координаты некорректы! Попробуйте другой ход!')


class Chessman:
    """Класс, являющийся базой для всех шахматных фигур"""

    def __init__(self, row, col, color):
        self.set_position(row, col)
        self.color = color

    def get_color(self):
        """Функция, возвращающая цвет фигуры"""
        return self.color

    def set_position(self, row, col):
        """Функция, устанавливающая фигуру на заданную позицию"""
        self.row = row
        self.col = col


class Board:
    pass


class Pawn(Chessman):
    pass


class Rook(Chessman):
    pass


class Queen(Chessman):
    pass


class Bishop(Chessman):
    pass


class Knight(Chessman):
    pass


class King(Chessman):
    pass


if __name__ == "__main__":
    main()
