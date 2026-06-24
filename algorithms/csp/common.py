class CSPBaseSolver:
    """Các hàm dùng chung cho nhóm thuật toán CSP."""

    KNIGHT_MOVES = [
        (-2, -1), (-2, 1),
        (-1, -2), (-1, 2),
        (1, -2), (1, 2),
        (2, -1), (2, 1)
    ]

    def __init__(
        self,
        rows,
        cols,
        start_pos=(0, 0),
        obstacles=None
    ):
        self.rows = rows
        self.cols = cols
        self.start_pos = start_pos
        self.obstacles = set(obstacles or [])
        self.total_cells = rows * cols - len(self.obstacles)

    def is_inside_board(self, position):
        row, col = position

        return (
            0 <= row < self.rows
            and 0 <= col < self.cols
        )

    def is_valid_position(self, position, visited):
        return (
            self.is_inside_board(position)
            and position not in self.obstacles
            and position not in visited
        )

    def get_valid_moves(self, position, visited):
        row, col = position
        valid_moves = []

        for delta_row, delta_col in self.KNIGHT_MOVES:
            next_position = (
                row + delta_row,
                col + delta_col
            )

            if self.is_valid_position(next_position, visited):
                valid_moves.append(next_position)

        return valid_moves

    def count_onward_moves(self, position, visited):
        temporary_visited = set(visited)
        temporary_visited.add(position)

        return len(
            self.get_valid_moves(
                position,
                temporary_visited
            )
        )

    def order_moves(self, position, visited):
        valid_moves = self.get_valid_moves(
            position,
            visited
        )

        valid_moves.sort(
            key=lambda next_position:
                self.count_onward_moves(
                    next_position,
                    visited
                )
        )

        return valid_moves