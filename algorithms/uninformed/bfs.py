from collections import deque
from algorithms.uninformed.common import SearchBaseSolver

class BFSSolver(SearchBaseSolver):
    def solve(self):
        """Tìm kiếm theo chiều rộng (BFS) sử dụng Queue"""
        queue = deque([(self.start_pos, [self.start_pos])])
        visited_nodes_count = 0

        while queue:
            curr, path = queue.popleft()
            visited_nodes_count += 1
            
            # Trả trạng thái về cho UI vẽ đồ họa
            yield path, visited_nodes_count, False

            if len(path) == self.total_cells:
                yield path, visited_nodes_count, True
                return

            r, c = curr
            for dr, dc in self.knight_moves:
                nr, nc = r + dr, c + dc
                if self.is_valid_position(nr, nc, path):
                    queue.append(((nr, nc), path + [(nr, nc)]))
                    
        yield [], visited_nodes_count, False