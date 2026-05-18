import math
import random
import time
from typing import Any, Optional

from Awale import Awale
from Sommet import Sommet


class MCTS:
    def __init__(
        self,
        name: str,
        player_id: int,
        game: Awale,
        gui: Optional[Any] = None,
        max_iterations: int = 200,
        max_time: float = 1.0,
        temperature: float = 1.0,
        rollout_limit: int = 80,
    ):
        self.name = name
        self.player_id = player_id
        self.game = game
        self.gui = gui
        self.max_iterations = max_iterations
        self.max_time = max_time
        self.temperature = temperature
        self.rollout_limit = rollout_limit

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
            raise ValueError(f"{self.name} n'a pas de coup légal disponible.")

        root = Sommet(state=self.game.clone())

        start_time = time.time()
        iterations = 0

        while iterations < self.max_iterations:
            if self.max_time is not None and (time.time() - start_time) >= self.max_time:
                break

            node = root

            while node.is_fully_expanded() and not node.is_terminal():
                next_node = node.best_child()
                if next_node is None:
                    break
                node = next_node

            if not node.is_terminal():
                expanded = node.expand()
                if expanded is not None:
                    node = expanded

            reward = self._rollout(node.state.clone())
            self._backpropagate(node, reward)

            iterations += 1

        return self._select_final_move(root, legal_moves)

    def _rollout(self, state: Awale) -> float:
        depth = 0

        while not state.is_game_over() and depth < self.rollout_limit:
            legal_moves = state.get_legal_moves()
            if not legal_moves:
                break

            move = random.choice(legal_moves)
            state.apply_move(move)
            depth += 1

        winner = state.get_winner()
        if winner is None:
            return 0.5
        if winner == self.player_id:
            return 1.0
        return 0.0

    def _backpropagate(self, node: Sommet, reward: float) -> None:
        current = node
        while current is not None:
            current.visits += 1
            current.total_reward += reward
            current = current.parent

    def _select_final_move(self, root: Sommet, legal_moves: list[int]) -> int:
        if not root.children:
            return random.choice(legal_moves)

        children = list(root.children.values())

        if self.temperature is not None and self.temperature > 0:
            weights = []
            for child in children:
                visits = max(child.visits, 1)
                weight = visits ** (1.0 / self.temperature)
                weights.append(weight)
            return random.choices(children, weights=weights, k=1)[0].move

        best_visits = max(child.visits for child in children)
        best_children = [child for child in children if child.visits == best_visits]
        return random.choice(best_children).move

    def debug_summary(self, root: Sommet) -> str:
        return (
            f"iterations={root.visits}, "
            f"children={len(root.children)}"
        )