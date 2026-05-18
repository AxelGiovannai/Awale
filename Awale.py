from typing import Optional, Tuple


class Awale:
    def __init__(self):
        self.board = [4] * 12
        self.score = [0, 0]
        self.current_player = 0

    def clone(self) -> "Awale":
        clone_game = Awale()
        clone_game.board = self.board.copy()
        clone_game.score = self.score.copy()
        clone_game.current_player = self.current_player
        return clone_game

    def get_board(self) -> list[int]:
        return self.board.copy()

    def get_score(self) -> Tuple[int, int]:
        return tuple(self.score)

    def get_current_player(self) -> int:
        return self.current_player

    def _player_pits(self, player: int) -> range:
        return range(0, 6) if player == 0 else range(6, 12)

    def _is_player_pit(self, pit: int, player: int) -> bool:
        return pit in self._player_pits(player)

    def _sow(self, pit: int) -> int:
        seeds = self.board[pit]
        self.board[pit] = 0

        current_index = pit
        while seeds > 0:
            current_index = (current_index + 1) % 12
            if current_index == pit:
                current_index = (current_index + 1) % 12
            self.board[current_index] += 1
            seeds -= 1

        return current_index

    def _capture(self, last_index: int, player: int) -> int:
        opponent = 1 - player
        if not self._is_player_pit(last_index, opponent):
            return 0

        captured = 0
        index = last_index

        while self._is_player_pit(index, opponent) and self.board[index] in (2, 3):
            captured += self.board[index]
            self.board[index] = 0
            index = (index - 1) % 12

        return captured

    def _perform_move(self, pit: int) -> int:
        player = self.current_player
        last_index = self._sow(pit)
        captured = self._capture(last_index, player)
        self.score[player] += captured
        self.current_player = 1 - player
        return captured

    def _collect_remaining_seeds(self) -> None:
        self.score[0] += sum(self.board[0:6])
        self.score[1] += sum(self.board[6:12])
        self.board = [0] * 12

    def _move_keeps_opponent_seed(self, pit: int) -> bool:
        simulated_game = self.clone()
        simulated_game._perform_move(pit)

        opponent = 1 - self.current_player
        return sum(simulated_game.board[i] for i in self._player_pits(opponent)) > 0

    def _has_legal_move(self) -> bool:
        player = self.current_player

        for pit in self._player_pits(player):
            if self.board[pit] == 0:
                continue
            if self._move_keeps_opponent_seed(pit):
                return True

        return False

    def get_legal_moves(self) -> list[int]:
        legal_moves = []

        for pit in self._player_pits(self.current_player):
            if self.board[pit] == 0:
                continue

            if self._move_keeps_opponent_seed(pit):
                legal_moves.append(pit)

        return legal_moves

    def is_legal_move(self, pit: int) -> bool:
        if pit < 0 or pit >= 12:
            return False
        if not self._is_player_pit(pit, self.current_player):
            return False
        if self.board[pit] == 0:
            return False
        return pit in self.get_legal_moves()

    def apply_move(self, pit: int) -> Tuple[int, bool]:
        if not self.is_legal_move(pit):
            raise ValueError(f"Coup illégal: pit {pit}")

        captured = self._perform_move(pit)

        game_over = self.is_game_over()
        if game_over:
            self._collect_remaining_seeds()

        return captured, game_over

    def simulate_move(self, pit: int) -> "Awale":
        simulated_game = self.clone()
        simulated_game.apply_move(pit)
        return simulated_game

    def is_game_over(self) -> bool:
        if self.score[0] >= 25 or self.score[1] >= 25:
            return True
        if sum(self.board) == 0:
            return True
        return not self._has_legal_move()

    def get_winner(self) -> Optional[int]:
        if not self.is_game_over():
            return None

        if self.score[0] > self.score[1]:
            return 0
        if self.score[1] > self.score[0]:
            return 1
        return None