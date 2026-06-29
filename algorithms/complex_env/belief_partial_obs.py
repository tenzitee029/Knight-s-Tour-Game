from collections import deque
from algorithms.uninformed.common import SearchBaseSolver

class BeliefStateSolver(SearchBaseSolver):
    """2. Partial Observation Solver
    Hành động dựa trên 8 hướng nhảy (offsets). Cảm biến trả về khoảng cách 
    Manhattan tới đích để lọc (Filter) và thu hẹp vùng nghi vấn.
    """
    
    def __init__(self, rows, cols, start_pos=(0, 0), obstacles=[]):
        super().__init__(rows, cols, start_pos, obstacles)
        # 8 hành động nhảy mẫu của quân Mã
        self.actions = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

    def sensor_feedback(self, pos: tuple[int, int]) -> int:
        """Giả lập cảm biến: Trả về khoảng cách Manhattan tới ô góc (0,0)."""
        return abs(pos[0]) + abs(pos[1])

    def solve(self):
        visited_nodes_count = 0
        
        # Giả định ban đầu bị nhiễu: Có thể ở start_pos hoặc các ô lân cận hợp lệ
        x, y = self.start_pos
        initial_set = {self.start_pos}
        for dx, dy in self.actions[:2]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                initial_set.add((nx, ny))
                
        start_belief = frozenset(initial_set)
        # Queue chứa: (Tập_niềm_tin, Đường_đi_thực_tế_quân_mã)
        queue = deque([(start_belief, [self.start_pos])])
        visited_beliefs = {start_belief}

        while queue:
            curr_belief, path = queue.popleft()
            visited_nodes_count += 1
            
            yield path, visited_nodes_count, False
            
            # Điều kiện thắng: Đi hết bàn cờ VÀ không gian niềm tin đã hội tụ hoàn toàn về 1 trạng thái
            if len(path) == self.rows * self.cols and len(curr_belief) == 1:
                yield path, visited_nodes_count, True
                return

            curr_actual = path[-1]

            # Thử áp dụng 8 hành động nhảy quân Mã lên toàn bộ các trạng thái trong Belief hiện tại
            for dx, dy in self.actions:
                # BƯỚC 1: PREDICTION (Tiên đoán các vị trí mới có thể đạt tới)
                predicted_set = set()
                for (px, py) in curr_belief:
                    nx, ny = px + dx, py + dy
                    if 0 <= nx < self.rows and 0 <= ny < self.cols and (nx, ny) not in path:
                        predicted_set.add((nx, ny))
                
                if not predicted_set:
                    continue
                
                # Kiểm tra xem nước đi này có hợp lệ với vị trí thực tế không
                actual_next = (curr_actual[0] + dx, curr_actual[1] + dy)
                if actual_next not in predicted_set:
                    continue

                # BƯỚC 2: FILTERING (Dùng Sensor ở vị trí thực tế để lọc loại bỏ các ô sai trong tập tiên đoán)
                actual_feedback = self.sensor_feedback(actual_next)
                filtered_set = {pos for pos in predicted_set if self.sensor_feedback(pos) == actual_feedback}
                
                next_belief = frozenset(filtered_set)
                if next_belief not in visited_beliefs:
                    visited_beliefs.add(next_belief)
                    queue.append((next_belief, path + [actual_next]))

        yield [], visited_nodes_count, False