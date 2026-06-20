import pygame
import time
import random  # Thêm thư viện random
from pathlib import Path
from config import *
from algorithms.base_search import KnightTourSolver
from storage.database import save_match

class Gameplay:
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont("Times New Roman", 18)
        self.font_bold = pygame.font.SysFont("Times New Roman", 22, bold=True)
        self.font_icon = pygame.font.SysFont("Times New Roman", 32, bold=True)
        self.knight_img = self.load_knight_image()
        
        self.board_rect = pygame.Rect(40, 60, 550, 550)
        self.btn_back = pygame.Rect(840, 620, 120, 40)
        
        self.reset_state()

    def reset_state(self):
        self.path = []
        self.visited_nodes = 0
        self.start_time = None
        self.elapsed_time = 0.0
        self.is_finished = False
        self.success = False
        self.solver_generator = None
        self.show_popup = False
        self.btn_popup_close = pygame.Rect(400, 420, 200, 40)
        self.last_ai_move_time = 0 
        self.start_pos = (0, 0)  # Thêm biến lưu vị trí bắt đầu để vẽ màu riêng nếu cần

    def load_knight_image(self):
        try:
            path = Path(__file__).resolve().parents[2] / "assets" / "knight.png"
            return pygame.image.load(str(path)).convert_alpha()
        except Exception as ex:
            print(f"Không thể tải knight.png: {ex}")
            return None

    def setup_game(self, level_id, algo_name):
        self.reset_state()
        self.level_id = level_id
        self.algo_name = algo_name
        
        lvl_cfg = LEVELS[level_id]
        rows, cols = lvl_cfg["rows"], lvl_cfg["cols"]
        obstacles = lvl_cfg["obstacles"]
        
        # --- TỰ ĐỘNG RANDOM VỊ TRÍ BẮT ĐẦU HỢP LỆ ---
        valid_positions = []
        for r in range(rows):
            for c in range(cols):
                if (r, c) not in obstacles:
                    valid_positions.append((r, c))
        
        # Chọn ngẫu nhiên 1 ô trong danh sách các ô không có vật cản
        self.start_pos = random.choice(valid_positions)
        # --------------------------------------------

        # Truyền vị trí start_pos vừa random vào Solver
        self.solver = KnightTourSolver(rows, cols, start_pos=self.start_pos, obstacles=obstacles)
        
        if "DFS" in algo_name:
            self.solver_generator = self.solver.solve_dfs()
        else:
            self.solver_generator = self.solver.solve_bfs()
            
        self.start_time = time.time()
        self.last_ai_move_time = time.time()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.show_popup and self.btn_popup_close.collidepoint(event.pos):
                self.manager.switch_screen("main_menu")
            elif self.btn_back.collidepoint(event.pos):
                self.manager.switch_screen("level_select")

    def update(self):
        if self.is_finished or self.show_popup:
            return

        current_time = time.time()
        self.elapsed_time = current_time - self.start_time

        if self.solver_generator and (current_time - self.last_ai_move_time >= AI_DELAY):
            try:
                self.path, self.visited_nodes, done = next(self.solver_generator)
                self.last_ai_move_time = current_time
                
                if done:
                    self.is_finished = True
                    self.success = len(self.path) == self.solver.total_cells
                    self.show_popup = True
                    status_str = "Thành công" if self.success else "Thất bại"
                    save_match(LEVELS[self.level_id]["name"], self.algo_name, len(self.path), self.elapsed_time, status_str)
            except StopIteration:
                self.is_finished = True
                self.show_popup = True

    def draw(self, screen):
        screen.fill(COLOR_BG)
        lvl_cfg = LEVELS[self.level_id]
        rows, cols = lvl_cfg["rows"], lvl_cfg["cols"]
        
        cell_w = self.board_rect.width / cols
        cell_h = self.board_rect.height / rows
        path_set = set(self.path)
        
        current_pos = self.path[-1] if self.path else self.start_pos
        for r in range(rows):
            for c in range(cols):
                rect = pygame.Rect(self.board_rect.x + c * cell_w, self.board_rect.y + r * cell_h, cell_w, cell_h)
                
                if (r, c) in lvl_cfg["obstacles"]:
                    color = (44, 62, 80)
                elif (r, c) == current_pos:
                    color = COLOR_CURRENT
                elif (r, c) in path_set:
                    color = COLOR_VISITED
                else:
                    color = COLOR_CELL_LIGHT if (r + c) % 2 == 0 else COLOR_CELL_DARK
                    
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (200,200,200), rect, width=1)
                
                if (r, c) in self.path:
                    idx = self.path.index((r, c)) + 1
                    num_surf = self.font.render(str(idx), True, (255,255,255) if color == COLOR_VISITED else (0,0,0))
                    screen.blit(num_surf, (rect.x + 5, rect.y + 5))

        if len(self.path) > 0:
            px = self.board_rect.x + current_pos[1] * cell_w + cell_w // 2
            py = self.board_rect.y + current_pos[0] * cell_h + cell_h // 2
            if self.knight_img:
                size = int(min(cell_w, cell_h) * 0.6)
                knight_surface = pygame.transform.smoothscale(self.knight_img, (size, size))
                screen.blit(knight_surface, (int(px - size / 2), int(py - size / 2)))
            else:
                radius = int(min(cell_w, cell_h) * 0.2)
                pygame.draw.circle(screen, (0, 0, 0), (int(px), int(py)), radius)
                pygame.draw.circle(screen, (255, 255, 255), (int(px), int(py)), radius - 4)

        if len(self.path) > 1:
            points = []
            for (r, c) in self.path:
                px = self.board_rect.x + c * cell_w + cell_w // 2
                py = self.board_rect.y + r * cell_h + cell_h // 2
                points.append((px, py))
            pygame.draw.lines(screen, COLOR_PATH, False, points, width=3)

        # Thanh Sidebar
        pygame.draw.rect(screen, COLOR_SIDEBAR, (630, 60, 330, 550), border_radius=10)
        screen.blit(self.font_bold.render("THÔNG SỐ BÀN CHƠI", True, COLOR_TEXT), (650, 90))
        screen.blit(self.font.render(f"Màn chơi: {lvl_cfg['name']}", True, COLOR_TEXT), (650, 140))
        screen.blit(self.font.render(f"Thuật toán: {self.algo_name}", True, COLOR_TEXT), (650, 180))
        screen.blit(self.font.render(f"Thời gian: {self.elapsed_time:.2f} Giây", True, COLOR_TEXT), (650, 220))
        screen.blit(self.font.render(f"Số bước đã đi: {len(self.path)} / {self.solver.total_cells}", True, COLOR_TEXT), (650, 260))
        screen.blit(self.font.render(f"Số node đã duyệt: {self.visited_nodes}", True, COLOR_TEXT), (650, 300))

        pygame.draw.rect(screen, (231, 76, 60), self.btn_back, border_radius=5)
        screen.blit(self.font.render("Dừng chơi", True, (255,255,255)), (self.btn_back.x + 22, self.btn_back.y + 8))

        if self.show_popup:
            s = pygame.Surface((1000,700), pygame.SRCALPHA)
            s.fill((0,0,0,180))
            screen.blit(s, (0,0))
            
            popup_rect = pygame.Rect(300, 200, 400, 300)
            pygame.draw.rect(screen, (255,255,255), popup_rect, border_radius=15)
            
            title_text = "THÀNH CÔNG!" if self.success else "THẤT BẠI HOẶC HẾT ĐƯỜNG!"
            title_color = (46, 204, 113) if self.success else (231, 76, 60)
            
            t_surf = self.font_bold.render(title_text, True, title_color)
            screen.blit(t_surf, (400, 230))
            screen.blit(self.font.render(f"Tổng thời gian tính: {self.elapsed_time:.2f}s", True, (0,0,0)), (350, 290))
            screen.blit(self.font.render(f"Tổng số bước nhảy: {len(self.path)}", True, (0,0,0)), (350, 330))
            screen.blit(self.font.render(f"Tổng số Node AI duyệt: {self.visited_nodes}", True, (0,0,0)), (350, 370))
            
            pygame.draw.rect(screen, (52, 152, 219), self.btn_popup_close, border_radius=5)
            screen.blit(self.font.render("Xác nhận & Quay lại", True, (255,255,255)), (425, 428))