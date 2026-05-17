from Awale import Awale
from Gui_tkinter import GuiTkinter
from Human import Human
from typing import Optional, Callable, Any


class GameController:
    def __init__(self):
        self.game = Awale()
        self.gui = GuiTkinter(self.game)
        self.player0 = Human("Joueur 0", 0, self.game, self.gui)
        self.player1 = Human("Joueur 1", 1, self.game, self.gui)
        self.game_over = False
        self.current_config = {
            "player0_type": "Humain",
            "player1_type": "Humain",
        }

        self.gui.on_pit_click_callback = self._on_pit_clicked
        self.gui.on_start_game_callback = self._on_start_game
        self.gui.on_replay_callback = self._on_replay
        self.gui.on_back_to_menu_callback = self._on_back_to_menu

    def run_game(self):
        self.gui.show_menu()
        self.gui.run()

    def _on_start_game(self, config: dict) -> None:
        self.current_config = config
        self._new_round()
        self.gui.show_game()
        self.gui.notify("Partie lancee. Joueur 0 commence.")

    def _on_replay(self) -> None:
        self._new_round()
        self.gui.notify("Nouvelle manche. Joueur 0 commence.")

    def _on_back_to_menu(self) -> None:
        self.game_over = False
        self.gui.show_menu()

    def _new_round(self) -> None:
        self.game = Awale()
        self.player0.set_game(self.game)
        self.player1.set_game(self.game)
        self.game_over = False
        self.gui.set_game(self.game)

    def _on_pit_clicked(self, pit: int):
        if self.game_over:
            return

        if not self.game.is_legal_move(pit):
            self.gui.notify("Coup illegal.")
            return

        try:
            captured, game_over = self.game.apply_move(pit)
            self.game_over = game_over
            self.gui.refresh()

            if captured > 0:
                self.gui.notify(f"{captured} graine(s) capturee(s).")
            else:
                self.gui.notify("Coup joue.")

            if game_over:
                self.gui.show_game_over()

        except ValueError as e:
            self.gui.notify(f"Erreur: {e}")