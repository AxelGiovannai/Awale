import random
from typing import Any, Optional
from Awale import Awale


class StupidBot:
    def __init__(self, name: str, player_id: int, game: Awale, gui: Optional[Any] = None):
        self.name = name
        self.player_id = player_id
        self.game = game
        self.gui = gui

    def choose_move(self) -> int:
        legal_moves = self.game.get_legal_moves()
        if not legal_moves:
            raise ValueError(f"{self.name} n'a pas de coup légal disponible.")
        return random.choice(legal_moves)

    def set_game(self, game: Awale) -> None:
        self.game = game

    def notify(self, message: str) -> None:
        if self.gui is not None and hasattr(self.gui, "notify"):
            self.gui.notify(message)
        else:
            print(message)