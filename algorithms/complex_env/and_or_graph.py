from typing import List, Tuple, Optional, Set

class AndOrGraphSolver:
    """And-Or Graph Search cho Knight's Tour"""
    
    def __init__(self, rows: int, cols: int, start_pos: tuple, obstacles=None):
        self.rows = rows
        self.cols = cols
        self.start_pos = start_pos
        self.obstacles = set(obstacles) if obstacles else set()
        self.total_cells = rows * cols - len(self.obstacles)
        self.moves = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]

    def get_valid_moves(self, pos: tuple, visited: set) -> list[tuple]:
        r, c = pos
        valid = []
        for dr, dc in self.moves:
            nr, nc = r + dr, c + dc
            if (0 <= nr < self.rows and 0 <= nc < self.cols and 
                (nr, nc) not in visited and (nr, nc) not in self.obstacles):
                valid.append((nr, nc))
        return valid

    def solve(self):
        visited: List[tuple] = [self.start_pos]
        visited_set: Set[tuple] = {self.start_pos}
        current_pos = self.start_pos
        visited_nodes_count = 1

        yield visited.copy(), visited_nodes_count, False

        while len(visited) < self.total_cells:
            or_nodes = self.get_valid_moves(current_pos, visited_set)

            if not or_nodes:
                yield visited.copy(), visited_nodes_count, False
                return

            best_move = None
            best_score = -1

            for move in or_nodes:
                temp_visited = visited_set | {move}
                contingency = self.get_valid_moves(move, temp_visited)
                score = len(contingency)

                if len(visited) + 1 == self.total_cells:
                    best_move = move
                    break
                if score > best_score:
                    best_score = score
                    best_move = move

            if best_move is None:
                best_move = or_nodes[0]

            visited.append(best_move)
            visited_set.add(best_move)
            current_pos = best_move
            visited_nodes_count += 1

            yield visited.copy(), visited_nodes_count, False

        yield visited.copy(), visited_nodes_count, True