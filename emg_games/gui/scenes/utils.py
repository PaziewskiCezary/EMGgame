from emg_games.gui.components import Button
from emg_games.gui.components import palette

def add_corner_button(func, text, x_screen, y_screen, screen):
        x_button, y_button = x_screen // 20, y_screen // 20
        button_font_size = y_screen // 18
        return_btn = Button(screen, text, (x_button, y_button), (x_button * 2, y_button * 2),
                            button_color=palette.SECONDARY_COLOR, label_color=palette.PRIMARY_COLOR, func=func,
                            font_size=button_font_size)
        
        return return_btn