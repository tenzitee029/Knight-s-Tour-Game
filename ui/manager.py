from ui.screens.main_menu import MainMenu
from ui.screens.level_select import LevelSelect
from ui.screens.gameplay import Gameplay
from ui.screens.history import HistoryScreen

class ScreenManager:
    def __init__(self):
        self.screens = {
            "main_menu": MainMenu(self),
            "level_select": LevelSelect(self),
            "gameplay": Gameplay(self),
            "history": HistoryScreen(self)
        }
        self.current_screen = self.screens["main_menu"]

    def switch_screen(self, screen_name):
        self.current_screen = self.screens[screen_name]

    def handle_event(self, event):
        self.current_screen.handle_event(event)

    def update(self):
        self.current_screen.update()

    def draw(self, screen):
        self.current_screen.draw(screen)