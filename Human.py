from typing import Any, Callable, Optional
from threading import Event
from Awale import Awale


class Human:
    def __init__(self, name: str, player_id: int, game: Awale, gui: Optional[Any] = None):
        self.name = name
        self.player_id = player_id
        self.game = game
        self.gui = gui
        self.selected_move = None
        self.move_event = None

    def choose_move_blocking(self, prompt: Optional[str] = None) -> int:
        if self.gui is not None:
            self.selected_move = None
            self.move_event = Event()

            if prompt is not None:
                self.notify(prompt)
            else:
                self.notify(f"{self.name}, choisissez un coup.")

            while self.selected_move is None:
                self.move_event.wait()

            return self.selected_move

        while True:
            if prompt is not None:
                print(prompt)
            print(f"Joueur {self.name}, coups légaux : {self.game.get_legal_moves()}")
            try:
                pit = int(input("Entrez votre coup : "))
            except ValueError:
                print("Entrée invalide.")
                continue

            if self._validate_and_store(pit):
                return pit

            print("Coup illégal.")

    def choose_move_async(self, callback: Callable[[int], None]) -> None:
        if self.gui is not None:
            self.selected_move = None
            self.move_event = None
            self._async_callback = callback
            self.notify(f"{self.name}, choisissez un coup.")
        else:
            pit = self.choose_move_blocking()
            callback(pit)

    def on_gui_click(self, x: int, y: int) -> None:
        pit = self._map_coords_to_pit(x, y)
        if pit is None:
            return

        if self._validate_and_store(pit):
            if self.move_event is not None:
                self.move_event.set()
            if hasattr(self, "_async_callback"):
                self._async_callback(pit)

    def set_game(self, game: Awale) -> None:
        self.game = game

    def notify(self, message: str) -> None:
        if self.gui is not None and hasattr(self.gui, "notify"):
            self.gui.notify(message)
        else:
            print(message)

    def _map_coords_to_pit(self, x: int, y: int) -> Optional[int]:
        if self.gui is None:
            return None

        if hasattr(self.gui, "map_coords_to_pit"):
            return self.gui.map_coords_to_pit(x, y)

        return None

    def _validate_and_store(self, pit: int) -> bool:
        if self.game.is_legal_move(pit):
            self.selected_move = pit
            return True
        return False

    

    
