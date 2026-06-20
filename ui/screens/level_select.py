import pygame
from config import COLOR_BG, COLOR_TEXT, LEVELS, ALGORITHMS, SCREEN_WIDTH

class LevelSelect:
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont("Times New Roman", 20)
        self.font_title = pygame.font.SysFont("Times New Roman", 28, bold=True)
        
        self.selected_level = 1
        self.selected_algo_idx = 0
        
        # Thiết kế các ô chọn level (2 cột, 3 hàng)
        self.level_rects = {}
        for i, lvl_id in enumerate(LEVELS.keys()):
            col = i % 2
            row = i // 2
            x = 150 + col * 360
            y = 150 + row * 80
            self.level_rects[lvl_id] = pygame.Rect(x, y, 320, 60)
            
        # Nút tương tác
        self.btn_algo = pygame.Rect(SCREEN_WIDTH//2 - 150, 450, 300, 40)
        self.btn_start = pygame.Rect(SCREEN_WIDTH//2 - 150, 530, 300, 50)
        self.btn_back = pygame.Rect(30, 30, 100, 40)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            # Kiểm tra click chọn Level
            for lvl_id, rect in self.level_rects.items():
                if rect.collidepoint(pos):
                    self.selected_level = lvl_id
            
            # Click chuyển đổi thuật toán giải
            if self.btn_algo.collidepoint(pos):
                self.selected_algo_idx = (self.selected_algo_idx + 1) % len(ALGORITHMS)
                
            # Click Bắt đầu chơi
            if self.btn_start.collidepoint(pos):
                self.manager.screens["gameplay"].setup_game(self.selected_level, ALGORITHMS[self.selected_algo_idx])
                self.manager.switch_screen("gameplay")
                
            # Quay lại
            if self.btn_back.collidepoint(pos):
                self.manager.switch_screen("main_menu")

    def update(self): pass

    def draw(self, screen):
        screen.fill(COLOR_BG)
        
        # Nút Quay lại
        pygame.draw.rect(screen, (180, 180, 180), self.btn_back, border_radius=5)
        screen.blit(self.font.render("Quay lại", True, (0,0,0)), (45, 38))
        
        # Tiêu đề chính
        title = self.font_title.render("CẤU HÌNH MÀN CHƠI AI", True, COLOR_TEXT)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        # Vẽ danh sách Level
        for lvl_id, rect in self.level_rects.items():
            is_sel = (lvl_id == self.selected_level)
            bg_color = (100, 149, 237) if is_sel else (220, 225, 230)
            text_color = (255, 255, 255) if is_sel else COLOR_TEXT
            
            pygame.draw.rect(screen, bg_color, rect, border_radius=8)
            pygame.draw.rect(screen, COLOR_TEXT, rect, width=1 if not is_sel else 2, border_radius=8)
            
            lvl_name = LEVELS[lvl_id]["name"]
            txt = self.font.render(lvl_name, True, text_color)
            screen.blit(txt, (rect.x + 20, rect.y + 18))

        # Vẽ thanh chọn thuật toán
        pygame.draw.rect(screen, (255, 255, 255), self.btn_algo, border_radius=5)
        pygame.draw.rect(screen, COLOR_TEXT, self.btn_algo, width=1, border_radius=5)
        algo_txt = self.font.render(f"AI: {ALGORITHMS[self.selected_algo_idx]}", True, COLOR_TEXT)
        screen.blit(algo_txt, (self.btn_algo.x + 15, self.btn_algo.y + 8))
        
        # Nút Start
        pygame.draw.rect(screen, (46, 204, 113), self.btn_start, border_radius=8)
        st_txt = self.font_title.render("BẮT ĐẦU CHẠY", True, (255,255,255))
        screen.blit(st_txt, (self.btn_start.x + self.btn_start.width//2 - st_txt.get_width()//2, self.btn_start.y + 8))