import math
import random

from .common import AdversarialBaseSolver


class MinimaxSolver(AdversarialBaseSolver):
    """
    AI MAX điều khiển quân mã.
    AI MIN khóa một nước đi sau mỗi 3 lượt của MAX.
    """

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

        # MAX thắng khi đi được ít nhất 70% số ô ban đầu
        self.max_win_target = math.ceil(
            self.total_cells * 0.5
        )

        self.winner = None
        self.max_won = False

    def minimax(
        self,
        path,
        dynamic_obstacles,
        depth,
        maximizing_player,
        max_move_count
    ):
        current_position = path[-1]

        valid_moves = self.get_valid_moves(
            current_position,
            path,
            dynamic_obstacles
        )

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

        # Chưa đủ 3 lượt MAX thì MIN bỏ lượt
        if max_move_count % 3 != 0:
            return self.minimax(
                path,
                dynamic_obstacles,
                depth - 1,
                True,
                max_move_count
            )

        # Chỉ còn một nước thì MIN không được khóa
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
            new_obstacles = set(
                dynamic_obstacles
            )
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
                depth=2,
                maximizing_player=False,
                max_move_count=max_move_count + 1
            )

            if score > best_score:
                best_score = score
                best_moves = [next_position]

            elif score == best_score:
                best_moves.append(next_position)

            if not best_moves:
                return None

            return random.choice(best_moves)

    def choose_min_block(
        self,
        path,
        max_move_count
    ):
        # MIN chỉ hành động sau mỗi 3 lượt MAX
        if max_move_count % 3 != 0:
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
                depth=1,
                maximizing_player=True,
                max_move_count=max_move_count
            )

            if score < worst_score:
                worst_score = score
                worst_blocks = [lock_position]

            elif score == worst_score:
                worst_blocks.append(lock_position)

            if not worst_blocks:
                return None

            return random.choice(worst_blocks)

    def solve(self):
        path = [self.start_pos]
        visited_nodes = 0
        max_move_count = 0

        self.winner = None
        self.max_won = False
        self.dynamic_obstacles.clear()

        while True:
            # Lượt AI MAX
            max_move = self.choose_max_move(
                path,
                max_move_count
            )

            visited_nodes += 1

            # MAX hết đường trước khi đạt 70%
            if max_move is None:
                self.winner = "MIN"
                self.max_won = False

                yield path.copy(), visited_nodes, True
                return

            path.append(max_move)
            max_move_count += 1

            yield path.copy(), visited_nodes, False

            # MAX đạt mục tiêu 70%
            if len(path) >= self.max_win_target:
                self.winner = "MAX"
                self.max_won = True

                yield path.copy(), visited_nodes, True
                return

            # MIN chỉ được xét sau mỗi 3 lượt MAX
            if max_move_count % 3 == 0:
                min_block = self.choose_min_block(
                    path,
                    max_move_count
                )

                if min_block is not None:
                    self.dynamic_obstacles.add(
                        min_block
                    )
                    visited_nodes += 1

                    yield (
                        path.copy(),
                        visited_nodes,
                        False
                    )