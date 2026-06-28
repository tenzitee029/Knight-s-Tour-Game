import random

class BeliefStateSolver:
    def __init__(self, rows, cols, start_pos, obstacles=None, observation_mode='full', partial_rate=0.5):
        self.rows = rows
        self.cols = cols
        self.start_pos = start_pos
        self.obstacles = obstacles if obstacles else []
        self.moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
        self.total_cells = (rows * cols) - len(self.obstacles)
        
        # Chế độ quan sát: 'full', 'partial', 'none'
        self.observation_mode = observation_mode
        # Xác suất nhìn thấy một nước đi tiếp theo trong chế độ 'partial' (0.0 đến 1.0)
        self.partial_rate = partial_rate

    def is_valid(self, r, c, visited):
        return (0 <= r < self.rows and 0 <= c < self.cols and 
                (r, c) not in visited and (r, c) not in self.obstacles)

    def get_valid_moves(self, pos, visited):
        r, c = pos
        return [(r + dr, c + dc) for dr, dc in self.moves if self.is_valid(r + dr, c + dc, visited)]

    def solve(self):
        visited = [self.start_pos]
        current_pos = self.start_pos
        # Bỏ visited_nodes_count ở yield, thay bằng self.obstacles

        yield visited.copy(), self.obstacles, False

        while len(visited) < self.total_cells:
            possible_moves = self.get_valid_moves(current_pos, visited)

            if not possible_moves:
                yield visited.copy(), self.obstacles, True # Hết đường -> Game Over
                return

            scored_beliefs = []

            for move in possible_moves:
                # 1. Chế độ No Observation
                if self.observation_mode == 'none':
                    score = random.random()
                
                # 2. Chế độ Full hoặc Partial Observation
                else:
                    next_choices = self.get_valid_moves(move, visited + [move])

                    if self.observation_mode == 'partial':
                        observed_choices = [
                            c for c in next_choices 
                            if random.random() < self.partial_rate
                        ]
                        next_choices_count = len(observed_choices)
                    else:
                        next_choices_count = len(next_choices)

                    if next_choices_count == 0 and len(visited) + 1 < self.total_cells:
                        score = 999
                    else:
                        score = next_choices_count

                scored_beliefs.append((score, move))

            scored_beliefs.sort(key=lambda x: x[0])
            best_move = scored_beliefs[0][1]

            visited.append(best_move)
            current_pos = best_move

            if len(visited) == self.total_cells:
                yield visited.copy(), self.obstacles, True # Chiến thắng -> Game Over
                return

            yield visited.copy(), self.obstacles, False

        yield visited.copy(), self.obstacles, True