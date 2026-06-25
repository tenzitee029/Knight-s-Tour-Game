import pygame
import time
from pathlib import Path
from config import *

from algorithms.uninformed.bfs import BFSSolver
from algorithms.uninformed.dfs import DFSSolver
from algorithms.uninformed.ucs import UCSSolver
from algorithms.uninformed.ids import IDSSolver

from algorithms.informed.gbfs import GBFSSolver
from algorithms.informed.astar import AStarSolver
from algorithms.informed.ida_star import IDAStarSolver

from algorithms.local_search.simple_hill_climbing import SimpleHillClimbingSolver
from algorithms.local_search.stochastic_hill_climbing import StochasticHillClimbingSolver

from algorithms.csp.backtracking import BacktrackingSolver
from algorithms.csp.forward_checking import ForwardCheckingSolver
from algorithms.csp.ac3 import AC3Solver
from algorithms.csp.min_conflicts import MinConflictsSolver
from algorithms.adversarial.minimax import MinimaxSolver
from algorithms.adversarial.expectimax import ExpectimaxSolver

from storage.database import save_match
from PIL import Image, ImageDraw

class Gameplay:
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont("Times New Roman", 18)
        self.font_bold = pygame.font.SysFont("Times New Roman", 22, bold=True)
        self.font_icon = pygame.font.SysFont("Times New Roman", 32, bold=True)
        self.knight_img = self.load_knight_image()
        
        self.board_rect = pygame.Rect(40, 60, 550, 550)
        self.btn_back = pygame.Rect(840, 620, 120, 40)
        self.btn_skip = pygame.Rect(650, 620, 120, 40)
        
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
        self.btn_popup_close = pygame.Rect(390, 530, 220, 42)        
        self.last_ai_move_time = 0 
        self.start_pos = (0, 0)  # Thêm biến lưu vị trí bắt đầu để vẽ màu riêng nếu cần
        self.current_match_id = None
        self.should_save_gifs = False

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
        
