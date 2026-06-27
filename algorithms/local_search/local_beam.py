class LocalBeamSolver:
    def __init__(self, rows, cols, start_pos, obstacles=None, beam_width=3):
        self.rows = rows
        self.cols = cols
        self.start_pos = start_pos
        self.obstacles = obstacles if obstacles else []
        self.beam_width = beam_width
        self.moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
        self.total_cells = (rows * cols) - len(self.obstacles)

    def is_valid_move(self, r, c, visited):
        return 0 <= r < self.rows and 0 <= c < self.cols and (r, c) not in visited and (r, c) not in self.obstacles

    def get_valid_moves(self, current_pos, visited):
        r, c = current_pos
        return [(r + dr, c + dc) for dr, dc in self.moves if self.is_valid_move(r + dr, c + dc, visited)]

    def heuristic(self, pos, visited):
        return len(self.get_valid_moves(pos, visited)) # Warnsdorff Rule

    def solve(self):
        beams = [(self.start_pos, [self.start_pos])]
        visited_nodes_count = 1

        yield [self.start_pos], visited_nodes_count, False

        while beams:

            next_states = []

            for current_pos, visited in beams:

                if len(visited) == self.total_cells:
                    yield visited.copy(), visited_nodes_count, True
                    return

                for move in self.get_valid_moves(current_pos, visited):
                    new_visited = visited.copy()
                    new_visited.append(move)

                    score = self.heuristic(move, new_visited)

                    next_states.append((score, move, new_visited))
                    visited_nodes_count += 1

            if not next_states:
                if beams:
                    yield beams[0][1].copy(), visited_nodes_count, False
                return

            next_states.sort(key=lambda x: x[0])

            beams = [(state[1], state[2]) for state in next_states[:self.beam_width]]

            yield beams[0][1].copy(), visited_nodes_count, False

        yield [], visited_nodes_count, False