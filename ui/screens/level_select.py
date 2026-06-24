import pygame

from config import (
    COLOR_BG,
    COLOR_TEXT,
    LEVELS,
    ALGORITHMS,
    SCREEN_WIDTH
)


class LevelSelect:
    def __init__(self, manager):
        self.manager = manager

        self.font = pygame.font.SysFont(
            "Times New Roman",
            20
        )

        self.font_title = pygame.font.SysFont(
            "Times New Roman",
            28,
            bold=True
        )

        self.selected_level = 1
        self.selected_algo_idx = 0

        # Trạng thái đóng/mở danh sách thuật toán
        self.algorithm_list_open = False

        # Các nút chọn màn chơi
        self.level_rects = {}

        for index, level_id in enumerate(LEVELS.keys()):
            column = index % 2
            row = index // 2

            x = 150 + column * 360
            y = 150 + row * 80

            self.level_rects[level_id] = pygame.Rect(
                x,
                y,
                320,
                60
            )

        # Ô chính dùng để mở danh sách thuật toán
        self.btn_algo = pygame.Rect(
            SCREEN_WIDTH // 2 - 220,
            420,
            440,
            42
        )

        # Các lựa chọn xuất hiện khi mở danh sách
        self.algorithm_option_rects = []

        for index in range(len(ALGORITHMS)):
            option_rect = pygame.Rect(
                self.btn_algo.x,
                self.btn_algo.bottom + index * 36,
                self.btn_algo.width,
                36
            )

            self.algorithm_option_rects.append(
                option_rect
            )

        self.btn_start = pygame.Rect(
            SCREEN_WIDTH // 2 - 150,
            500,
            300,
            50
        )

        self.btn_back = pygame.Rect(
            30,
            30,
            100,
            40
        )

    def handle_event(self, event):
        if (
            event.type != pygame.MOUSEBUTTONDOWN
            or event.button != 1
        ):
            return

        mouse_position = event.pos

        # Nút quay lại
        if self.btn_back.collidepoint(mouse_position):
            self.algorithm_list_open = False
            self.manager.switch_screen("main_menu")
            return

        # Nhấn ô thuật toán để đóng/mở danh sách
        if self.btn_algo.collidepoint(mouse_position):
            self.algorithm_list_open = (
                not self.algorithm_list_open
            )
            return

        # Nếu danh sách đang mở, ưu tiên kiểm tra lựa chọn
        if self.algorithm_list_open:
            for index, option_rect in enumerate(
                self.algorithm_option_rects
            ):
                if option_rect.collidepoint(mouse_position):
                    self.selected_algo_idx = index
                    self.algorithm_list_open = False
                    return

            # Nhấn ra ngoài thì đóng danh sách
            self.algorithm_list_open = False
            return

        # Chọn màn chơi
        for level_id, level_rect in self.level_rects.items():
            if level_rect.collidepoint(mouse_position):
                self.selected_level = level_id
                return

        # Bắt đầu chạy thuật toán
        if self.btn_start.collidepoint(mouse_position):
            selected_algorithm = (
                ALGORITHMS[self.selected_algo_idx]
            )

            self.manager.screens["gameplay"].setup_game(
                self.selected_level,
                selected_algorithm
            )

            self.manager.switch_screen("gameplay")

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(COLOR_BG)

        # Nút quay lại
        pygame.draw.rect(
            screen,
            (180, 180, 180),
            self.btn_back,
            border_radius=5
        )

        back_text = self.font.render(
            "Quay lại",
            True,
            (0, 0, 0)
        )

        screen.blit(
            back_text,
            (
                self.btn_back.x + 15,
                self.btn_back.y + 8
            )
        )

        # Tiêu đề
        title = self.font_title.render(
            "CẤU HÌNH MÀN CHƠI AI",
            True,
            COLOR_TEXT
        )

        screen.blit(
            title,
            (
                SCREEN_WIDTH // 2
                - title.get_width() // 2,
                50
            )
        )

        # Danh sách màn chơi
        for level_id, level_rect in self.level_rects.items():
            is_selected = (
                level_id == self.selected_level
            )

            background_color = (
                (100, 149, 237)
                if is_selected
                else (220, 225, 230)
            )

            text_color = (
                (255, 255, 255)
                if is_selected
                else COLOR_TEXT
            )

            pygame.draw.rect(
                screen,
                background_color,
                level_rect,
                border_radius=8
            )

            pygame.draw.rect(
                screen,
                COLOR_TEXT,
                level_rect,
                width=2 if is_selected else 1,
                border_radius=8
            )

            level_name = LEVELS[level_id]["name"]

            level_text = self.font.render(
                level_name,
                True,
                text_color
            )

            screen.blit(
                level_text,
                (
                    level_rect.x + 20,
                    level_rect.y + 18
                )
            )

        # Ô chọn thuật toán
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            self.btn_algo,
            border_radius=5
        )

        pygame.draw.rect(
            screen,
            COLOR_TEXT,
            self.btn_algo,
            width=1,
            border_radius=5
        )

        selected_algorithm = (
            ALGORITHMS[self.selected_algo_idx]
        )

        algorithm_text = self.font.render(
            f"Thuật toán: {selected_algorithm}",
            True,
            COLOR_TEXT
        )

        screen.blit(
            algorithm_text,
            (
                self.btn_algo.x + 15,
                self.btn_algo.y + 9
            )
        )

        # Mũi tên đóng/mở
        arrow = (
            "▲"
            if self.algorithm_list_open
            else "▼"
        )

        arrow_text = self.font.render(
            arrow,
            True,
            COLOR_TEXT
        )

        screen.blit(
            arrow_text,
            (
                self.btn_algo.right - 30,
                self.btn_algo.y + 9
            )
        )

        # Nút bắt đầu
        pygame.draw.rect(
            screen,
            (46, 204, 113),
            self.btn_start,
            border_radius=8
        )

        start_text = self.font_title.render(
            "BẮT ĐẦU CHẠY",
            True,
            (255, 255, 255)
        )

        screen.blit(
            start_text,
            (
                self.btn_start.centerx
                - start_text.get_width() // 2,
                self.btn_start.y + 8
            )
        )

        # Vẽ danh sách cuối cùng để nằm trên các nút khác
        if self.algorithm_list_open:
            for index, option_rect in enumerate(
                self.algorithm_option_rects
            ):
                is_selected = (
                    index == self.selected_algo_idx
                )

                background_color = (
                    (100, 149, 237)
                    if is_selected
                    else (255, 255, 255)
                )

                text_color = (
                    (255, 255, 255)
                    if is_selected
                    else COLOR_TEXT
                )

                pygame.draw.rect(
                    screen,
                    background_color,
                    option_rect
                )

                pygame.draw.rect(
                    screen,
                    COLOR_TEXT,
                    option_rect,
                    width=1
                )

                option_text = self.font.render(
                    ALGORITHMS[index],
                    True,
                    text_color
                )

                screen.blit(
                    option_text,
                    (
                        option_rect.x + 15,
                        option_rect.y + 6
                    )
                )