import random

from .common import CSPBaseSolver


class MinConflictsSolver(CSPBaseSolver):
    """Giải Knight's Tour bằng Min-Conflicts."""
    MAX_NODES = 50000


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

    def get_available_cells(self):
        cells = []

        for row in range(self.rows):
            for col in range(self.cols):
                position = (row, col)

                if position not in self.obstacles:
                    cells.append(position)

        return cells

    def create_random_assignment(self):
        """
        Tạo một phương án đầy đủ.

        Vị trí bắt đầu luôn được giữ ở phần tử đầu tiên.
        Các ô còn lại được xáo trộn ngẫu nhiên.
        """
        remaining_cells = [
            position
            for position in self.get_available_cells()
            if position != self.start_pos
        ]

        random.shuffle(remaining_cells)

        return [self.start_pos] + remaining_cells

    def get_conflicted_indexes(self, assignment):
        """
        Tìm các bước không tạo thành nước đi quân mã hợp lệ
        với bước ngay trước hoặc ngay sau nó.
        """
        conflicted_indexes = set()

        for index in range(len(assignment) - 1):
            current_position = assignment[index]
            next_position = assignment[index + 1]

            if not self.is_knight_move(
                current_position,
                next_position
            ):
                conflicted_indexes.add(index)
                conflicted_indexes.add(index + 1)

        # Không được thay đổi vị trí xuất phát
        conflicted_indexes.discard(0)

        return list(conflicted_indexes)

    def count_conflicts(self, assignment):
        conflict_count = 0

        for index in range(len(assignment) - 1):
            if not self.is_knight_move(
                assignment[index],
                assignment[index + 1]
            ):
                conflict_count += 1

        return conflict_count

    def get_valid_prefix(self, assignment):
        """
        Lấy phần đầu đường đi vẫn còn hợp lệ để giao diện vẽ.

        Nếu phương án còn xung đột thì không được báo toàn bộ
        đường đi là thành công.
        """
        valid_path = [assignment[0]]

        for index in range(1, len(assignment)):
            if self.is_knight_move(
                assignment[index - 1],
                assignment[index]
            ):
                valid_path.append(assignment[index])
            else:
                break

        return valid_path

    def find_best_swap(self, assignment, conflicted_index):
        """
        Thử đổi vị trí đang xung đột với các vị trí khác,
        sau đó chọn phép đổi tạo ít xung đột nhất.
        """
        best_indexes = []
        minimum_conflicts = None

        for other_index in range(1, len(assignment)):
            if other_index == conflicted_index:
                continue

            assignment[conflicted_index], assignment[other_index] = (
                assignment[other_index],
                assignment[conflicted_index]
            )

            conflict_count = self.count_conflicts(assignment)

            assignment[conflicted_index], assignment[other_index] = (
                assignment[other_index],
                assignment[conflicted_index]
            )

            if (
                minimum_conflicts is None
                or conflict_count < minimum_conflicts
            ):
                minimum_conflicts = conflict_count
                best_indexes = [other_index]

            elif conflict_count == minimum_conflicts:
                best_indexes.append(other_index)

        if not best_indexes:
            return None

        return random.choice(best_indexes)
    def solve(self):
        visited_nodes = 0
        best_path = [self.start_pos]

        while visited_nodes < self.MAX_NODES:
            assignment = self.create_random_assignment()

            while visited_nodes < self.MAX_NODES:
                visited_nodes += 1

                conflict_count = self.count_conflicts(
                    assignment
                )

                valid_path = self.get_valid_prefix(
                    assignment
                )

                if len(valid_path) > len(best_path):
                    best_path = valid_path.copy()

                yield valid_path, visited_nodes, False

                if conflict_count == 0:
                    yield assignment.copy(), visited_nodes, True
                    return

                conflicted_indexes = (
                    self.get_conflicted_indexes(assignment)
                )

                if not conflicted_indexes:
                    break

                conflicted_index = random.choice(
                    conflicted_indexes
                )

                swap_index = self.find_best_swap(
                    assignment,
                    conflicted_index
                )

                if swap_index is None:
                    break

                assignment[conflicted_index], assignment[swap_index] = (
                    assignment[swap_index],
                    assignment[conflicted_index]
                )

        yield best_path, visited_nodes, True
