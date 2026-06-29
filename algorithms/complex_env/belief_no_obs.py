from collections import deque
from algorithms.uninformed.common import SearchBaseSolver

class BeliefStateSolver(SearchBaseSolver):
    """3. No Observation Solver (Sensorless)
    Mù hoàn toàn, hoàn toàn không có bước Filtering. 
    Thuật toán phải tự tìm chuỗi hành động ép tập niềm tin co cụm lại dần.
    """
    
    def __init__(self, rows, cols, start_pos=(0, 0), obstacles=[]):
        super().__init__(rows, cols, start_pos, obstacles)
        self.actions = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

    def solve(self):
        visited_nodes_count = 0
        
        # Ban đầu mù hoàn toàn: Phân vân giữa vị trí xuất phát và tất cả các ô xung quanh nó
        x, y = self.start_pos
        initial_set = {self.start_pos}
        for dx, dy in self.actions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                initial_set.add((nx, ny))
                
        start_belief = frozenset(initial_set)
        queue = deque([(start_belief, [self.start_pos])])
        visited_beliefs = {start_belief}

        while queue:
            curr_belief, path = queue.popleft()
            visited_nodes_count += 1
            
            yield path, visited_nodes_count, False
            
            # Thắng khi đi hết bàn cờ và kích thước tập niềm tin tự co về bằng 1 duy nhất (Hội tụ thành công)
            if len(path) == self.rows * self.cols and len(curr_belief) == 1:
                yield path, visited_nodes_count, True
                return

            curr_actual = path[-1]

            for dx, dy in self.actions:
                # CHỈ CÓ PREDICTION (Không có Filtering vì không có Sensor)
                next_set = set()
                for (px, py) in curr_belief:
                    nx, ny = px + dx, py + dy
                    # Các trạng thái vật lý nào đập vào tường hoặc ô đã đi thì bị loại bỏ (hiệu ứng co cụm)
                    if 0 <= nx < self.rows and 0 <= ny < self.cols and (nx, ny) not in path:
                        next_set.add((nx, ny))
                
                if not next_set:
                    continue
                    
                actual_next = (curr_actual[0] + dx, curr_actual[1] + dy)
                if actual_next not in next_set:
                    continue

                next_belief = frozenset(next_set)
                if next_belief not in visited_beliefs:
                    visited_beliefs.add(next_belief)
                    queue.append((next_belief, path + [actual_next]))

        yield [], visited_nodes_count, False