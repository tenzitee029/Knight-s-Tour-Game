from algorithms.uninformed.common import SearchBaseSolver


class SimpleHillClimbingSolver(SearchBaseSolver):
    """Simple Hill Climbing cho bài toán Knight's Tour.

    Thuật toán xem các trạng thái kề theo thứ tự sinh ra. Nếu gặp trạng thái
    có điểm đánh giá tốt hơn trạng thái hiện tại thì đi ngay sang trạng thái đó.
    Thuật toán không quay lui, nên có thể dừng khi rơi vào cực trị cục bộ.
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

    def count_onward_moves(self, position, path):
        new_path = path + [position]
        return len(self.get_valid_moves(position, new_path))

    def count_isolated_cells(self, path):
        """Đếm số ô chưa đi gần như bị cô lập để tránh chọn đường cụt sớm."""
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
        """Điểm càng lớn càng tốt.

        Ưu tiên đi được nhiều ô hơn. Khi hai lựa chọn gần giống nhau, thuật toán
        thích nước đi có ít nước đi tiếp hơn theo quy tắc Warnsdorff, nhưng tránh
        tạo nhiều ô bị cô lập.
        """
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

    def solve(self):
        path = [self.start_pos]
        visited_nodes_count = 1

        yield path.copy(), visited_nodes_count, False

        while len(path) < self.total_cells:
            current_position = path[-1]
            current_score = self.evaluate_path(path)
            next_path = None

            for next_position in self.get_valid_moves(current_position, path):
                candidate_path = path + [next_position]
                visited_nodes_count += 1

                if self.evaluate_path(candidate_path) > current_score:
                    next_path = candidate_path
                    break

            if next_path is None:
                break

            path = next_path
            yield path.copy(), visited_nodes_count, False

        yield path.copy(), visited_nodes_count, True
