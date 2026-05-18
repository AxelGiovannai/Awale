from __future__ import annotations

import time
from dataclasses import dataclass, field
from itertools import combinations
from typing import Any, Optional

from Awale import Awale
from Gui_tkinter import GuiTkinter
from Human import Human
from MinMax import MinMaxBot
from MCTS import MCTS
from StupidBot import StupidBot


@dataclass(frozen=True)
class PlayerSpec:
    kind: str
    name: str
    params: dict[str, Any] = field(default_factory=dict)


@dataclass
class MatchOutcome:
    starting_player: int
    winner: Optional[int]
    score0: int
    score1: int
    moves: int


@dataclass
class SeriesSummary:
    label: str
    starting_player: int
    games: int = 0
    p0_wins: int = 0
    p1_wins: int = 0
    draws: int = 0
    score0_total: int = 0
    score1_total: int = 0
    moves_total: int = 0

    def add(self, outcome: MatchOutcome) -> None:
        self.games += 1
        self.score0_total += outcome.score0
        self.score1_total += outcome.score1
        self.moves_total += outcome.moves

        if outcome.winner is None:
            self.draws += 1
        elif outcome.winner == 0:
            self.p0_wins += 1
        else:
            self.p1_wins += 1

    def as_text(self) -> str:
        avg_score0 = self.score0_total / self.games if self.games else 0.0
        avg_score1 = self.score1_total / self.games if self.games else 0.0
        avg_moves = self.moves_total / self.games if self.games else 0.0

        return (
            f"{self.label} | start={self.starting_player} | games={self.games} | "
            f"p0={self.p0_wins} | p1={self.p1_wins} | draws={self.draws} | "
            f"avg_score0={avg_score0:.2f} | avg_score1={avg_score1:.2f} | "
            f"avg_moves={avg_moves:.2f}"
        )


def build_player(spec: PlayerSpec, game: Awale, player_id: int, gui: Optional[Any] = None):
    kind = spec.kind.strip()

    if kind == "Humain":
        return Human(spec.name, player_id, game, gui)

    if kind == "IA (Stupide)":
        return StupidBot(spec.name, player_id, game, gui)

    if kind == "IA (MinMax)":
        return MinMaxBot(
            spec.name,
            player_id,
            game,
            gui,
            max_depth=spec.params.get("depth", 4),
            heuristic=spec.params.get("heuristic", "score"),
        )

    if kind == "IA (MCTS)":
        return MCTS(
            spec.name,
            player_id,
            game,
            gui,
            max_iterations=spec.params.get("iterations", 200),
            max_time=spec.params.get("time", 1.0),
            temperature=spec.params.get("temperature", 1.0),
        )

    raise ValueError(f"Type de joueur inconnu: {kind}")


def play_match( player0_spec: PlayerSpec, player1_spec: PlayerSpec, starting_player: int = 0, gui: Optional[GuiTkinter] = None, gui_delay: float = 0.0, verbose: bool = False, ) -> MatchOutcome:
    game = Awale()
    game.current_player = starting_player

    player0 = build_player(player0_spec, game, 0, gui)
    player1 = build_player(player1_spec, game, 1, gui)
    players = [player0, player1]

    if gui is not None:
        gui.set_game(game)
        gui.show_game()
        gui.notify(f"Debut de partie: {players[game.get_current_player()].name} commence.")
        gui.root.update_idletasks()
        gui.root.update()

    move_count = 0

    while not game.is_game_over():
        current_player = game.get_current_player()
        current_bot = players[current_player]

        if isinstance(current_bot, Human) and gui is None:
            raise ValueError("Un joueur humain ne peut pas etre utilise en mode headless.")

        move = current_bot.choose_move()
        captured, _ = game.apply_move(move)
        move_count += 1

        if verbose:
            print(f"J{current_player} -> {move} ({captured} capture(s))")

        if gui is not None:
            gui.refresh()
            if captured > 0:
                gui.notify(f"{current_bot.name} joue {move} et capture {captured} graine(s).")
            else:
                gui.notify(f"{current_bot.name} joue {move}.")
            gui.root.update_idletasks()
            gui.root.update()
            if gui_delay > 0:
                time.sleep(gui_delay)

    if gui is not None:
        gui.show_game_over()
        gui.root.update_idletasks()
        gui.root.update()

    winner = game.get_winner()
    score0, score1 = game.get_score()

    return MatchOutcome(
        starting_player=starting_player,
        winner=winner,
        score0=score0,
        score1=score1,
        moves=move_count,
    )


