import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from ui.manager import ScreenManager

def main():
    pygame.init()
    pygame.font.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Knight's Tour")
    clock = pygame.time.Clock()
    
    manager = ScreenManager()
    running = True
    
    while running:
        # Giới hạn tốc độ Frame
        clock.tick(FPS)
        
        # Xử lý tất cả các sự kiện (Click chuột, phím bấm, tắt admin...)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Truyền sự kiện vào manager để xử lý chuyển màn hình/click nút
            manager.handle_event(event)
            
        # Cập nhật logic toán học & Trực quan vẽ giao diện
        manager.update()
        manager.draw(screen)
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()