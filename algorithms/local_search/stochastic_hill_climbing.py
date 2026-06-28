import random

from algorithms.uninformed.common import SearchBaseSolver


class StochasticHillClimbingSolver(SearchBaseSolver):
    """Stochastic Hill Climbing cho bài toán Knight's Tour.

    Đúng tinh thần thuật toán:
    - Mỗi bước sinh các trạng thái kề hợp lệ.
    - Chỉ giữ các trạng thái có heuristic tốt hơn trạng thái hiện tại.
    - Chọn ngẫu nhiên một trạng thái tốt hơn để đi tiếp.
    - Không random restart trong thuật toán này.
    """

    def get_valid_moves(self, position, path):
        row, col = position
        moves = []

        for delta_row, delta_col in self.knight_moves:
            next_row = row + delta_row
            next_col = col + delta_col

            if self.is_valid_position(next_row, next_col, path):
                moves.append((next_row, next_col))

        return moves

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
        """Hàm heuristic. Điểm càng lớn càng tốt."""
        if len(path) == self.total_cells:
            return 1_000_000

        current_position = path[-1]
        onward_moves = len(self.get_valid_moves(current_position, path))
        isolated_penalty = self.count_isolated_cells(path) * 25
        dead_end_penalty = 500 if onward_moves == 0 else 0
        path_length_score = len(path) * 100
        warnsdorff_bonus = 8 - onward_moves

        return path_length_score + warnsdorff_bonus - isolated_penalty - dead_end_penalty

    def weighted_random_choice(self, candidates):
        """Chọn ngẫu nhiên, nhưng ưu tiên ứng viên có điểm heuristic cao hơn."""
        min_score = min(score for score, _ in candidates)
        weights = [(score - min_score) + 1 for score, _ in candidates]

        return random.choices(
            [candidate for _, candidate in candidates],
            weights=weights,
            k=1
        )[0]

    def run_one_attempt(self):
        """Chạy đúng 1 lần Stochastic Hill Climbing.

        Hàm này được tách riêng để Random Restart Hill Climbing có thể tái sử dụng.
        """
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
                    improving_candidates.append((candidate_score, candidate_path))

            if not improving_candidates:
                break

            path = self.weighted_random_choice(improving_candidates)
            yield path.copy(), visited_nodes_count, False

        return path, visited_nodes_count

    def solve(self):
        """Stochastic Hill Climbing chỉ chạy 1 attempt, không restart."""
        attempt_generator = self.run_one_attempt()
        final_path = [self.start_pos]
        final_nodes = 1

        try:
            while True:
                path, visited_nodes_count, done = next(attempt_generator)
                final_path = path
                final_nodes = visited_nodes_count
                yield path.copy(), visited_nodes_count, done

        except StopIteration as stop_result:
            if stop_result.value:
                final_path, final_nodes = stop_result.value

        yield final_path.copy(), final_nodes, True
