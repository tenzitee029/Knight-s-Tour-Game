import pygame
import os
import shutil
from tkinter import Tk, filedialog
from config import COLOR_BG, COLOR_TEXT, SCREEN_WIDTH
from storage.database import load_history, clear_all_history

class HistoryScreen:
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont("Times New Roman", 16)
        self.font_title = pygame.font.SysFont("Times New Roman", 26, bold=True)
        
        self.btn_back = pygame.Rect(30, 30, 100, 40)
        self.btn_clear = pygame.Rect(SCREEN_WIDTH - 180, 30, 150, 40)
        
        # Danh sách lưu vị trí các nút bấm của các hàng để bắt sự kiện click
        self.download_buttons = []

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_back.collidepoint(event.pos):
                self.manager.switch_screen("main_menu")
                return
            elif self.btn_clear.collidepoint(event.pos):
                clear_all_history()
                return
                
            # Kiểm tra xem có click vào nút tải GIF nào không
            # Debug: in thông tin click và danh sách nút
            try:
                print(f"[DEBUG] Click tại: {event.pos}; Số nút tải hiện có: {len(self.download_buttons)}")
                for i, (btn_rect, match_id, gif_type) in enumerate(self.download_buttons):
                    print(f"[DEBUG] Btn[{i}] rect={btn_rect} id={match_id} type={gif_type}")
                    if btn_rect.collidepoint(event.pos):
                        print(f"[DEBUG] Click trúng nút tải: id={match_id} type={gif_type}")
                        self.download_gif(match_id, gif_type)
                        break
            except Exception as ex:
                print(f"[DEBUG] Lỗi khi xử lý click trong HistoryScreen: {ex}")

    def download_gif(self, match_id, gif_type):
        """Mở cửa sổ Windows để chọn nơi lưu file GIF"""
        from pathlib import Path
        exports_dir = Path(__file__).resolve().parents[2] / "exports"
        source_path = str(exports_dir / f"match_{match_id}_{gif_type}.gif")

        if not os.path.exists(source_path):
            # Nếu thư mục exports không tồn tại, tạo luôn để người dùng có thể lưu sau
            if not exports_dir.exists():
                try:
                    exports_dir.mkdir(parents=True, exist_ok=True)
                    print(f"[INFO] Tạo thư mục exports tại: {exports_dir}")
                except Exception as ex:
                    print(f"[ERROR] Không thể tạo thư mục exports: {ex}")

            # kiểm tra tên thay thế (đuôi in hoa)
            alt = str(exports_dir / f"match_{match_id}_{gif_type}.GIF")
            if os.path.exists(alt):
                source_path = alt
            else:
                print(f"Không tìm thấy file gốc: {source_path}")
                print(f"[DEBUG] Thư mục exports tồn tại: {exports_dir.exists()}; Nội dung: {list(exports_dir.glob('*')) if exports_dir.exists() else 'N/A'}")
                print("Hãy chạy lại một trận để chương trình tạo các file GIF trong thư mục 'exports' trước khi tải xuống.")
                return
            
        # Khởi tạo cửa sổ ẩn của tkinter để dùng filedialog
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True) # Đưa cửa sổ lên trên cùng
        
        default_filename = f"knight_tour_{gif_type}_match_{match_id}.gif"
        file_path = filedialog.asksaveasfilename(
            title="Chọn nơi lưu file GIF",
            initialfile=default_filename,
            defaultextension=".gif",
            filetypes=[("GIF Files", "*.gif")]
        )
        
        root.destroy()
        
        if file_path:
            shutil.copy(source_path, file_path)
            print(f"Đã tải file về: {file_path}")

    def update(self): pass

    def draw(self, screen):
        screen.fill(COLOR_BG)
        
        pygame.draw.rect(screen, (180, 180, 180), self.btn_back, border_radius=5)
        screen.blit(self.font.render("Quay lại", True, (0,0,0)), (45, 38))
        
        pygame.draw.rect(screen, (231, 76, 60), self.btn_clear, border_radius=5)
        screen.blit(self.font.render("Xóa lịch sử", True, (255,255,255)), (SCREEN_WIDTH - 150, 38))
        
        title = self.font_title.render("LỊCH SỬ TRẬN ĐẤU AI", True, COLOR_TEXT)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 35))
        
        headers = ["Thời gian", "Màn chơi", "Thuật toán", "Số bước", "T.Gian", "Kết quả", "Tải GIF"]
        positions = [40, 200, 360, 500, 580, 660, 780]
        
        for h, pos in zip(headers, positions):
            screen.blit(self.font.render(h, True, (0,0,0)), (pos, 110))
        pygame.draw.line(screen, (0,0,0), (40, 135), (960, 135), 2)
        
        history_data = load_history()
        y_offset = 150
        
        # Làm sạch danh sách nút trước khi vẽ lại để tránh bị lệch tọa độ
        self.download_buttons = []
        
        # Hiển thị tối đa 10 trận gần nhất
        for match in reversed(history_data[-10:]):
            screen.blit(self.font.render(match["date"], True, COLOR_TEXT), (40, y_offset))
            screen.blit(self.font.render(match["level"], True, COLOR_TEXT), (200, y_offset))
            screen.blit(self.font.render(match["algo"], True, COLOR_TEXT), (360, y_offset))
            screen.blit(self.font.render(str(match["steps"]), True, COLOR_TEXT), (500, y_offset))
            screen.blit(self.font.render(match["time"], True, COLOR_TEXT), (580, y_offset))
            
            # Trạng thái màu sắc kết quả
            successful_statuses = {
                "Thành công",
                "AI MAX thắng"
            }

            status = match["status"]

            is_successful = (
                status in successful_statuses
                or status.startswith("AI MAX thắng ở trận")
            )

            status_color = (
                (46, 204, 113)
                if is_successful
                else (231, 76, 60)
            )


            screen.blit(self.font.render(match["status"], True, status_color), (660, y_offset))
            
            # --- TẠO VÀ VẼ NÚT TẢI GIF ---
            # 1. Nút tải Đường đi (chỉ bật nếu Thành công)
            btn_path = pygame.Rect(760, y_offset - 2, 90, 24)
            if (
                match["status"] in {
                    "Thành công",
                    "AI MAX thắng",
                    "AI MIN thắng"
                }
                or match["status"].startswith(
                    "AI MAX thắng ở trận"
                )
                or match["status"]
                    == "AI MAX không thắng sau 100 trận"
            ):
                pygame.draw.rect(screen, (52, 152, 219), btn_path, border_radius=4)
                screen.blit(self.font.render("Đường đi", True, (255,255,255)), (775, y_offset))
                self.download_buttons.append((btn_path, match["id"], "path"))
            else:
                pygame.draw.rect(screen, (200, 200, 200), btn_path, border_radius=4)
                screen.blit(self.font.render("Đường đi", True, (140,140,140)), (775, y_offset))

            # 2. Nút tải Quá trình (luôn luôn có)
            btn_process = pygame.Rect(865, y_offset - 2, 95, 24)
            pygame.draw.rect(screen, (46, 204, 113), btn_process, border_radius=4)
            screen.blit(self.font.render("Quá trình", True, (255,255,255)), (882, y_offset))
            self.download_buttons.append((btn_process, match["id"], "process"))
            
            y_offset += 45