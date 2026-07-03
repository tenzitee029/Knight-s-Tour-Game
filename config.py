# config.py - Cấu hình chung cho dự án Knight's Tour

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

# Cấu hình Level
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

# Danh sách thuật toán
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
    "Random Restart Hill Climbing (Local Search)",
    "Backtracking (CSP)",
    "Forward Checking (CSP)",
    "AC3 (CSP)",
    "Min-Conflicts (CSP)",
    "Minimax (Adversarial)",
    "Expectimax (Adversarial)",
    "Alpha-Beta Pruning (Adversarial)",
    "Local Beam Search (Local Search)",
    "Belief State No Observation (Complex Environments)",
    "Belief State Partial Observation (Complex Environments)",
    "Belief State Full Observation (Complex Environments)",
    "AND-OR Graph Search (Complex Environments)"
]

AI_DELAY = 0.2