import unittest
from unittest.mock import MagicMock, patch
from menu_backend import MenuBackend
from game_backend import GameBackend
from sudoku_generator import SudokuGenerator

class TestMenuBackend(unittest.TestCase):
    """Тесты для класса MenuBackend, который управляет настройками игры"""
    def setUp(self):
        self.backend = MenuBackend()

    def test_default_settings(self):
        """Проверяет, что настройка по умолчанию правильная"""
        self.assertEqual(self.backend.difficulty, 'Легкий')
        self.assertEqual(self.backend.size, '9x9')

    def test_set_game_settings(self):
        """Тестирует изменение настроек игры"""
        self.backend.set_game_settings('Сложный', '4x4')
        self.assertEqual(self.backend.difficulty, 'Сложный')
        self.assertEqual(self.backend.size, '4x4')

    @patch('game_frontend.GameFrontend')
    def test_start_game(self, mock_game_frontend):
        self.backend.start_game()
        mock_game_frontend('Легкий', '9x9')

class TestGameBackend(unittest.TestCase):
    """Проверяет, что при запуске игры создается с правильными параметрами"""
    def setUp(self):
        self.backend = GameBackend('Легкий', '4x4')

    def test_is_valid_move(self):
        """Проверяет, правильно ли даёт допустимые ходы"""
        self.backend.user_grid = [
            [1, 0, 0, 0],
            [0, 2, 0, 0],
            [0, 0, 3, 0],
            [0, 0, 0, 4],
        ]
        self.assertTrue(self.backend.is_valid_move(0, 1, 4))
        self.assertFalse(self.backend.is_valid_move(0, 1, 1))

    def test_is_game_complete(self):
        """Проверяет метод завершения игры"""
        self.backend.user_grid = self.backend.sudoku_generator.solved_grid
        self.assertTrue(self.backend.is_game_complete())
        self.backend.user_grid[0][0] = 0
        self.assertFalse(self.backend.is_game_complete())

    def test_get_hint(self):
        """Тестирует метод get_hint, который даёт подсказку"""
        self.backend.hint_count = 0
        hint = self.backend.get_hint()
        self.assertIsNotNone(hint)
        self.assertEqual(self.backend.hint_count, 1)

class TestSudokuGenerator(unittest.TestCase):
    def setUp(self):
        """Создаёт экземпляр MenuBackend для использования в тестах"""
        self.generator = SudokuGenerator(4)

    def test_generate(self):
        """Тестирует метод generate для генерации судоку"""
        grid = self.generator.generate('Легкий')
        self.assertEqual(len(grid), 4)
        self.assertEqual(len(grid[0]), 4)

    def test_is_valid_placement(self):
        """Проверяет, правильно ли метод _is_valid_placement определяет допустимость размещения числа в сетке"""
        self.generator.grid = [
            [1, 0, 0, 0],
            [0, 2, 0, 0],
            [0, 0, 3, 0],
            [0, 0, 0, 4],
        ]
        self.assertTrue(self.generator._is_valid_placement(0, 1, 4))
        self.assertFalse(self.generator._is_valid_placement(0, 1, 1))

    def test_solve(self):
        """Тестирует метод _solve, который решает судоку и проверяет, что в сетке нет нулей"""
        self.generator.grid = [
            [1, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        self.assertTrue(self.generator._solve())
        self.assertNotIn(0, [num for row in self.generator.grid for num in row])

if __name__ == '__main__':
    unittest.main()