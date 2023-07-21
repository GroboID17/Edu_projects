from aqsi_tkinter_class import AqsiWindow, AuthWin
import config as cfg

if __name__ == "__main__":
    cfg.check_flag = False
    # Создание окна аутентификации
    awin = AuthWin()
    awin.run()
    # Создание окна программы по шаблону из класса (со всем функционалом)
    if cfg.check_flag:
        win = AqsiWindow(icon="aqsi_icon.ico", back_image="aqsi_bg_short.png")
        win.run()











