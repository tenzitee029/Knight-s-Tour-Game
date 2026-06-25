import heapq
import itertools

from algorithms.uninformed.common import SearchBaseSolver


class AStarSolver(SearchBaseSolver):
    """A* Search cho bài toán Knight's Tour.

    Với Knight's Tour, mọi lời giải đều có cùng độ dài là số ô hợp lệ.
    Vì vậy f(n) được dùng theo hướng ưu tiên trạng thái gần hoàn thành hơn:
    f(n) = số ô còn lại + điểm phạt heuristic.
    """

    MAX_EXPANSIONS = 300_000

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

    def heuristic(self, path):
        if len(path) == self.total_cells:
            return 0

        current_position = path[-1]
        onward_moves = len(self.get_valid_moves(current_position, path))

        if onward_moves == 0:
            return 1_000_000

        isolated_penalty = self.count_isolated_cells(path) * 20
        warnsdorff_penalty = onward_moves

        return isolated_penalty + warnsdorff_penalty

    def calculate_f_score(self, path):
        remaining_steps = self.total_cells - len(path)
        h_score = self.heuristic(path)
        return remaining_steps + h_score

    def solve(self):
        start_path = [self.start_pos]
        counter = itertools.count()
        priority_queue = [
            (
                self.calculate_f_score(start_path),
                self.heuristic(start_path),
                -len(start_path),
                next(counter),
                self.start_pos,
                start_path
            )
        ]

        visited_nodes_count = 0
        best_path = start_path.copy()

        while priority_queue and visited_nodes_count < self.MAX_EXPANSIONS:
            _, _, _, _, current_position, path = heapq.heappop(priority_queue)
            visited_nodes_count += 1

            if len(path) > len(best_path):
                best_path = path.copy()

            yield path, visited_nodes_count, False

            if len(path) == self.total_cells:
                yield path, visited_nodes_count, True
                return

            valid_moves = self.get_valid_moves(current_position, path)
            valid_moves.sort(
                key=lambda move: self.count_onward_moves(move, path)
            )

            for next_position in valid_moves:
                new_path = path + [next_position]
                heapq.heappush(
                    priority_queue,
                    (
                        self.calculate_f_score(new_path),
                        self.heuristic(new_path),
                        -len(new_path),
                        next(counter),
                        next_position,
                        new_path
                    )
                )

        yield best_path, visited_nodes_count, True
