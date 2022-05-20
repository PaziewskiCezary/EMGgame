from emg_games.gui.components import Button
from emg_games.gui.components import palette


def add_corner_button(func, text, x_screen, y_screen, screen, loc='right',  func_args={}):
    y_button = y_screen // 20
    if loc == 'right':
        x_button = int(19 / 20 * x_screen)
    elif loc == 'left':
        x_button = x_screen // 20
    else:
        raise AttributeError('Loc in add_corner_button must be "left" or "right"')
    button_font_size = y_screen // 18
    return_btn = Button(screen, text, (x_button, y_button), ((x_screen // 20) * 2, y_button * 2),
                        button_color=palette.SECONDARY_COLOR, label_color=palette.PRIMARY_COLOR, func=func,
                        font_size=button_font_size, func_args=func_args)
    
    return return_btn