def run_series(
    player0_spec: PlayerSpec, player1_spec: PlayerSpec, games: int = 100, starting_player: int = 0, gui: Optional[GuiTkinter] = None, gui_delay: float = 0.0, verbose: bool = False, label: Optional[str] = None, ) -> SeriesSummary:
    summary = SeriesSummary(
        label=label or f"{player0_spec.name} vs {player1_spec.name}",
        starting_player=starting_player,
    )

    for _ in range(games):
        outcome = play_match(
            player0_spec=player0_spec,
            player1_spec=player1_spec,
            starting_player=starting_player,
            gui=gui,
            gui_delay=gui_delay,
            verbose=verbose,
        )
        summary.add(outcome)

    return summary


def compare_starting_player_effect( player0_spec: PlayerSpec, player1_spec: PlayerSpec, games_per_start: int = 100, gui: Optional[GuiTkinter] = None, gui_delay: float = 0.0, ) -> dict[int, SeriesSummary]:
    print(
        f"[stats]  - start=0: {player0_spec.name} vs {player1_spec.name}",
        flush=True,
    )
    summary0 = run_series(
        player0_spec,
        player1_spec,
        games=games_per_start,
        starting_player=0,
        gui=gui,
        gui_delay=gui_delay,
        label=f"{player0_spec.name} vs {player1_spec.name}",
    )

    print(
        f"[stats]  - start=1: {player0_spec.name} vs {player1_spec.name}",
        flush=True,
    )
    summary1 = run_series(
        player0_spec,
        player1_spec,
        games=games_per_start,
        starting_player=1,
        gui=gui,
        gui_delay=gui_delay,
        label=f"{player0_spec.name} vs {player1_spec.name}",
    )

    return {0: summary0, 1: summary1}


def run_all_pairs( specs: list[PlayerSpec], games_per_start: int = 100, ) -> list[tuple[PlayerSpec, PlayerSpec, dict[int, SeriesSummary]]]:
    results = []
    total_pairs = len(specs) * (len(specs) - 1) // 2
    for index, (spec_a, spec_b) in enumerate(combinations(specs, 2), start=1):
        print(f"[stats] Paire {index}/{total_pairs}: {spec_a.name} vs {spec_b.name}", flush=True)
        results.append(
            (
                spec_a,
                spec_b,
                compare_starting_player_effect(spec_a, spec_b, games_per_start=games_per_start),
            )
        )
    return results


def print_report(results: list[tuple[PlayerSpec, PlayerSpec, dict[int, SeriesSummary]]]) -> None:
    for spec_a, spec_b, by_start in results:
        print(f"\n### {spec_a.name} vs {spec_b.name}")
        for start_player, summary in by_start.items():
            print(summary.as_text())


if __name__ == "__main__":
    minmax_score = PlayerSpec("IA (MinMax)", "MinMax score", {"depth": 4, "heuristic": "score"})
    minmax_mobility = PlayerSpec("IA (MinMax)", "MinMax mobility", {"depth": 4, "heuristic": "mobility"})
    stupid = PlayerSpec("IA (Stupide)", "Stupid Bot")
    mcts = PlayerSpec("IA (MCTS)", "MCTS", {"iterations": 200, "time": 1.0, "temperature": 1.0})

    specs = [minmax_score, minmax_mobility, stupid, mcts]
    results = run_all_pairs(specs, games_per_start=100)
    print_report(results)