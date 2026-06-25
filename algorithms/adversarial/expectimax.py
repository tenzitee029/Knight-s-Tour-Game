import itertools
import random
import math
from .common import AdversarialBaseSolver


class ExpectimaxSolver(AdversarialBaseSolver):
    """MAX tìm đường, CHANCE tạo vật cản ngẫu nhiên."""

    MAX_GAMES = 100

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

        # MAX phải đi trên 50% tổng số ô
        self.max_win_target = math.ceil(
            self.total_cells * 0.5
        )
        self.game_count = 0
        self.winning_game = None
        self.max_won = False

        self.best_path = [self.start_pos]
        self.best_obstacles = set()

    def score_state(self, path, blocked):
        current_position = path[-1]

        valid_moves = self.get_valid_moves(
            current_position,
            path,
            blocked
        )

        return (
            len(path) * 100
            + len(valid_moves) * 20
            - len(blocked) * 5
        )

    def calculate_expected_value(self, path, blocked):
        """
        EV = 70% không khóa
           + 20% khóa 1 ô
           + 10% khóa 2 ô.
        """
        current_position = path[-1]

        candidates = self.get_valid_moves(
            current_position,
            path,
            blocked
        )

        normal_score = self.score_state(path, blocked)

        # Không được khóa nước cuối cùng
        if len(candidates) <= 1:
            return normal_score

        one_block_scores = []

        for position in candidates:
            new_blocked = set(blocked)
            new_blocked.add(position)

            one_block_scores.append(
                self.score_state(path, new_blocked)
            )

        average_one = (
            sum(one_block_scores)
            / len(one_block_scores)
        )

        # Còn đúng 2 nước thì chỉ được khóa 1 ô
        if len(candidates) == 2:
            average_two = average_one

        else:
            two_block_scores = []

            for pair in itertools.combinations(
                candidates,
                2
            ):
                new_blocked = set(blocked)
                new_blocked.update(pair)

                two_block_scores.append(
                    self.score_state(
                        path,
                        new_blocked
                    )
                )

            average_two = (
                sum(two_block_scores)
                / len(two_block_scores)
            )

        return (
            0.70 * normal_score
            + 0.15 * average_one
            + 0.15 * average_two
        )

    def choose_max_move(self, path):
        current_position = path[-1]

        valid_moves = self.get_valid_moves(
            current_position,
            path,
            self.dynamic_obstacles
        )

        best_moves = []
        best_value = float("-inf")

        for next_position in valid_moves:
            new_path = path + [next_position]

            expected_value = (
                self.calculate_expected_value(
                    new_path,
                    self.dynamic_obstacles
                )
            )

            if expected_value > best_value:
                best_value = expected_value
                best_moves = [next_position]

            elif expected_value == best_value:
                best_moves.append(next_position)

        if not best_moves:
            return None

        return random.choice(best_moves)

    def apply_chance_event(self, path):
        current_position = path[-1]

        candidates = self.get_valid_moves(
            current_position,
            path,
            self.dynamic_obstacles
        )

        # Luôn chừa ít nhất một nước cho MAX
        if len(candidates) <= 1:
            return

        random_value = random.random()

        if random_value < 0.70:
            number_to_block = 0

        elif random_value < 0.85:
            number_to_block = 1

        else:
            number_to_block = 2

        number_to_block = min(
            number_to_block,
            len(candidates) - 1
        )

        if number_to_block > 0:
            blocked_positions = random.sample(
                candidates,
                number_to_block
            )

            self.dynamic_obstacles.update(
                blocked_positions
            )

    def save_best_result(self, path):
        if len(path) > len(self.best_path):
            self.best_path = path.copy()
            self.best_obstacles = (
                self.dynamic_obstacles.copy()
            )

    def solve(self):
        total_visited_nodes = 0

        self.game_count = 0
        self.winning_game = None
        self.max_won = False
        self.best_path = [self.start_pos]
        self.best_obstacles = set()

        while self.game_count < self.MAX_GAMES:
            self.game_count += 1

            path = [self.start_pos]
            self.dynamic_obstacles.clear()

            # Hiển thị việc bắt đầu một trận mới
            yield path.copy(), total_visited_nodes, False

            while True:
                next_position = self.choose_max_move(path)
                total_visited_nodes += 1

                # MAX thua trận hiện tại
                if next_position is None:
                    self.save_best_result(path)
                    break

                path.append(next_position)
                self.save_best_result(path)

                yield (
                    path.copy(),
                    total_visited_nodes,
                    False
                )

                # MAX thắng, dừng toàn bộ quá trình
                if len(path) >= self.max_win_target:
                    self.max_won = True
                    self.winning_game = self.game_count

                    yield (
                        path.copy(),
                        total_visited_nodes,
                        True
                    )
                    return

                # CHANCE xuất hiện sau mỗi lượt MAX
                self.apply_chance_event(path)

                yield (
                    path.copy(),
                    total_visited_nodes,
                    False
                )

        # Không thắng sau 100 trận
        self.max_won = False
        self.dynamic_obstacles = (
            self.best_obstacles.copy()
        )

        yield (
            self.best_path.copy(),
            total_visited_nodes,
            True
        )