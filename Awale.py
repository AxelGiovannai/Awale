

from ast import Tuple
from typing import Optional


class Awale:
    def __init__(self):
        self.board = [4] * 12
        self.score = [0, 0]
        self.current_player = 0

    def  clone(self) -> 'Awale':

    def get_board(self) -> list[int]:

    def get_score(self) -> Tuple[int, int]:

    def get_current_player(self) -> int:

    def get_legal_moves(self) -> list[int]:

    def is_legal_moves(self, pit: int) -> bool:

    def apply_moves(self, pit: int) -> Tuple[int, bool]:

    def simulate_moves(self, pit: int) -> Awale:

    def is_game_over(self) -> bool:

    def get_winner(self) -> Optional[int]: