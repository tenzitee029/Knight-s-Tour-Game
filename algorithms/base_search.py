class KnightTourSolver:
    def __init__(self, rows, cols, start_pos=(0, 0), obstacles=[]):
        self.rows = rows
        self.cols = cols
        self.start_pos = start_pos
        self.obstacles = set(obstacles)
        self.total_cells = (rows * cols) - len(self.obstacles)
        
        # 8 hướng di chuyển chuẩn chữ L của quân Mã
        self.moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

    def is_valid(self, r, c, visited):
        return (0 <= r < self.rows and 
                0 <= c < self.cols and 
                (r, c) not in visited and 
                (r, c) not in self.obstacles)

    def solve_dfs(self):
        """Demo Tìm kiếm Khám phá đường đi bằng Stack (Hành trình mở)"""
        # Trạng thái: (vị trí_hiện_tại, danh_sách_đường_đi)
        stack = [(self.start_pos, [self.start_pos])]
        visited_nodes_count = 0

        while stack:
            curr, path = stack.pop()
            visited_nodes_count += 1
            
            # Trả trạng thái về cho UI vẽ đồ họa
            yield path, visited_nodes_count, False

            if len(path) == self.total_cells:
                yield path, visited_nodes_count, True
                return

            # Tìm các bước đi kế tiếp tiếp theo
            r, c = curr
            for dr, dc in self.moves:
                nr, nc = r + dr, c + dc
                if self.is_valid(nr, nc, path):
                    stack.append(((nr, nc), path + [(nr, nc)]))
                    
        yield [], visited_nodes_count, False  # Thất bại không tìm thấy đường

    def solve_bfs(self):
        """Demo Tìm kiếm bằng Queue (BFS tìm ra lời giải ngắn nhất cho các ô đầu)"""
        from collections import deque
        queue = deque([(self.start_pos, [self.start_pos])])
        visited_nodes_count = 0

        while queue:
            curr, path = queue.popleft()
            visited_nodes_count += 1
            
            yield path, visited_nodes_count, False

            if len(path) == self.total_cells:
                yield path, visited_nodes_count, True
                return

            r, c = curr
            for dr, dc in self.moves:
                nr, nc = r + dr, c + dc
                if self.is_valid(nr, nc, path):
                    queue.append(((nr, nc), path + [(nr, nc)]))
                    
        yield [], visited_nodes_count, False