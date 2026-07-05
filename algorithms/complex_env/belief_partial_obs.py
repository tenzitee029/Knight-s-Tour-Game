import random
from typing import List, Optional, Generator

class PartialObservationBeliefSolver:
    """PARTIAL OBSERVATION - DFS + Backtracking + Warnsdorff"""
    
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

    def warnsdorff_score(self, pos: tuple, visited: set) -> int:
        return len(self.get_valid_moves(pos, visited | {pos}))

    def solve(self, initial_pos: Optional[tuple] = None, half: str = "left"):
        start_pos = initial_pos or self.default_start or self.get_random_start()
        visited_nodes_count = 0
        path = [start_pos]

        def dfs(current_path: List[tuple]):
            nonlocal visited_nodes_count
            visited_nodes_count += 1

            if visited_nodes_count % 5000 == 0 or len(current_path) % 5 == 0:
                print(f"Partial Obs ({half}) | Nodes: {visited_nodes_count:,} | Đường: {len(current_path)}/{self.total_cells}")

            yield current_path.copy(), visited_nodes_count, False

            if len(current_path) == self.total_cells:
                print(f"✅ Partial Observation ({half}) - Tìm thấy đường đi hoàn chỉnh!")
                yield current_path.copy(), visited_nodes_count, True
                return True

            current_pos = current_path[-1]
            visited_set = set(current_path)

            moves = self.get_valid_moves(current_pos, visited_set)
            
            # === PARTIAL OBSERVATION (nới lỏng hơn) ===
            mid = self.cols // 2
            if half == "left":
                # Cho phép đi sang phải một chút nếu đang ở biên
                moves = [m for m in moves if m[1] <= mid + 1]
            else:
                moves = [m for m in moves if m[1] >= mid - 1]

            moves.sort(key=lambda p: self.warnsdorff_score(p, visited_set))

            for next_pos in moves:
                current_path.append(next_pos)
                if (yield from dfs(current_path)):
                    return True
                current_path.pop()

            return False

        return dfs(path)