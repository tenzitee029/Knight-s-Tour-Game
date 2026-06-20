import pygame
from config import COLOR_BG, COLOR_TEXT, SCREEN_WIDTH, SCREEN_HEIGHT

class MainMenu:
    def __init__(self, manager):
        self.manager = manager
        self.font_title = pygame.font.SysFont("Times New Roman", 50, bold=True)
        self.font_btn = pygame.font.SysFont("Times New Roman", 24)
        
        # Định nghĩa các nút bấm
        self.btn_play = pygame.Rect(SCREEN_WIDTH//2 - 150, 250, 300, 50)
        self.btn_history = pygame.Rect(SCREEN_WIDTH//2 - 150, 330, 300, 50)
        self.btn_exit = pygame.Rect(SCREEN_WIDTH//2 - 150, 410, 300, 50)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if self.btn_play.collidepoint(mouse_pos):
                self.manager.switch_screen("level_select")
            elif self.btn_history.collidepoint(mouse_pos):
                self.manager.switch_screen("history")
            elif self.btn_exit.collidepoint(mouse_pos):
                pygame.quit()
                exit()

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(COLOR_BG)
        
        # Vẽ tiêu đề
        title_surf = self.font_title.render("KNIGHT'S TOUR AI", True, COLOR_TEXT)
        screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 100))
        
        # Vẽ các nút bấm
        for btn, text in [(self.btn_play, "CHỌN LEVEL"), (self.btn_history, "LỊCH SỬ"), (self.btn_exit, "THOÁT")]:
            pygame.draw.rect(screen, (200, 214, 229), btn, border_radius=8)
            pygame.draw.rect(screen, COLOR_TEXT, btn, width=2, border_radius=8)
            txt_surf = self.font_btn.render(text, True, COLOR_TEXT)
            screen.blit(txt_surf, (btn.x + btn.width//2 - txt_surf.get_width()//2, btn.y + btn.height//2 - txt_surf.get_height()//2))