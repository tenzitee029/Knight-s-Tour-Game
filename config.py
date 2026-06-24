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
LEVELS = {
    1: {"name": "Khởi Động (5x5)", "rows": 5, "cols": 5, "obstacles": []},
    2: {"name": "Tiêu Chuẩn (6x6)", "rows": 6, "cols": 6, "obstacles": []},
    3: {"name": "Đại Kiện Tướng (8x8)", "rows": 8, "cols": 8, "obstacles": []},
    4: {"name": "Mê Cung Số (10x10)", "rows": 10, "cols": 10, "obstacles": []},
    5: {"name": "Địa Hình Hiểm Trở", "rows": 8, "cols": 8, "obstacles": [(2,2), (2,5), (5,2), (5,5)]},
    6: {"name": "Bàn Cờ Khuyết Góc", "rows": 8, "cols": 8, "obstacles": [(0,0), (0,7), (7,0), (7,7)]}
}

ALGORITHMS = [
    "BFS (Uninformed)",
    "DFS (Uninformed)",
    "UCS (Uninformed)",
    "IDS (Uninformed)",
    "Backtracking (CSP)",
    "Forward Checking (CSP)",
    "AC3 (CSP)",
    "Min-Conflicts (CSP)"
]

AI_DELAY = 0.2
