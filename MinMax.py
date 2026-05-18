import random
from math import inf
from typing import Any, Optional

from Awale import Awale

class MinMaxBot:
    def __init__(
        self,
        name: str,
        player_id: int,
        game: Awale,
        gui: Optional[Any] = None,
        max_depth: int = 4,
        heuristic: str = "score",  
    ):
        self.name = name
        self.player_id = player_id
        self.game = game
        self.gui = gui
        self.max_depth = max_depth
        self.heuristic = heuristic

    def set_game(self, game: Awale) -> None:
        self.game = game

    def notify(self, message: str) -> None:
        if self.gui is not None and hasattr(self.gui, "notify"):
            self.gui.notify(message)
        else:
            print(message)

    def choose_move(self) -> int:
        legal_moves = self.game.get_legal_moves()
        if not legal_moves:
            raise ValueError(f"{self.name} n'a pas de coup legal disponible.")

        maximizing = self.game.get_current_player() == self.player_id
        best_value = -inf if maximizing else inf
        best_moves: list[int] = []

        alpha = -inf
        beta = inf

        for pit in legal_moves:
            next_state = self.game.simulate_move(pit)
            value = self._alphabeta(
                state=next_state,
                depth=self.max_depth - 1,
                alpha=alpha,
                beta=beta,
            )

            if maximizing:
                if value > best_value:
                    best_value = value
                    best_moves = [pit]
                elif value == best_value:
                    best_moves.append(pit)
                alpha = max(alpha, best_value)
            else:
                if value < best_value:
                    best_value = value
                    best_moves = [pit]
                elif value == best_value:
                    best_moves.append(pit)
                beta = min(beta, best_value)

        return random.choice(best_moves) if best_moves else legal_moves[0]

    def _alphabeta(self, state: Awale, depth: int, alpha: float, beta: float) -> float:
        if depth == 0 or state.is_game_over():
            return self._evaluate(state)

        legal_moves = state.get_legal_moves()
        if not legal_moves:
            return self._evaluate(state)

        maximizing = state.get_current_player() == self.player_id

        if maximizing:
            value = -inf
            for pit in legal_moves:
                child = state.simulate_move(pit)
                value = max(value, self._alphabeta(child, depth - 1, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value

        value = inf
        for pit in legal_moves:
            child = state.simulate_move(pit)
            value = min(value, self._alphabeta(child, depth - 1, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value

    def _evaluate(self, state: Awale) -> float:
        if state.is_game_over():
            winner = state.get_winner()
            if winner is None:
                return 0.0
            return 10000.0 if winner == self.player_id else -10000.0

        if self.heuristic == "mobility":
            return self._heuristic_mobility(state)
        return self._heuristic_score(state)

    def _heuristic_score(self, state: Awale) -> float:
        score0, score1 = state.get_score()
        my_score = score0 if self.player_id == 0 else score1
        opp_score = score1 if self.player_id == 0 else score0
        return float(my_score - opp_score)

    def _heuristic_mobility(self, state: Awale) -> float:
        board = state.get_board()
        my_range = range(0, 6) if self.player_id == 0 else range(6, 12)
        opp_range = range(6, 12) if self.player_id == 0 else range(0, 6)

        my_side_seeds = sum(board[i] for i in my_range)
        opp_side_seeds = sum(board[i] for i in opp_range)

        score0, score1 = state.get_score()
        my_score = score0 if self.player_id == 0 else score1
        opp_score = score1 if self.player_id == 0 else score0

        return 0.5 * (my_score - opp_score) + 0.1 * (my_side_seeds - opp_side_seeds)


