from collections import deque

from .common import CSPBaseSolver


class AC3Solver(CSPBaseSolver):
    """Giải Knight's Tour bằng Backtracking kết hợp AC-3."""

    def is_knight_move(self, first_position, second_position):
        first_row, first_col = first_position
        second_row, second_col = second_position

        row_difference = abs(first_row - second_row)
        col_difference = abs(first_col - second_col)

        return (
            (row_difference == 2 and col_difference == 1)
            or
            (row_difference == 1 and col_difference == 2)
        )

    def get_available_cells(self, visited):
        available_cells = set()

        for row in range(self.rows):
            for col in range(self.cols):
                position = (row, col)

                if (
                    position not in self.obstacles
                    and position not in visited
                ):
                    available_cells.add(position)

        return available_cells

    def create_domains(self, path, visited):
        """
        Mỗi bước trong hành trình là một biến CSP.

        Các bước đã đi có miền chỉ gồm một vị trí.
        Các bước chưa đi có miền gồm các ô còn trống.
        """
        domains = {}
        available_cells = self.get_available_cells(visited)

        for step in range(self.total_cells):
            if step < len(path):
                domains[step] = {path[step]}
            else:
                domains[step] = set(available_cells)

        return domains

    def satisfies_constraint(
        self,
        first_step,
        first_position,
        second_step,
        second_position
    ):
        # Hai bước không được nằm trên cùng một ô
        if first_position == second_position:
            return False

        # Hai bước liên tiếp phải là một nước đi quân mã
        if abs(first_step - second_step) == 1:
            return self.is_knight_move(
                first_position,
                second_position
            )

        return True

    def revise(self, domains, first_step, second_step):
        """
        Loại giá trị trong miền của first_step nếu không có
        giá trị phù hợp trong miền của second_step.
        """
        revised = False
        values_to_remove = set()

        for first_position in domains[first_step]:
            has_support = False

            for second_position in domains[second_step]:
                if self.satisfies_constraint(
                    first_step,
                    first_position,
                    second_step,
                    second_position
                ):
                    has_support = True
                    break

            if not has_support:
                values_to_remove.add(first_position)

        if values_to_remove:
            domains[first_step] -= values_to_remove
            revised = True

        return revised

    def create_arc_queue(self):
        """
        Tạo các cung giữa những biến có ràng buộc.

        Mọi bước khác nhau có ràng buộc không trùng ô.
        Hai bước liên tiếp còn có ràng buộc nước đi quân mã.
        """
        queue = deque()

        for first_step in range(self.total_cells):
            for second_step in range(self.total_cells):
                if first_step != second_step:
                    queue.append(
                        (first_step, second_step)
                    )

        return queue

    def apply_ac3(self, domains):
        queue = self.create_arc_queue()

        while queue:
            first_step, second_step = queue.popleft()

            if self.revise(
                domains,
                first_step,
                second_step
            ):
                # Miền rỗng nghĩa là trạng thái không hợp lệ
                if not domains[first_step]:
                    return False

                # Kiểm tra lại các cung liên quan
                for other_step in range(self.total_cells):
                    if (
                        other_step != first_step
                        and other_step != second_step
                    ):
                        queue.append(
                            (other_step, first_step)
                        )

        return True

    def solve(self):
        path = [self.start_pos]
        visited = {self.start_pos}

        visited_nodes = 0
        best_path = path.copy()

        def backtrack_with_ac3():
            nonlocal visited_nodes
            nonlocal best_path

            visited_nodes += 1

            if len(path) > len(best_path):
                best_path = path.copy()

            yield path.copy(), visited_nodes, False

            if len(path) == self.total_cells:
                yield path.copy(), visited_nodes, True
                return True



            current_position = path[-1]

            valid_moves = self.order_moves(
                current_position,
                visited
            )

            for next_position in valid_moves:
                path.append(next_position)
                visited.add(next_position)

                # Tạo miền và chạy AC-3 sau khi thử nước đi
                domains = self.create_domains(
                    path,
                    visited
                )

                is_consistent = self.apply_ac3(domains)

                if is_consistent:
                    found = yield from backtrack_with_ac3()

                    if found:
                        return True

                # AC-3 phát hiện miền rỗng hoặc nhánh thất bại
                path.pop()
                visited.remove(next_position)

                yield path.copy(), visited_nodes, False



            return False

        found = yield from backtrack_with_ac3()

        if not found:
            yield best_path, visited_nodes, True