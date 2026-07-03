import random
from collections import deque
from typing import Optional   # ← Thêm dòng này

class NoObservationBeliefSolver:
    """NO OBSERVATION - Không biết vị trí. Random start mỗi lần."""
    
    def __init__(self, rows: int, cols: int, start_pos=None, obstacles=None):
        self.rows = rows
        self.cols = cols
        self.default_start = start_pos
        self.obstacles = set(obstacles) if obstacles else set()
        self.total_cells = rows * cols - len(self.obstacles)

    def get_valid_moves(self, pos: tuple, visited: set) -> list:
        x, y = pos
        moves = [(x+2,y+1),(x+2,y-1),(x-2,y+1),(x-2,y-1),
                 (x+1,y+2),(x+1,y-2),(x-1,y+2),(x-1,y-2)]
        return [(nx, ny) for nx, ny in moves 
                if 0 <= nx < self.rows and 0 <= ny < self.cols 
                and (nx, ny) not in visited and (nx, ny) not in self.obstacles]

    def get_random_start(self) -> tuple:
        valid_pos = [(r, c) for r in range(self.rows) for c in range(self.cols) 
                    if (r, c) not in self.obstacles]
        return random.choice(valid_pos)

    def solve(self, initial_pos: Optional[tuple] = None):
        visited_nodes_count = 0
        
        # Ưu tiên random nếu start_pos là None
        if initial_pos is None and self.default_start is None:
            start_pos = self.get_random_start()
        else:
            start_pos = initial_pos or self.default_start or self.get_random_start()
        
        belief = frozenset([start_pos])
        queue = deque([(belief, [start_pos])])
        visited_beliefs = {belief}

        while queue:
            curr_belief, path = queue.popleft()
            visited_nodes_count += 1
            yield path, visited_nodes_count, False

            if len(path) == self.total_cells:
                yield path, visited_nodes_count, True
                return

            curr_pos = next(iter(curr_belief))
            visited_set = set(path)

            for next_pos in self.get_valid_moves(curr_pos, visited_set):
                next_belief = frozenset([next_pos])
                if next_belief not in visited_beliefs:
                    visited_beliefs.add(next_belief)
                    queue.append((next_belief, path + [next_pos]))

        yield [], visited_nodes_count, False