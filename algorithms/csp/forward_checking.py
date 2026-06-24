from .common import CSPBaseSolver


class ForwardCheckingSolver(CSPBaseSolver):
    """Giải Knight's Tour bằng Forward Checking."""

    def has_future_move(self, position, visited, path_length):
        # Nếu đây là ô cuối cùng cần đi thì không cần nước tiếp theo
        if path_length == self.total_cells:
            return True

        future_moves = self.get_valid_moves(
            position,
            visited
        )

        return len(future_moves) > 0

    def forward_check(self, position, visited, path_length):
        """
        Kiểm tra trước miền giá trị của bước tiếp theo.

        False: nước vừa chọn làm quân mã hết đường quá sớm.
        True: vẫn còn ít nhất một nước đi tiếp theo.
        """
        return self.has_future_move(
            position,
            visited,
            path_length
        )

    def solve(self):
        path = [self.start_pos]
        visited = {self.start_pos}

        visited_nodes = 0
        best_path = path.copy()

        def backtrack_with_forward_checking():
            nonlocal visited_nodes
            nonlocal best_path

            visited_nodes += 1

            if len(path) > len(best_path):
                best_path = path.copy()

            # Gửi trạng thái hiện tại cho giao diện
            yield path.copy(), visited_nodes, False

            # Đã đi qua toàn bộ ô hợp lệ
            if len(path) == self.total_cells:
                yield path.copy(), visited_nodes, True
                return True



            current_position = path[-1]

            valid_moves = self.order_moves(
                current_position,
                visited
            )

            for next_position in valid_moves:
                # Thử gán nước đi mới
                path.append(next_position)
                visited.add(next_position)

                # Kiểm tra trước miền của bước tiếp theo
                is_safe = self.forward_check(
                    next_position,
                    visited,
                    len(path)
                )

                if is_safe:
                    found = yield from (
                        backtrack_with_forward_checking()
                    )

                    if found:
                        return True

                # Nước đi không phù hợp hoặc không có lời giải
                path.pop()
                visited.remove(next_position)

                # Hiển thị bước quay lui
                yield path.copy(), visited_nodes, False



            return False

        found = yield from backtrack_with_forward_checking()

        if not found:
            yield best_path, visited_nodes, True