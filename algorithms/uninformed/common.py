class SearchBaseSolver:
    def __init__(self, rows, cols, start_pos=(0, 0), obstacles=[]):
        self.rows = rows
        self.cols = cols
        self.start_pos = start_pos
        self.obstacles = set(obstacles)
        self.total_cells = (rows * cols) - len(self.obstacles)
        
        # 8 hướng di chuyển chuẩn chữ L của quân Mã
        self.knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), 
                             (1, -2), (1, 2), (2, -1), (2, 1)]

    def is_valid_position(self, r, c, visited):
        """Kiểm tra ô kế tiếp có hợp lệ để nhảy vào không"""
        return (0 <= r < self.rows and 
                0 <= c < self.cols and 
                (r, c) not in visited and 
                (r, c) not in self.obstacles)