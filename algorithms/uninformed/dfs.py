from algorithms.uninformed.common import SearchBaseSolver

class DFSSolver(SearchBaseSolver):
    def solve(self):
        """Tìm kiếm theo chiều sâu (DFS) sử dụng Stack"""
        stack = [(self.start_pos, [self.start_pos])]
        visited_nodes_count = 0

        while stack:
            curr, path = stack.pop()
            visited_nodes_count += 1
            
            yield path, visited_nodes_count, False

            if len(path) == self.total_cells:
                yield path, visited_nodes_count, True
                return

            r, c = curr
            for dr, dc in self.knight_moves:
                nr, nc = r + dr, c + dc
                if self.is_valid_position(nr, nc, path):
                    stack.append(((nr, nc), path + [(nr, nc)]))
                    
        yield [], visited_nodes_count, False