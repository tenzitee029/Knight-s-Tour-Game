import pygame
import os
import shutil
from config import COLOR_BG, COLOR_TEXT, SCREEN_WIDTH
from storage.database import load_history, clear_all_history

class HistoryScreen:
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont("Times New Roman", 15)
        self.font_small = pygame.font.SysFont("Times New Roman", 12, bold=True)
        self.font_title = pygame.font.SysFont("Times New Roman", 26, bold=True)
        
        self.btn_back = pygame.Rect(30, 30, 100, 40)
        self.btn_clear = pygame.Rect(SCREEN_WIDTH - 180, 30, 150, 40)

    def export_gif_dialog(self, match_id, gif_type):
        """Mở hộp thoại hệ thống cho người dùng chọn thư mục và tải về file GIF"""
        from tkinter import filedialog, Tk
        src_file = f"exports/match_{match_id}_{gif_type}.gif"
        
        if not os.path.exists(src_file):
            print(f"File {src_file} không tồn tại!")
            return

        # Khởi tạo Tkinter ẩn để gọi File Dialog cục bộ không bị lỗi giao diện Pygame
        root = Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        
        default_name = f"KnightTour_Match{match_id}_{gif_type}.gif"
        dest_path = filedialog.asksaveasfilename(
            title=f"Lưu File GIF { 'Đường Đi' if gif_type == 'path' else 'Quá Trình' }",
            initialfile=default_name,
            filetypes=[("GIF files", "*.gif")]
        )
        root.destroy()  # Đóng kết nối cửa sổ sau khi tương tác xong

        if dest_path:
            try:
                shutil.copy(src_file, dest_path)
                print(f"Đã xuất file thành công tới: {dest_path}")
            except Exception as e:
                print(f"Lỗi khi copy file: {e}")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_back.collidepoint(event.pos):
                self.manager.switch_screen("main_menu")
            elif self.btn_clear.collidepoint(event.pos):
                clear_all_history()
            else:
                # Xử lý bắt sự kiện click nút bấm trong hàng bảng dữ liệu
                history_data = load_history()
                y_offset = 150
                for match in reversed(history_data[-10:]):
                    btn_path_rect = pygame.Rect(790, y_offset - 4, 90, 25)
                    btn_proc_rect = pygame.Rect(895, y_offset - 4, 90, 25)
                    
                    if match["status"] == "Thành công" and btn_path_rect.collidepoint(event.pos):
                        self.export_gif_dialog(match["id"], "path")
                        break
                    if btn_proc_rect.collidepoint(event.pos):
                        self.export_gif_dialog(match["id"], "process")
                        break
                        
                    y_offset += 40

    def update(self): pass

    def draw(self, screen):
        screen.fill(COLOR_BG)
        
        pygame.draw.rect(screen, (180, 180, 180), self.btn_back, border_radius=5)
        screen.blit(self.font.render("Quay lại", True, (0,0,0)), (45, 38))
        
        pygame.draw.rect(screen, (231, 76, 60), self.btn_clear, border_radius=5)
        screen.blit(self.font.render("Xóa toàn bộ", True, (255,255,255)), (SCREEN_WIDTH - 150, 38))
        
        title = self.font_title.render("LỊCH SỬ THỬ NGHIỆM AI", True, COLOR_TEXT)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 35))
        
        # Thiết lập vị trí các cột tương thích màn hình 1000px rộng
        headers = ["Thời gian", "Màn chơi", "Thuật toán", "Số bước", "T.Gian", "K.Quả", "Tải GIF 1", "Tải GIF 2"]
        positions = [30, 200, 350, 540, 620, 700, 790, 895]
        
        for h, pos in zip(headers, positions):
            screen.blit(self.font.render(h, True, (0,0,0)), (pos, 110))
        pygame.draw.line(screen, (0,0,0), (20, 135), (980, 135), 2)
        
        history_data = load_history()
        y_offset = 150
        for match in reversed(history_data[-10:]):
            screen.blit(self.font.render(match["date"], True, COLOR_TEXT), (30, y_offset))
            screen.blit(self.font.render(match["level"], True, COLOR_TEXT), (200, y_offset))
            screen.blit(self.font.render(match["algo"], True, COLOR_TEXT), (350, y_offset))
            screen.blit(self.font.render(str(match["steps"]), True, COLOR_TEXT), (540, y_offset))
            screen.blit(self.font.render(match["time"], True, COLOR_TEXT), (620, y_offset))
            
            color_status = (46, 204, 113) if match["status"] == "Thành công" else (231, 76, 60)
            screen.blit(self.font.render(match["status"], True, color_status), (700, y_offset))
            
            # --- VẼ NÚT BẤM XUẤT GIF ĐƯỜNG ĐI ---
            btn_path_rect = pygame.Rect(790, y_offset - 4, 90, 25)
            if match["status"] == "Thành công":
                pygame.draw.rect(screen, (52, 152, 219), btn_path_rect, border_radius=4)
                txt_path = self.font_small.render("Đường đi", True, (255,255,255))
            else:
                pygame.draw.rect(screen, (200, 200, 200), btn_path_rect, border_radius=4)
                txt_path = self.font_small.render("Không có", True, (120,120,120))
            screen.blit(txt_path, (btn_path_rect.x + (btn_path_rect.width - txt_path.get_width())//2, btn_path_rect.y + 5))

            # --- VẼ NÚT BẤM XUẤT GIF QUÁ TRÌNH ---
            btn_proc_rect = pygame.Rect(895, y_offset - 4, 90, 25)
            pygame.draw.rect(screen, (46, 204, 113), btn_proc_rect, border_radius=4)
            txt_proc = self.font_small.render("Quá trình", True, (255,255,255))
            screen.blit(txt_proc, (btn_proc_rect.x + (btn_proc_rect.width - txt_proc.get_width())//2, btn_proc_rect.y + 5))
            
            pygame.draw.line(screen, (220,220,220), (20, y_offset + 30), (980, y_offset + 30), 1)
            y_offset += 40