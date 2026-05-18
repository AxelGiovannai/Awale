from Awale import Awale
from Gui_tkinter import GuiTkinter
from Human import Human
from MinMax import MinMaxBot
from StupidBot import StupidBot
from typing import Optional, Callable, Any
from MCTS import MCTS


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
        self.player0 = self._create_player("Joueur 0", 0, config["player0"])
        self.player1 = self._create_player("Joueur 1", 1, config["player1"])
        self._new_round()
        self.gui.show_game()
        self.gui.notify("Partie lancee. Joueur 0 commence.")
        self._play_bot_turn_if_needed()

    def _on_replay(self) -> None:
        self._new_round()
        self.gui.notify("Nouvelle manche. Joueur 0 commence.")
        self._play_bot_turn_if_needed()

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

        current_player = self.game.get_current_player()
        current_bot = self.player0 if current_player == 0 else self.player1

        if not isinstance(current_bot, Human):
            self.gui.notify("C'est au tour du bot.")
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
            else:
                self._play_bot_turn_if_needed()

        except ValueError as e:
            self.gui.notify(f"Erreur: {e}")

    def _play_bot_turn_if_needed(self) -> None:
        if self.game_over:
            return

        current_player = self.game.get_current_player()
        current_bot = self.player0 if current_player == 0 else self.player1

        if isinstance(current_bot, Human):
            return

        self.gui.root.after(500, self._execute_bot_move)

    def _execute_bot_move(self) -> None:
        if self.game_over:
            return

        current_player = self.game.get_current_player()
        current_bot = self.player0 if current_player == 0 else self.player1

        try:
            pit = current_bot.choose_move()
            self.gui.notify(f"{current_bot.name} joue le coup {pit}.")

            captured, game_over = self.game.apply_move(pit)
            self.game_over = game_over
            self.gui.refresh()

            if captured > 0:
                self.gui.notify(f"{captured} graine(s) capturee(s).")
            else:
                self.gui.notify("Coup joue.")

            if game_over:
                self.gui.show_game_over()
            else:

                self._play_bot_turn_if_needed()

        except ValueError as e:
            self.gui.notify(f"Erreur: {e}")

    def _create_player(self, name: str, player_id: int, config: dict):
        player_type = config["type"]

        if player_type == "Humain":
            return Human(name, player_id, self.game, self.gui)

        if player_type == "IA (Stupide)":
            return StupidBot(name, player_id, self.game, self.gui)

        if player_type == "IA (MinMax)":
            return MinMaxBot(
                name,
                player_id,
                self.game,
                self.gui,
                max_depth=config.get("depth", 4),
                heuristic=config.get("heuristic", "score"),
            )

        if player_type == "IA (MCTS)":
            return MCTS(
                name,
                player_id,
                self.game,
                self.gui,
                max_iterations=config.get("iterations", 200),
                max_time=config.get("time", 1.0),
                temperature=config.get("temperature", 1.0),
            )

        raise ValueError(f"Type de joueur inconnu: {player_type}")