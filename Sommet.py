import math
import random
from dataclasses import dataclass, field
from typing import Optional

from Awale import Awale


@dataclass
class Sommet:
    state: Awale
    parent: Optional["Sommet"] = None
    move: Optional[int] = None
    children: dict[int, "Sommet"] = field(default_factory=dict)
    untried_moves: list[int] = field(default_factory=list)
    visits: int = 0
    total_reward: float = 0.0

    def __post_init__(self) -> None:
        if not self.untried_moves:
            self.untried_moves = self.state.get_legal_moves()

    def is_terminal(self) -> bool:
        return self.state.is_game_over()

    def is_fully_expanded(self) -> bool:
        return len(self.untried_moves) == 0

    def expand(self) -> Optional["Sommet"]:
        if self.is_terminal() or not self.untried_moves:
            return None

        move = self.untried_moves.pop(random.randrange(len(self.untried_moves)))
        next_state = self.state.simulate_move(move)
        child = Sommet(state=next_state, parent=self, move=move)
        self.children[move] = child
        return child

    def best_child(self, exploration_weight: float = 1.41421356237) -> Optional["Sommet"]:
        if not self.children:
            return None

        best_score = -math.inf
        best_children: list[Sommet] = []

        for child in self.children.values():
            if child.visits == 0:
                score = math.inf
            else:
                exploitation = child.total_reward / child.visits
                exploration = exploration_weight * math.sqrt(
                    math.log(self.visits + 1) / child.visits
                )
                score = exploitation + exploration

            if score > best_score:
                best_score = score
                best_children = [child]
            elif score == best_score:
                best_children.append(child)

        return random.choice(best_children)