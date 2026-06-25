class AdversarialBaseSolver:
    """Các hàm dùng chung cho nhóm Adversarial Search."""

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

        # Vật cản có sẵn của màn chơi
        self.static_obstacles = set(obstacles or [])

        # Vật cản do AI MIN tạo ra
        self.dynamic_obstacles = set()

        self.total_cells = (
            rows * cols - len(self.static_obstacles)
        )

    def is_inside_board(self, position):
        row, col = position

        return (
            0 <= row < self.rows
            and 0 <= col < self.cols
        )

    def is_valid_position(
        self,
        position,
        path,
        dynamic_obstacles=None
    ):
        blocked = (
            self.dynamic_obstacles
            if dynamic_obstacles is None
            else dynamic_obstacles
        )

        return (
            self.is_inside_board(position)
            and position not in path
            and position not in self.static_obstacles
            and position not in blocked
        )

    def get_valid_moves(
        self,
        position,
        path,
        dynamic_obstacles=None
    ):
        row, col = position
        valid_moves = []

        for delta_row, delta_col in self.KNIGHT_MOVES:
            next_position = (
                row + delta_row,
                col + delta_col
            )

            if self.is_valid_position(
                next_position,
                path,
                dynamic_obstacles
            ):
                valid_moves.append(next_position)

        return valid_moves

    def get_lock_candidates(
        self,
        path,
        dynamic_obstacles
    ):
        """
        Các ô mà AI MIN được phép khóa.
        Không được khóa ô đã đi hoặc vật cản đã tồn tại.
        """
        candidates = []

        for row in range(self.rows):
            for col in range(self.cols):
                position = (row, col)

                if (
                    position not in path
                    and position not in self.static_obstacles
                    and position not in dynamic_obstacles
                ):
                    candidates.append(position)

        return candidates

    def evaluate_state(
        self,
        path,
        dynamic_obstacles
    ):
        """
        MAX muốn điểm cao.
        MIN muốn điểm thấp.
        """
        current_position = path[-1]

        valid_moves = self.get_valid_moves(
            current_position,
            path,
            dynamic_obstacles
        )

        return (
            len(path) * 100
            + len(valid_moves) * 10
            - len(dynamic_obstacles) * 5
        )