# --- BẮT ĐẦU TỪ Ô GIỮA BÀN CỜ ---
        center_r = rows // 2
        center_c = cols // 2
        
        # Đặt vị trí xuất phát ở giữa
        # Kèm thêm kiểm tra an toàn: nếu ô giữa vô tình bị cấu hình là vật cản, sẽ chọn tạm 1 ô trống đầu tiên
        if (center_r, center_c) not in obstacles:
            self.start_pos = (center_r, center_c)
        else:
            valid_positions = [(r, c) for r in range(rows) for c in range(cols) if (r, c) not in obstacles]
            self.start_pos = valid_positions[0]
        if "Minimax" in algo_name:
            self.solver = MinimaxSolver(
                rows,
                cols,
                start_pos=self.start_pos,
                obstacles=obstacles
            )

            self.solver_generator = self.solver.solve()
        elif "Expectimax" in algo_name:
            self.solver = ExpectimaxSolver(
                rows,
                cols,
                start_pos=self.start_pos,
                obstacles=obstacles
            )
            self.solver_generator = self.solver.solve()
        # Truyền vị trí start_pos vào Solver
        elif "BFS" in algo_name:
            self.solver = BFSSolver(
                rows,
                cols,
                start_pos=self.start_pos,
                obstacles=obstacles
            )
            self.solver_generator = self.solver.solve()

        elif "DFS" in algo_name:
            self.solver = DFSSolver(
                rows,
                cols,
                start_pos=self.start_pos,
                obstacles=obstacles
            )
            self.solver_generator = self.solver.solve()

        elif "UCS" in algo_name:
            self.solver = UCSSolver(
                rows,
                cols,
                start_pos=self.start_pos,
                obstacles=obstacles
            )
            self.solver_generator = self.solver.solve()

        elif "IDS" in algo_name:
            self.solver = IDSSolver(
                rows,
                cols,
                start_pos=self.start_pos,
                obstacles=obstacles
            )
            self.solver_generator = self.solver.solve()

        elif "GBFS" in algo_name:
            self.solver = GBFSSolver(
                rows,
                cols,
                start_pos=self.start_pos,
                obstacles=obstacles
            )
            self.solver_generator = self.solver.solve()

        elif "IDA*" in algo_name:
            self.solver = IDAStarSolver(
                rows,
                cols,
                start_pos=self.start_pos,
                obstacles=obstacles
            )
            self.solver_generator = self.solver.solve()

        elif "A*" in algo_name:
            self.solver = AStarSolver(
                rows,
                cols,
                start_pos=self.start_pos,
                obstacles=obstacles
            )
            self.solver_generator = self.solver.solve()

        elif "Simple Hill Climbing" in algo_name:
            self.solver = SimpleHillClimbingSolver(
                rows,
                cols,
                start_pos=self.start_pos,
                obstacles=obstacles
            )
            self.solver_generator = self.solver.solve()

        elif "Stochastic Hill Climbing" in algo_name:
            self.solver = StochasticHillClimbingSolver(
                rows,
                cols,
                start_pos=self.start_pos,
                obstacles=obstacles
            )
            self.solver_generator = self.solver.solve()

        elif "Backtracking" in algo_name:
            self.solver = BacktrackingSolver(
                rows,
                cols,
                start_pos=self.start_pos,
                obstacles=obstacles
            )
            self.solver_generator = self.solver.solve()

        elif "Forward Checking" in algo_name:
            self.solver = ForwardCheckingSolver(
                rows,
                cols,
                start_pos=self.start_pos,
                obstacles=obstacles
            )
            self.solver_generator = self.solver.solve()

        elif "AC3" in algo_name or "AC-3" in algo_name:
            self.solver = AC3Solver(
                rows,
                cols,
                start_pos=self.start_pos,
                obstacles=obstacles
            )
            self.solver_generator = self.solver.solve()

        elif "Min-Conflicts" in algo_name:
            self.solver = MinConflictsSolver(
                rows,
                cols,
                start_pos=self.start_pos,
                obstacles=obstacles
            )
            self.solver_generator = self.solver.solve()

        self.start_time = time.time()
        self.last_ai_move_time = time.time()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.show_popup and self.btn_popup_close.collidepoint(event.pos):
                self.manager.switch_screen("main_menu")
            elif self.btn_back.collidepoint(event.pos):
                self.manager.switch_screen("level_select")
            elif not self.is_finished and not self.show_popup and self.btn_skip.collidepoint(event.pos):
                self.trigger_skip_calculation()

    def trigger_skip_calculation(self):
        """Hàm chạy ép luồng AI ngầm để hoàn thành ngay lập tức và sinh GIF"""
        if not self.solver_generator:
            return

        print("⏩ Đang tua nhanh thuật toán để xuất GIF ngầm...")
        try:
            done = False
            # Sử dụng vòng lặp chạy ngầm không dừng cho đến khi tìm thấy đích hoặc hết đường
            while not done:
                result = next(self.solver_generator)
                self.path = result[0]
                self.visited_nodes = result[1]
                done = result[2]
            
            # Xử lý kết thúc giống y hệt khi chạy xong tự nhiên
            self.finalize_game_and_save()

        except StopIteration:
            self.finalize_game_and_save()
            
    def finalize_game_and_save(self):
        """Kết thúc trận, lưu lịch sử và tạo GIF."""

        self.is_finished = True

        # Xác định kết quả theo từng nhóm thuật toán
        if "Minimax" in self.algo_name:
            self.success = self.solver.max_won

        elif "Expectimax" in self.algo_name:
            self.success = self.solver.max_won

        else:
            self.success = (
                len(self.path)
                == self.solver.total_cells
            )

        status_str = self.get_result_status()
        self.show_popup = True

        # Lưu kết quả vào lịch sử
        self.current_match_id = save_match(
            LEVELS[self.level_id]["name"],
            self.algo_name,
            len(self.path),
            time.time() - self.start_time,
            status_str
        )

        # Tạo GIF đường đi và quá trình
        self.save_gifs_logic()
    def get_result_status(self):
        """Trả về nội dung kết quả để lưu lịch sử."""

        if "Minimax" in self.algo_name:
            if self.solver.max_won:
                return (
                    f"AI MAX thắng ở trận "
                    f"{self.solver.winning_game}"
                )

            return "AI MAX không thắng sau 100 trận"
        if "Expectimax" in self.algo_name:
            if self.solver.max_won:
                return (
                    f"AI MAX thắng ở trận "
                    f"{self.solver.winning_game}"
                )

            return "AI MAX không thắng sau 100 trận"
        return (
            "Thành công"
            if self.success
            else "Thất bại"
        )

    def update(self):
        if self.is_finished or self.show_popup:
            return

        current_time = time.time()
        self.elapsed_time = current_time - self.start_time

        if (self.solver_generator and current_time - self.last_ai_move_time >= AI_DELAY):
            try:
                result = next(self.solver_generator)
                self.path = result[0]
                self.visited_nodes = result[1]
                done = result[2]

                self.last_ai_move_time = current_time

                if done:
                    # Gọi hàm hoàn tất xử lý tự động
                    self.finalize_game_and_save()

            except StopIteration:
                self.finalize_game_and_save()

    def draw(self, screen):
        screen.fill(COLOR_BG)
        lvl_cfg = LEVELS[self.level_id]
        rows, cols = lvl_cfg["rows"], lvl_cfg["cols"]
        
        cell_w = self.board_rect.width / cols
        cell_h = self.board_rect.height / rows
        path_set = set(self.path)
        dynamic_obstacles = getattr(
            self.solver,
            "dynamic_obstacles",
            set()
        )
        
        current_pos = self.path[-1] if self.path else self.start_pos
        for r in range(rows):
            for c in range(cols):
                rect = pygame.Rect(self.board_rect.x + c * cell_w, self.board_rect.y + r * cell_h, cell_w, cell_h)
                
                if (r, c) in dynamic_obstacles:
                    if "Expectimax" in self.algo_name:
                        # Vật cản do CHANCE tạo: màu tím
                        color = (155, 89, 182)
                    else:
                        # Vật cản do AI MIN tạo: màu đỏ
                        color = (231, 76, 60)
                elif (r, c) in lvl_cfg["obstacles"]:
                    # Vật cản có sẵn
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
        if "Minimax" in self.algo_name:
            blocked_count = len(
                self.solver.dynamic_obstacles
            )

            screen.blit(
                self.font.render(
                    f"Số ô AI MIN đã khóa: {blocked_count}",
                    True,
                    (231, 76, 60)
                ),
                (650, 340)
            )
        pygame.draw.rect(screen, (231, 76, 60), self.btn_back, border_radius=5)
        screen.blit(self.font.render("Dừng chơi", True, (255,255,255)), (self.btn_back.x + 22, self.btn_back.y + 8))

        # Vẽ nút Skip
        if not self.is_finished and not self.show_popup:
            pygame.draw.rect(screen, (52, 152, 219), self.btn_skip, border_radius=5)
            screen.blit(self.font.render("Tua nhanh", True, (255,255,255)), (self.btn_skip.x + 22, self.btn_skip.y + 8))

        # Thực thi xuất file ngay khi biến này được kích hoạt ở update()
        if self.should_save_gifs:
            self.should_save_gifs = False
            self.save_gifs_logic(screen)

        # Vẽ popup thông báo đè lên sau cùng
        if self.show_popup:
            overlay = pygame.Surface(
                (SCREEN_WIDTH, SCREEN_HEIGHT),
                pygame.SRCALPHA
            )
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            popup_rect = pygame.Rect(
                220,
                90,
                560,
                520
            )

            pygame.draw.rect(
                screen,
                (255, 255, 255),
                popup_rect,
                border_radius=15
            )
            if "Expectimax" in self.algo_name:
                if self.solver.max_won:
                    title_text = "AI MAX THẮNG!"
                    title_color = (46, 204, 113)
                else:
                    title_text = (
                        "AI MAX KHÔNG THẮNG SAU 100 TRẬN!"
                    )
                    title_color = (231, 76, 60)

            elif "Minimax" in self.algo_name:
                if self.solver.max_won:
                    title_text = "AI MAX THẮNG!"
                    title_color = (46, 204, 113)
                else:
                    title_text = (
                        "AI MAX KHÔNG THẮNG SAU 100 TRẬN!"
                    )
                    title_color = (231, 76, 60)

            else:
                title_text = (
                    "THÀNH CÔNG!"
                    if self.success
                    else "THẤT BẠI HOẶC HẾT ĐƯỜNG!"
                )

                title_color = (
                    (46, 204, 113)
                    if self.success
                    else (231, 76, 60)
                )


            title_surface = self.font_bold.render(
                title_text,
                True,
                title_color
            )

            screen.blit(
                title_surface,
                (
                    popup_rect.centerx
                    - title_surface.get_width() // 2,
                    170
                )
            )

            # Thông tin chung
            information_lines = [
                f"Tổng thời gian tính: {self.elapsed_time:.2f}s",
                f"Tổng số bước nhảy: {len(self.path)}",
                f"Tổng số Node AI duyệt: {self.visited_nodes}"
            ]
            # Thông tin riêng của Expectimax
            if "Expectimax" in self.algo_name:
                winning_game = getattr(
                    self.solver,
                    "winning_game",
                    None
                )

                information_lines.extend([
                    (
                        f"Số trận đã chơi: "
                        f"{self.solver.game_count}/"
                        f"{self.solver.MAX_GAMES}"
                    ),
                    (
                        f"Trận MAX thắng: "
                        f"{winning_game if winning_game else '--'}"
                    ),
                    (
                        f"Mục tiêu MAX: "
                        f"{self.solver.max_win_target}/"
                        f"{self.solver.total_cells} ô"
                    ),
                    (
                        f"Số ô đã đi ở trận kết quả: "
                        f"{len(self.path)}/"
                        f"{self.solver.max_win_target}"
                    ),
                    (
                        f"Số ô CHANCE đã khóa: "
                        f"{len(self.solver.dynamic_obstacles)}"
                    )
                ])
            # Thông tin riêng của Minimax
            elif "Minimax" in self.algo_name:
                game_count = getattr(
                    self.solver,
                    "game_count",
                    1
                )

                winning_game = getattr(
                    self.solver,
                    "winning_game",
                    None
                )

                max_games = getattr(
                    self.solver,
                    "MAX_GAMES",
                    100
                )

                target = getattr(
                    self.solver,
                    "max_win_target",
                    0
                )

                blocked_count = len(
                    getattr(
                        self.solver,
                        "dynamic_obstacles",
                        set()
                    )
                )

                information_lines.extend([
                    f"Số trận đã chơi: {game_count}/{max_games}",
                    (
                        "Trận MAX thắng: "
                        f"{winning_game if winning_game else '--'}"
                    ),
                    (
                        f"Mục tiêu MAX: "
                        f"{target}/{self.solver.total_cells} ô"
                    ),
                    (
                        f"Số ô đã đi ở trận kết quả: "
                        f"{len(self.path)}/{target}"
                    ),
                    f"Số ô MIN đã khóa: {blocked_count}"
                ])

            # Vẽ từng dòng thông tin
            start_y = 225

            for index, information in enumerate(
                information_lines
            ):
                text_surface = self.font.render(
                    information,
                    True,
                    COLOR_TEXT
                )

                screen.blit(
                    text_surface,
                    (
                        popup_rect.x + 35,
                        start_y + index * 36
                    )
                )

            pygame.draw.rect(
                screen,
                (52, 152, 219),
                self.btn_popup_close,
                border_radius=5
            )

            close_text = self.font.render(
                "Xác nhận & Quay lại",
                True,
                (255, 255, 255)
            )

            screen.blit(
                close_text,
                (
                    self.btn_popup_close.centerx
                    - close_text.get_width() // 2,
                    self.btn_popup_close.y + 10
                )
            )
    def export_to_gif(self, match_id):
        """Hàm vẽ bàn cờ và xuất ra file GIF lưu trong thư mục exports"""
        import os
        os.makedirs("exports", exist_ok=True)

    def save_gifs_logic(self):
        """Tự động tạo và lưu trực tiếp 2 file GIF ngầm bằng Pillow"""
        try:
            import os
            from PIL import Image, ImageDraw
            from pathlib import Path

            exports_dir = Path(__file__).resolve().parents[2] / "exports"
            exports_dir.mkdir(parents=True, exist_ok=True)
            match_id = self.current_match_id if self.current_match_id else "unknown"
            print(f"[GIF] Bắt đầu tạo GIF cho match_id={match_id} tại {exports_dir}")
            
            lvl_cfg = LEVELS[self.level_id]
            rows, cols = lvl_cfg["rows"], lvl_cfg["cols"]
            obstacles = set(lvl_cfg["obstacles"])
            dynamic_obstacles = set(
                getattr(
                    self.solver,
                    "dynamic_obstacles",
                    set()
                )
            )
            
            # Cấu hình khung ảnh GIF 400x400 pixel
            img_size = 400
            cell_w = img_size / cols
            cell_h = img_size / rows
            
            def draw_frame_by_pillow(current_path_list):
                """Hàm vẽ một trạng thái bàn cờ bằng Pillow"""
                img = Image.new("RGBA", (img_size, img_size), (240, 244, 248))
                draw = ImageDraw.Draw(img)
                path_set = set(current_path_list)
                curr_pos = current_path_list[-1] if current_path_list else self.start_pos
                
                for r in range(rows):
                    for c in range(cols):
                        x1, y1 = c * cell_w, r * cell_h
                        x2, y2 = x1 + cell_w, y1 + cell_h
                        
                        if (r, c) in dynamic_obstacles:
                            if "Expectimax" in self.algo_name:
                                color = (155, 89, 182)
                            else:
                                color = (231, 76, 60)

                        elif (r, c) in obstacles:
                            color = (44, 62, 80)
                        elif (r, c) in obstacles:
                            color = (44, 62, 80)   # Vật cản có sẵn
                        elif (r, c) == curr_pos:
                            color = (255, 215, 0)       # Vị trí hiện tại (Vàng)
                        elif (r, c) in path_set:
                            color = (100, 149, 237)     # Ô đã đi (Xanh)
                        else:
                            color = (235, 235, 208) if (r + c) % 2 == 0 else (119, 149, 86)
                            
                        draw.rectangle([x1, y1, x2, y2], fill=color, outline=(200, 200, 200))
                        
                        # Điền số thứ tự bước đi
                        if (r, c) in current_path_list:
                            step_num = current_path_list.index((r, c)) + 1
                            draw.text((x1 + 6, y1 + 4), str(step_num), fill=(255, 255, 255) if (r, c) != curr_pos else (0, 0, 0))
                
                # Vẽ nét nối đường đi
                if len(current_path_list) > 1:
                    points = []
                    for (r, c) in current_path_list:
                        px = c * cell_w + cell_w / 2
                        py = r * cell_h + cell_h / 2
                        points.append((px, py))
                    draw.line(points, fill=(255, 69, 0), width=2)
                    
                return img

            # --- 1. XUẤT GIF TIẾN TRÌNH LỜI GIẢI ĐƯỜNG ĐI (Chỉ khi thành công) ---
            if self.path:
                path_frames = []
                for i in range(1, len(self.path) + 1):
                    path_frames.append(draw_frame_by_pillow(self.path[:i]))
                    
                if path_frames:
                    path_out = str(exports_dir / f"match_{match_id}_path.gif")
                    print(f"[GIF] Lưu file path -> {path_out}")
                    path_frames[0].save(
                        path_out, save_all=True, append_images=path_frames[1:], duration=150, loop=0
                    )
                    print(f"--> [OK] Đã lưu file đường đi tốt nhất: {path_out}")

            # --- 2. XUẤT GIF TOÀN BỘ QUÁ TRÌNH DI CHUYỂN ---
            process_frames = []
            # Trích xuất mẫu khoảng 20-30 khung hình để tránh file GIF bị quá nặng
            step_chunks = max(1, len(self.path) // 25)
            for i in range(1, len(self.path) + 1, step_chunks):
                process_frames.append(draw_frame_by_pillow(self.path[:i]))
            
            # Đảm bảo có frame cuối cùng kết thúc
            process_frames.append(draw_frame_by_pillow(self.path))
            
            if process_frames:
                proc_out = str(exports_dir / f"match_{match_id}_process.gif")
                print(f"[GIF] Lưu file process -> {proc_out}")
                process_frames[0].save(
                    proc_out, save_all=True, append_images=process_frames[1:], duration=250, loop=0
                )
                print(f"--> [OK] Đã lưu file toàn bộ quá trình: {proc_out}")

        except Exception as e:
            print(f"❌ LỖI KHI XUẤT FILE GIF: {e}")