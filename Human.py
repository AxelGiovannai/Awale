

from typing import Any, Callable, Optional
from Awale import Awale


class Human:
    def __init__(self, name : str, player_id : int, game : Awale, gui : Optional[Any] = None):
        self.name = name
        self.player_id = player_id
        self.game = game
        self.gui = gui
        self.selected_move = None
        self.move_event = None

    def choose_move_blocking(self, prompt: Optional[str] = None) -> int:

    def choose_move_async(self, callback: Callable[[int], None]) -> None:

    def choose_move_async(self, callback: Callable[[int], None]) -> None:

    def on_gui_click(self, x: int, y: int) -> None:

    def set_game(self, game: Awale) -> None:

    def notify(self, message: str) -> None:

    def _map_coords_to_pit(self, x: int, y: int) -> Optional[int]:

    def _validate_and_store(self, pit: int) -> bool:

    

    
