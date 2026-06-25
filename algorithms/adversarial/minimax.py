import math
import random

from .common import AdversarialBaseSolver


class MinimaxSolver(AdversarialBaseSolver):
    """
    AI MAX điều khiển quân mã.
    AI MIN khóa một nước đi sau mỗi 2 lượt MAX.
    Nếu MAX thua, tự bắt đầu trận mới.
    """

    MAX_GAMES = 100
    SEARCH_DEPTH = 3
    def __init__(
        self,
        rows,
        cols,
        start_pos=(0, 0),
        obstacles=None
    ):
        super().__init__(
            rows,
            cols,
            start_pos,
            obstacles
        )

        # MAX thắng khi đạt ít nhất 50% số ô
        self.max_win_target = math.ceil(
            self.total_cells * 0.5
        )

        self.game_count = 0
        self.winning_game = None
        self.max_won = False
        self.winner = None

        self.best_path = [self.start_pos]
        self.best_obstacles = set()
        self.search_nodes = 0

    def minimax(
        self,
        path,
        dynamic_obstacles,
        depth,
        maximizing_player,
        max_move_count
    ):
        self.search_nodes += 1

        current_position = path[-1]

        valid_moves = self.get_valid_moves(
            current_position,
            path,
            dynamic_obstacles
        )

        if len(path) >= self.max_win_target:
            return 1_000_000

        if depth == 0 or not valid_moves:
            return self.evaluate_state(
                path,
                dynamic_obstacles
            )

        if maximizing_player:
            best_score = float("-inf")

            for next_position in valid_moves:
                new_path = path + [next_position]

                score = self.minimax(
                    new_path,
                    set(dynamic_obstacles),
                    depth - 1,
                    False,
                    max_move_count + 1
                )

                best_score = max(
                    best_score,
                    score
                )

            return best_score

        # MIN chỉ hành động sau mỗi 2 lượt MAX
        if max_move_count % 2 != 0:
            return self.minimax(
                path,
                dynamic_obstacles,
                depth - 1,
                True,
                max_move_count
            )

        # MIN không được khóa nước cuối cùng
        if len(valid_moves) <= 1:
            return self.minimax(
                path,
                dynamic_obstacles,
                depth - 1,
                True,
                max_move_count
            )

        worst_score = float("inf")

        for lock_position in valid_moves:
            new_obstacles = set(dynamic_obstacles)
            new_obstacles.add(lock_position)

            score = self.minimax(
                path,
                new_obstacles,
                depth - 1,
                True,
                max_move_count
            )

            worst_score = min(
                worst_score,
                score
            )

        return worst_score

    def choose_max_move(
        self,
        path,
        max_move_count
    ):
        current_position = path[-1]

        valid_moves = self.get_valid_moves(
            current_position,
            path,
            self.dynamic_obstacles
        )

        random.shuffle(valid_moves)

        best_moves = []
        best_score = float("-inf")

        for next_position in valid_moves:
            new_path = path + [next_position]

            score = self.minimax(
                new_path,
                set(self.dynamic_obstacles),
                depth=self.SEARCH_DEPTH,
                maximizing_player=False,
                max_move_count=max_move_count + 1
            )

            if score > best_score:
                best_score = score
                best_moves = [next_position]

            elif score == best_score:
                best_moves.append(next_position)

        # Phải nằm ngoài vòng for
        if not best_moves:
            return None

        return random.choice(best_moves)

    def choose_min_block(
        self,
        path,
        max_move_count
    ):
        # MIN chỉ hành động sau mỗi 2 lượt MAX
        if max_move_count % 2 != 0:
            return None

        current_position = path[-1]

        candidates = self.get_valid_moves(
            current_position,
            path,
            self.dynamic_obstacles
        )

        random.shuffle(candidates)

        # MIN không được khóa nước cuối cùng
        if len(candidates) <= 1:
            return None

        worst_blocks = []
        worst_score = float("inf")

        for lock_position in candidates:
            test_obstacles = set(
                self.dynamic_obstacles
            )
            test_obstacles.add(lock_position)

            score = self.minimax(
                path,
                test_obstacles,
                depth=self.SEARCH_DEPTH,
                maximizing_player=True,
                max_move_count=max_move_count
            )

            if score < worst_score:
                worst_score = score
                worst_blocks = [lock_position]

            elif score == worst_score:
                worst_blocks.append(lock_position)

        # Phải nằm ngoài vòng for
        if not worst_blocks:
            return None

        return random.choice(worst_blocks)

    def save_best_result(self, path):
        if len(path) > len(self.best_path):
            self.best_path = path.copy()
            self.best_obstacles = (
                self.dynamic_obstacles.copy()
            )

    def solve(self):
        self.game_count = 0
        self.winning_game = None
        self.max_won = False
        self.winner = None

        self.best_path = [self.start_pos]
        self.best_obstacles = set()
        self.search_nodes = 0

        while self.game_count < self.MAX_GAMES:
            self.game_count += 1

            path = [self.start_pos]
            max_move_count = 0
            self.dynamic_obstacles.clear()

            # Bắt đầu trận mới
            yield (
                path.copy(),
                self.search_nodes,
                False
            )

            while True:
                max_move = self.choose_max_move(
                    path,
                    max_move_count
                )

                # MAX thua trận hiện tại
                if max_move is None:
                    self.save_best_result(path)
                    break

                path.append(max_move)
                max_move_count += 1
                self.save_best_result(path)

                yield (
                    path.copy(),
                    self.search_nodes,
                    False
                )

                # MAX đạt mục tiêu 50%
                if len(path) >= self.max_win_target:
                    self.max_won = True
                    self.winner = "MAX"
                    self.winning_game = self.game_count

                    yield (
                        path.copy(),
                        self.search_nodes,
                        True
                    )
                    return

                # MIN chỉ khóa sau mỗi 2 lượt MAX
                if max_move_count % 2 == 0:
                    min_block = self.choose_min_block(
                        path,
                        max_move_count
                    )

                    if min_block is not None:
                        self.dynamic_obstacles.add(
                            min_block
                        )

                        yield (
                            path.copy(),
                            self.search_nodes,
                            False
                        )

        # Không thắng sau 100 trận: dùng trận tốt nhất
        self.max_won = False
        self.winner = None

        self.dynamic_obstacles = (
            self.best_obstacles.copy()
        )

        yield (
            self.best_path.copy(),
            self.search_nodes,
            True
        )