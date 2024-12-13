"""
Класс MenuBackend обеспечивает логику работы меню и управление настройками игры.

Этот класс хранит текущие настройки игры, такие как уровень сложности и размер поля, 
и предоставляет методы для их изменения и запуска игры.

Attributes:
    difficulty (str): Уровень сложности игры (по умолчанию 'Легкий').
    size (str): Размер игрового поля (по умолчанию '9x9').

Methods:
    set_game_settings(difficulty: str, size: str) -> None:
        Устанавливает выбранные настройки сложности и размера поля.
    
    start_game() -> None:
        Запускает игру с текущими настройками, создавая экземпляр класса GameFrontend.
"""
import game_frontend

class MenuBackend:
    """Логика работы меню и управление настройками игры."""
    
    def __init__(self):
        self.difficulty = 'Легкий'
        self.size = '9x9'

    def set_game_settings(self, difficulty, size):
        self.difficulty = difficulty
        self.size = size

    def start_game(self):
        game = game_frontend.GameFrontend(self.difficulty, self.size)
        game.run()