class BeliefStateSolver:
    def __init__(self, rows, cols, start_pos, obstacles=None):
        self.rows = rows
        self.cols = cols
        self.start_pos = start_pos
        self.obstacles = obstacles if obstacles else []
        self.moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
        self.total_cells = (rows * cols) - len(self.obstacles)

    def is_valid(self, r, c, visited):
        return (0 <= r < self.rows and 0 <= c < self.cols and 
                (r, c) not in visited and (r, c) not in self.obstacles)

    def get_valid_moves(self, pos, visited):
        r, c = pos
        return [(r + dr, c + dc) for dr, dc in self.moves if self.is_valid(r + dr, c + dc, visited)]

    def solve(self):
        visited = [self.start_pos]
        current_pos = self.start_pos
        visited_nodes_count = 1

        yield visited.copy(), visited_nodes_count, False

        while len(visited) < self.total_cells:
            possible_moves = self.get_valid_moves(current_pos, visited)

            if not possible_moves:
                yield visited.copy(), visited_nodes_count, False
                return

            scored_beliefs = []

            for move in possible_moves:
                next_choices = self.get_valid_moves(move, visited + [move])

                if len(next_choices) == 0 and len(visited) + 1 < self.total_cells:
                    score = 999
                else:
                    score = len(next_choices)

                scored_beliefs.append((score, move))

            scored_beliefs.sort(key=lambda x: x[0])
            best_move = scored_beliefs[0][1]

            visited.append(best_move)
            current_pos = best_move
            visited_nodes_count += 1

            if len(visited) == self.total_cells:
                yield visited.copy(), visited_nodes_count, True
                return

            yield visited.copy(), visited_nodes_count, False

        yield visited.copy(), visited_nodes_count, False