"""
Класс GameBackend управляет логикой игры Судоку, включая генерацию сетки, проверку ходов и обработку подсказок.

Этот класс отвечает за генерацию судоку, проверку правильности ввода пользователя, 
отслеживание состояния игры и предоставление подсказок.

Attributes:
    size (int): Размер сетки Судоку (например, 4 или 9).
    difficulty (str): Уровень сложности игры (например, 'Легкий' или 'Сложный').
    sudoku_generator (SudokuGenerator): Объект генератора Судоку для создания сетки и её решения.
    sudoku_grid (list[list[int]]): Игровая сетка Судоку с пустыми ячейками.
    user_grid (list[list[int]]): Копия сетки, в которую пользователь вводит числа.
    hint_count (int): Счётчик использованных подсказок (максимум 3 подсказки).

Methods:
    is_valid_move(row: int, col: int, num: int) -> bool:
        Проверяет, можно ли вставить указанное число в заданную ячейку.
    
    is_game_complete() -> bool:
        Проверяет, завершил ли пользователь игру, заполнив все ячейки корректно.
    
    get_hint() -> tuple[int, int, int] | None:
        Возвращает подсказку для случайной пустой ячейки, если доступны подсказки.
"""
from sudoku_generator import SudokuGenerator
import random

class GameBackend:
    """Логика игры Судоку."""
    def __init__(self, difficulty, size):
        """
        Инициализирует объект GameBackend и создаёт игровую сетку Судоку.
        """
        self.size = int(size.split('x')[0])
        self.difficulty = difficulty
        self.sudoku_generator = SudokuGenerator(self.size)
        self.sudoku_grid = self.sudoku_generator.generate(difficulty)
        self.user_grid = [row[:] for row in self.sudoku_grid]  # Копия для пользовательского ввода
        self.hint_count = 0  # Счётчик использованных подсказок

    def is_valid_move(self, row, col, num):
        """
        Проверяет, можно ли вставить число в указанную ячейку.

        Args:
            row (int): Номер строки ячейки.
            col (int): Номер столбца ячейки.
            num (int): Число, которое пользователь хочет вставить.

        Returns:
            bool: True, если число можно вставить в ячейку, иначе False.
        """ 
        # Проверка по строке
        if num in (self.user_grid[row][c] for c in range(self.size) if c != col):
            return False
        
        # Проверка по столбцу
        if num in (self.user_grid[r][col] for r in range(self.size) if r != row):
            return False

        # Определение размера региона (2x2 для 4x4 или 3x3 для 9x9)
        region_size = int(self.size ** 0.5)
        start_row = (row // region_size) * region_size
        start_col = (col // region_size) * region_size


        # Проверка региона (квадрата) на дублирующиеся числа
        for i in range(region_size):
            for j in range(region_size):
                r, c = start_row + i, start_col + j
                if (r, c) != (row, col) and self.user_grid[r][c] == num:
                    return False

        return True

    def is_game_complete(self):
        """
        Проверяет, заполнены ли все ячейки и соответствует ли пользовательская сетка решённой сетке.

        Returns:
            bool: True, если все ячейки заполнены правильно, иначе False.
        """ 
        for row in range(self.size):
            for col in range(self.size):
                if self.user_grid[row][col] == 0:  # Если есть хотя бы одна пустая ячейка
                    return False
                if self.user_grid[row][col] != self.sudoku_generator.solved_grid[row][col]:  # Если хоть одна ячейка не совпадает
                    return False
        return True

    def get_hint(self):
        """
        Предоставляет подсказку, если подсказки ещё доступны и есть пустые ячейки.

        Подсказка ищет случайную пустую ячейку и заполняет её правильным значением.
        Подсказки ограничены количеством (не более 3 за игру).

        Returns:
            tuple[int, int, int] | None: 
                Кортеж из координат (row, col) и числа value, вставленного в ячейку.
                Возвращает None, если подсказки закончились или пустых ячеек нет.
        """
        if self.hint_count >= 3:
            return None  # Подсказки закончились
        
        # Теперь ищем пустые ячейки в пользовательской сетке (не в sudoku_grid)
        empty_cells = [(row, col) for row in range(self.size) for col in range(self.size) if self.user_grid[row][col] == 0]
        
        if empty_cells:
            row, col = random.choice(empty_cells)  # Случайно выбираем пустую клетку
            value = self.sudoku_generator.solved_grid[row][col]  # Получаем правильное значение из решенной сетки
            self.sudoku_grid[row][col] = value  # Обновляем оригинальную сетку
            self.user_grid[row][col] = value  # Обновляем пользовательскую сетку
            self.hint_count += 1  # Увеличиваем количество использованных подсказок
            return row, col, value  # Возвращаем координаты и значение для интерфейса (GameFrontend)
        
        return None
