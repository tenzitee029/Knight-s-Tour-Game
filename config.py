import pygame

# Kích thước màn hình
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# Màu sắc (RGB)
COLOR_BG = (240, 244, 248)       # Màu nền chính nhẹ nhàng
COLOR_SIDEBAR = (255, 255, 255)  # Màu nền thanh thông số
COLOR_TEXT = (33, 37, 41)
COLOR_TEXT_MUTED = (108, 117, 125)

COLOR_CELL_LIGHT = (235, 235, 208)
COLOR_CELL_DARK = (119, 149, 86)
COLOR_PATH = (255, 69, 0)        # Màu đường đi của Mã (Orange Red)
COLOR_VISITED = (100, 149, 237)   # Ô đã duyệt qua (Cornflower Blue)
COLOR_CURRENT = (255, 215, 0)     # Vị trí hiện tại của Mã (Gold)

# Cấu hình Level (Kích thước, Tên, Vật cản nếu có)
# Cấu hình Level (Rút gọn từ 6 xuống còn 3 màn chơi)
LEVELS = {
    1: {
        "name": "Khởi Động (5x5)", 
        "rows": 5, 
        "cols": 5, 
        "obstacles": []
    },
    2: {
        "name": "Tiêu Chuẩn (6x6)", 
        "rows": 6, 
        "cols": 6, 
        "obstacles": []
    },
    3: {
        "name": "Thử Thách (6x6 - Vật Cản)", 
        "rows": 6, 
        "cols": 6, 
        "obstacles": [(1, 1), (1, 4), (4, 1), (4, 4)] 
    }
}

ALGORITHMS = [
    "BFS (Uninformed)",
    "DFS (Uninformed)",
    "UCS (Uninformed)",
    "IDS (Uninformed)",
    "GBFS (Informed)",
    "A* (Informed)",
    "IDA* (Informed)",
    "Simple Hill Climbing (Local Search)",
    "Stochastic Hill Climbing (Local Search)",
    "Backtracking (CSP)",
    "Forward Checking (CSP)",
    "AC3 (CSP)",
    "Min-Conflicts (CSP)",
    "Minimax (Adversarial)",
    "Expectimax (Adversarial)"
]

AI_DELAY = 0.2
