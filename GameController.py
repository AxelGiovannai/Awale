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
        
        self.gui.on_pit_click_callback = self._on_pit_clicked

    def run_game(self):
        self.gui.notify("Partie lancée. Joueur 0 commence.")
        self.gui.run()

    def _on_pit_clicked(self, pit: int):
        if self.game_over:
            return

        if not self.game.is_legal_move(pit):
            self.gui.notify("Coup illégal.")
            return

        try:
            captured, game_over = self.game.apply_move(pit)
            self.game_over = game_over
            self.gui.refresh()

            if captured > 0:
                self.gui.notify(f"{captured} graine(s) capturée(s).")
            else:
                self.gui.notify("Coup joué.")

            if game_over:
                winner = self.game.get_winner()
                score0, score1 = self.game.get_score()
                if winner is None:
                    self.gui.notify(f"Fin de partie: égalité ({score0} - {score1}).")
                else:
                    self.gui.notify(f"Fin de partie: Joueur {winner} gagne ({score0} - {score1}).")

        except ValueError as e:
            self.gui.notify(f"Erreur: {e}")