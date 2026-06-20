import pygame
from config import COLOR_BG, COLOR_TEXT, SCREEN_WIDTH
from storage.database import load_history, clear_all_history

class HistoryScreen:
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont("Times New Roman", 16)
        self.font_title = pygame.font.SysFont("Times New Roman", 26, bold=True)
        
        self.btn_back = pygame.Rect(30, 30, 100, 40)
        self.btn_clear = pygame.Rect(SCREEN_WIDTH - 180, 30, 150, 40)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_back.collidepoint(event.pos):
                self.manager.switch_screen("main_menu")
            elif self.btn_clear.collidepoint(event.pos):
                clear_all_history()

    def update(self): pass

    def draw(self, screen):
        screen.fill(COLOR_BG)
        
        pygame.draw.rect(screen, (180, 180, 180), self.btn_back, border_radius=5)
        screen.blit(self.font.render("Quay lại", True, (0,0,0)), (45, 38))
        
        pygame.draw.rect(screen, (231, 76, 60), self.btn_clear, border_radius=5)
        screen.blit(self.font.render("Xóa toàn bộ", True, (255,255,255)), (SCREEN_WIDTH - 150, 38))
        
        title = self.font_title.render("LỊCH SỬ THỬ NGHIỆM AI", True, COLOR_TEXT)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 35))
        
        # Vẽ tiêu đề cột Table bảng dữ liệu
        headers = ["Thời gian", "Màn chơi", "Thuật toán", "Số bước", "T.Gian Chạy", "Kết quả"]
        positions = [50, 250, 420, 620, 720, 850]
        
        for h, pos in zip(headers, positions):
            screen.blit(self.font.render(h, True, (0,0,0)), (pos, 110))
        pygame.draw.line(screen, (0,0,0), (40, 135), (960, 135), 2)
        
        # Đọc dữ liệu từ DB vẽ ra danh sách hàng lịch sử
        history_data = load_history()
        y_offset = 150
        for match in reversed(history_data[-10:]): # Chỉ hiển thị tối đa 10 trận gần nhất
            screen.blit(self.font.render(match["date"], True, COLOR_TEXT), (50, y_offset))
            screen.blit(self.font.render(match["level"], True, COLOR_TEXT), (250, y_offset))
            screen.blit(self.font.render(match["algo"], True, COLOR_TEXT), (420, y_offset))
            screen.blit(self.font.render(str(match["steps"]), True, COLOR_TEXT), (620, y_offset))
            screen.blit(self.font.render(match["time"], True, COLOR_TEXT), (720, y_offset))
            
            color_status = (46, 204, 113) if match["status"] == "Thành công" else (231, 76, 60)
            screen.blit(self.font.render(match["status"], True, color_status), (850, y_offset))
            
            pygame.draw.line(screen, (220,220,220), (40, y_offset + 30), (960, y_offset + 30), 1)
            y_offset += 40