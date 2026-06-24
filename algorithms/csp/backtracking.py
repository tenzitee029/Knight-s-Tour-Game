from .common import CSPBaseSolver


class BacktrackingSolver(CSPBaseSolver):
    """Giải Knight's Tour bằng Backtracking Search."""

    def solve(self):
        path = [self.start_pos]
        visited = {self.start_pos}

        visited_nodes = 0
        best_path = path.copy()
        def backtrack():
            nonlocal visited_nodes
            nonlocal best_path

            visited_nodes += 1

            # Lưu lại đường đi dài nhất đã tìm được
            if len(path) > len(best_path):
                best_path = path.copy()

            # Gửi trạng thái hiện tại cho giao diện
            yield path.copy(), visited_nodes, False

            # Đã đi qua toàn bộ ô hợp lệ
            if len(path) == self.total_cells:
                yield path.copy(), visited_nodes, True
                return True



            current_position = path[-1]

            # Lấy các nước đi hợp lệ
            valid_moves = self.order_moves(
                current_position,
                visited
            )

            for next_position in valid_moves:
                # Chọn nước đi
                path.append(next_position)
                visited.add(next_position)

                # Tiếp tục tìm kiếm
                found = yield from backtrack()

                if found:
                    return True

                # Quay lui nếu nước đi không dẫn tới lời giải
                path.pop()
                visited.remove(next_position)

                # Gửi trạng thái quay lui cho giao diện
                yield path.copy(), visited_nodes, False

  
            return False

        found = yield from backtrack()

        # Không tìm được hành trình hoàn chỉnh
        if not found:
            yield best_path, visited_nodes, True