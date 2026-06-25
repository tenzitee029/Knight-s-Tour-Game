import random

from algorithms.uninformed.common import SearchBaseSolver


class StochasticHillClimbingSolver(SearchBaseSolver):
    """Stochastic Hill Climbing cho bài toán Knight's Tour.

    Thuật toán lấy các trạng thái kề có điểm tốt hơn trạng thái hiện tại, sau đó
    chọn ngẫu nhiên một trạng thái để đi tiếp. Cách này giúp đường đi bớt cứng
    hơn Simple Hill Climbing, nhưng vẫn có thể mắc cực trị cục bộ.
    """

    MAX_RANDOM_ATTEMPTS = 50

    def get_valid_moves(self, position, path):
        row, col = position
        moves = []

        for delta_row, delta_col in self.knight_moves:
            next_row = row + delta_row
            next_col = col + delta_col

            if self.is_valid_position(next_row, next_col, path):
                moves.append((next_row, next_col))

        return moves

    def count_onward_moves(self, position, path):
        new_path = path + [position]
        return len(self.get_valid_moves(position, new_path))

    def count_isolated_cells(self, path):
        visited = set(path)
        remaining_cells = []

        for row in range(self.rows):
            for col in range(self.cols):
                position = (row, col)

                if position not in visited and position not in self.obstacles:
                    remaining_cells.append(position)

        if not remaining_cells:
            return 0

        available_sources = set(remaining_cells)
        available_sources.add(path[-1])
        isolated_count = 0

        for cell in remaining_cells:
            reachable_count = 0
            cell_row, cell_col = cell

            for delta_row, delta_col in self.knight_moves:
                neighbor = (cell_row + delta_row, cell_col + delta_col)

                if neighbor in available_sources:
                    reachable_count += 1

            if reachable_count <= 1:
                isolated_count += 1

        return isolated_count

    def evaluate_path(self, path):
        """Điểm càng lớn càng tốt."""
        if len(path) == self.total_cells:
            return 1_000_000

        current_position = path[-1]
        onward_moves = len(self.get_valid_moves(current_position, path))
        isolated_penalty = self.count_isolated_cells(path) * 25

        if onward_moves == 0:
            dead_end_penalty = 500
        else:
            dead_end_penalty = 0

        path_length_score = len(path) * 100
        warnsdorff_bonus = 8 - onward_moves

        return path_length_score + warnsdorff_bonus - isolated_penalty - dead_end_penalty

    def weighted_random_choice(self, candidates):
        """Chọn ngẫu nhiên, nhưng ưu tiên ứng viên có điểm cao hơn."""
        min_score = min(score for score, _ in candidates)
        weights = []

        for score, _ in candidates:
            weights.append((score - min_score) + 1)

        return random.choices(
            [candidate for _, candidate in candidates],
            weights=weights,
            k=1
        )[0]

    def run_one_attempt(self):
        path = [self.start_pos]
        visited_nodes_count = 1

        yield path.copy(), visited_nodes_count, False

        while len(path) < self.total_cells:
            current_position = path[-1]
            current_score = self.evaluate_path(path)
            improving_candidates = []

            for next_position in self.get_valid_moves(current_position, path):
                candidate_path = path + [next_position]
                candidate_score = self.evaluate_path(candidate_path)
                visited_nodes_count += 1

                if candidate_score > current_score:
                    improving_candidates.append(
                        (candidate_score, candidate_path)
                    )

            if not improving_candidates:
                break

            path = self.weighted_random_choice(improving_candidates)
            yield path.copy(), visited_nodes_count, False

        return path, visited_nodes_count

    def solve(self):
        total_visited_nodes = 0
        best_path = [self.start_pos]

        for _ in range(self.MAX_RANDOM_ATTEMPTS):
            attempt_generator = self.run_one_attempt()
            final_path = [self.start_pos]
            previous_attempt_nodes = 0

            try:
                while True:
                    path, attempt_nodes, done = next(attempt_generator)
                    final_path = path
                    node_delta = max(0, attempt_nodes - previous_attempt_nodes)
                    previous_attempt_nodes = attempt_nodes
                    total_visited_nodes += node_delta

                    if len(path) > len(best_path):
                        best_path = path.copy()

                    yield path.copy(), total_visited_nodes, False

            except StopIteration as stop_result:
                if stop_result.value:
                    final_path, attempt_nodes = stop_result.value
                    node_delta = max(0, attempt_nodes - previous_attempt_nodes)
                    total_visited_nodes += node_delta

            if len(final_path) > len(best_path):
                best_path = final_path.copy()

            if len(best_path) == self.total_cells:
                yield best_path.copy(), total_visited_nodes, True
                return

        yield best_path.copy(), total_visited_nodes, True
