from algorithms.uninformed.common import SearchBaseSolver


class IDAStarSolver(SearchBaseSolver):
    """Iterative Deepening A* cho bài toán Knight's Tour.

    Thuật toán dùng ngưỡng f(n) = g(n) + h(n), sau đó tăng ngưỡng dần.
    h(n) ước lượng số bước còn lại để hoàn thành hành trình.
    Các nước đi được sắp xếp theo heuristic Warnsdorff để dễ tìm đường đi
    đầy đủ hơn trên bàn cờ lớn.
    """

    MAX_EXPANSIONS = 300_000
    MAX_ITERATIONS = 200

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
        return self.total_cells - len(path)

    def calculate_f_score(self, path):
        g_score = len(path) - 1
        h_score = self.heuristic(path)
        return g_score + h_score

    def order_moves(self, position, path):
        valid_moves = self.get_valid_moves(position, path)
        valid_moves.sort(
            key=lambda move: self.count_onward_moves(move, path)
        )
        return valid_moves

    def solve(self):
        path = [self.start_pos]
        threshold = self.calculate_f_score(path)
        visited_nodes_count = 0
        best_path = path.copy()
        iteration_count = 0

        def depth_first_search(current_threshold):
            nonlocal visited_nodes_count
            nonlocal best_path
            nonlocal next_threshold

            visited_nodes_count += 1

            if len(path) > len(best_path):
                best_path = path.copy()

            yield path.copy(), visited_nodes_count, False

            f_score = self.calculate_f_score(path)

            if f_score > current_threshold:
                next_threshold = min(next_threshold, f_score)
                return False

            if len(path) == self.total_cells:
                yield path.copy(), visited_nodes_count, True
                return True

            if visited_nodes_count >= self.MAX_EXPANSIONS:
                return False

            current_position = path[-1]

            for next_position in self.order_moves(current_position, path):
                path.append(next_position)

                found = yield from depth_first_search(current_threshold)

                if found:
                    return True

                path.pop()

                if visited_nodes_count >= self.MAX_EXPANSIONS:
                    return False

            return False

        while (
            iteration_count < self.MAX_ITERATIONS
            and visited_nodes_count < self.MAX_EXPANSIONS
        ):
            next_threshold = float("inf")
            found = yield from depth_first_search(threshold)

            if found:
                return

            if next_threshold == float("inf"):
                break

            threshold = next_threshold
            iteration_count += 1

        yield best_path, visited_nodes_count, True
