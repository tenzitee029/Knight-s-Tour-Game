import random
from collections import deque
from typing import Optional

class PartialObservationBeliefSolver:
    """PARTIAL OBSERVATION - Chỉ biết một nửa bàn cờ. Random start mỗi lần."""
    
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

    def solve(self, half: str = "left"):
        """half: 'left' hoặc 'right'"""
        visited_nodes_count = 0
        start_pos = self.default_start or self.get_random_start()
        
        mid = self.cols // 2
        initial_belief = frozenset(
            (i, j) for i in range(self.rows) for j in range(self.cols)
            if (i, j) not in self.obstacles and 
            ((half == "left" and j < mid) or (half == "right" and j >= mid))
        )
        
        queue = deque([(initial_belief, [start_pos])])
        visited_beliefs = {initial_belief}

        while queue:
            curr_belief, path = queue.popleft()
            visited_nodes_count += 1
            yield path, visited_nodes_count, False

            if len(path) == self.total_cells:
                yield path, visited_nodes_count, True
                return

            visited_set = set(path)
            possible_next = {npos for pos in curr_belief 
                           for npos in self.get_valid_moves(pos, visited_set)}

            for next_pos in possible_next:
                next_belief = frozenset(
                    npos for pos in curr_belief 
                    for npos in self.get_valid_moves(pos, visited_set)
                )
                if next_belief and next_belief not in visited_beliefs:
                    visited_beliefs.add(next_belief)
                    queue.append((next_belief, path + [next_pos]))

        yield [], visited_nodes_count, False