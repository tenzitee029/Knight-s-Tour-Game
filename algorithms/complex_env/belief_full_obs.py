from collections import deque
from algorithms.uninformed.common import SearchBaseSolver

class BeliefStateSolver(SearchBaseSolver):
    """1. Full Observation Solver
    Biết chính xác 100% vị trí quân Mã. Tập niềm tin luôn chỉ có 1 phần tử.
    """
    
    def get_valid_moves(self, pos: tuple[int, int]) -> list[tuple[int, int]]:
        x, y = pos
        knight_moves = [
            (x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1),
            (x + 1, y + 2), (x + 1, y - 2), (x - 1, y + 2), (x - 1, y - 2)
        ]
        return [(nx, ny) for nx, ny in knight_moves if 0 <= nx < self.rows and 0 <= ny < self.cols]

    def solve(self):
        visited_nodes_count = 0
        start_belief = frozenset([self.start_pos])
        
        queue = deque([(start_belief, [self.start_pos])])
        visited_beliefs = {start_belief}

        while queue:
            curr_belief, path = queue.popleft()
            visited_nodes_count += 1
            
            curr_pos = next(iter(curr_belief))
            yield path, visited_nodes_count, False

            if len(path) == self.rows * self.cols:
                yield path, visited_nodes_count, True
                return

            for next_pos in self.get_valid_moves(curr_pos):
                if next_pos not in path:
                    next_belief = frozenset([next_pos])
                    if next_belief not in visited_beliefs:
                        visited_beliefs.add(next_belief)
                        queue.append((next_belief, path + [next_pos]))

        yield [], visited_nodes_count, False