import os
from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import messagebox
import config as cfg
import threading
from nalog_functions import *
import requests


class AqsiWindow:
    '''
    Класс AqsiWindow описывает шаблон графического интерфейса программы
    '''

    def __init__(self, width=1200, height=600, title="aqsi_helper", resizable=(False, False),
                 icon=None, back_image=None):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}+{(self.root.winfo_screenwidth() - width)//2}+"
                               f"{(self.root.winfo_screenheight() - height)// 2}")
        self.root.resizable(resizable[0], resizable[1])
        if icon:
            self.root.iconbitmap(icon)
        if back_image:
            self.background = PhotoImage(file=f"{back_image}")
            Label(self.root, image=self.background).pack()
        # Текст до кнопок
        self.Label_1 = Label(self.root, text="Выберите действие", bg='white', fg='black', font=('Times New Roman', 24))
        # Создание кнопок
        self.start_btn = Button(self.root, text='Проверка', font=('Times New Roman', 20), bg='#4dd152', relief=RAISED,
                                bd='6', command=self.start)
        self.quit_btn = Button(self.root, text='Выход', font=('Times New Roman', 20), bg='#f04d4d', relief=RAISED,
                                bd='6', command=self.root.destroy)

        # Создание фреймов для полей ввода/вывода
        self.input_frame = Frame(self.root)
        self.output_frame = Frame(self.root)
        # Создание полей ввыода/вывода
        self.input_text_field = Text(wrap='word', font=('Times New Roman', 14))
        self.output_text_field = Text(wrap='word', font=('Times New Roman', 14))
        # Создание скроллов
        self.scroll_input = Scrollbar(self.root, command=self.input_text_field.yview)
        self.scroll_output = Scrollbar(self.root, command=self.output_text_field.yview)
        # Текст над полями ввода/вывода
        self.Label_2 = Label(self.root, text="Поле ввода SN", bg='white', fg='black', font=('Times New Roman', 16))
        self.Label_3 = Label(self.root, text="Результат", bg='white', fg='black', font=('Times New Roman', 16))
        # Создание progressbar
        self.pgbar = Progressbar(self.root, orient='horizontal', mode='indeterminate', length=300)
        # Вспомогательная переменная для хранения списка SN
        self.aqsi_list = []
        self.root.event_add('<<Paste>>', '<Control-igrave>')
        self.root.event_add("<<Copy>>", "<Control-ntilde>")


    def draw_widjets(self):
        '''
        Функция draw_widjets размещает созданные виджеты в окне программы
        '''
        self.Label_1.place(relx=0.5, rely=0.2, anchor='center')
        self.start_btn.place(relx=0.5, rely=0.4, anchor='center', width='180', height='60')
        self.quit_btn.place(relx=0.5, rely=0.65, anchor='center', width='120', height='50')
        self.input_frame.place(relx=0.2, rely=0.5, width='310', height='480', anchor='center')
        self.output_frame.place(relx=0.8, rely=0.5, width='310', height='480', anchor='center')
        self.scroll_input.pack(in_=self.input_frame, fill='y', side='right')
        self.scroll_output.pack(in_=self.output_frame, fill='y', side='right')
        self.input_text_field.pack(in_=self.input_frame, fill='y', side='left')
        self.output_text_field.pack(in_=self.output_frame, fill='y', side='left')
        self.input_text_field.config(yscrollcommand=self.scroll_input.set)
        self.output_text_field.config(yscrollcommand=self.scroll_output.set)
        self.Label_2.place(relx=0.2, rely=0.05, anchor='center')
        self.Label_3.place(relx=0.8, rely=0.05, anchor='center')
        self.pgbar.place(relx=0.5, rely=0.8, width=400, height=50, anchor='n')

    def main_check(self):
        '''
        Функция main_check описывает основной процесс всей программы. Последовательно вызываются функции,
        описанные в файле nalog_functions.py
        '''

        # Считываем текст из поля ввода в функцию read_aqsi_list, на выходе которой получаем список найденных серийных
        # номеров AQSI
        self.aqsi_list = read_aqsi_list(self.input_text_field.get('1.0', 'end'))
        # Если серийные номера не найдены, сообщаем об этом пользователю
        if not self.aqsi_list:
            self.pgbar.stop()
            messagebox.showwarning("Warning", "Вы не ввели ни одного серийного номера AQSI")
        else:
            # Функция get_nalog_info осуществляет проверку терминалов в налоговой. Возвращает словарь
            # {серийный номер : результат проверки}
            aqsi_res_dict = get_nalog_info(self.aqsi_list)
            # Если функция вернула сообщение о недоступности сервиса, сообщаем об этом пользователю
            if aqsi_res_dict == 'Сервер временно недоступен':
                self.pgbar.stop()
                messagebox.showwarning("Warning", "Сервер временно недоступен")
            else:
                # Удаляем текст из поля вывода результатов проверки
                self.output_text_field.delete('1.0', 'end')
                # Выводим строку исправных, неисправных и не обнаруженных терминалов,
                # формируемую в функции print_check_str из словаря.
                self.output_text_field.insert('1.0', print_check_str(aqsi_res_dict))
        self.pgbar.stop()
        # Возвращаем кликабельность кнопке "Проверка"
        self.start_btn['state'] = 'normal'

    def start(self):
        '''
        Функция start вызывается при нажатии кнопки "Проверка".
        '''
        # Блокировка кнопки "Проверка"
        self.start_btn['state'] = 'disable'
        # Запуск прогрессбара
        self.pgbar.start(10)
        # Запуск функции main в отдельном потоке
        threading.Thread(target=self.main_check).start()

    def run(self):
        # Функция запуска работы объекта класса
        self.draw_widjets()
        self.root.mainloop()


# Класс для создания окна ввода логина и пароля для подключения к прокси
class AuthWin:

    def __init__(self):
        # Создаём окно запроса пароля пользователя
        self.auth_win = Tk()
        self.auth_win.title('Авторизация')
        self.auth_win.geometry(f"300x160+{self.auth_win.winfo_screenwidth()//2-150}+"
                               f"{self.auth_win.winfo_screenheight()//2-50}")
        self.auth_win.resizable(False, False)
        # Текст до полей ввода
        self.offer_text_label = Label(self.auth_win, text="   Введите данные учетной записи: ", fg='black',
                                      font=('Times New Roman', 14))
        self.login_text_label = Label(self.auth_win, text="Логин:", fg='black', font=('Times New Roman', 12))
        self.login_entry = Entry(self.auth_win, width=25, font=('Times New Roman', 12))
        self.password_text_label = Label(self.auth_win, text="Пароль:", fg='black', font=('Times New Roman', 12))
        self.password_entry = Entry(self.auth_win, width=25, show='*', font=('Times New Roman', 12))
        # Кнопки подтверждения и отмены с соответствующими фукнциями
        self.ok_button = Button(self.auth_win, text='Ок', font=('Times New Roman', 12), bg='#68e3e3', relief=RAISED,
                                bd='3', width=10, command=self.enter_data)
        self.cancel_button = Button(self.auth_win, text='Отмена', font=('Times New Roman', 12), bg='#ed6f6f', relief=RAISED,
                                bd='3', width=10, command=self.auth_win.quit)

    def draw_widjets(self):
        self.offer_text_label.grid(row=0, column=0, columnspan=4)
        self.login_text_label.grid(row=1, column=0, pady=10)
        self.login_entry.grid(row=1, column=1, columnspan=3)
        # Добавляем текст "по-умолчанию" - логин пользователя из модуля "os":
        self.login_entry.insert(0, os.getlogin())
        self.password_text_label.grid(row=2, column=0, pady=10)
        self.password_entry.grid(row=2, column=1, columnspan=3)
        self.password_entry.focus()
        self.ok_button.grid(row=3, column=1)
        self.cancel_button.grid(row=3, column=3)

    # Функция ввода лоигна и пароля пользователя
    def enter_data(self):
        # Цикл запроса логин/пароля итеррирует до тех пор, пока тестовый запрос (строка 176) не даст положительный результат
        while not cfg.check_flag:
            cfg.domain_name = self.login_entry.get()
            cfg.password = self.password_entry.get()
            proxy = {"http": cfg.HTTP_PROXY_URL, "https": cfg.HTTPS_PROXY_URL}
            payload = ""
            headers = {
                "User-Agent": "PostmanRuntime/7.28.4",
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive"
            }
            s = requests.Session()
            # s.proxies = proxy
            response = s.get(cfg.NALOG_URL, headers=headers, params={"factory_number": "1006117069023371",
                                                            "model_code": "0127"}, data=payload)
            if response.ok:
                cfg.check_flag = True
                self.auth_win.destroy()
            else:
                messagebox.showwarning("Warning", "Неверные логин или пароль")

    def run(self):
        self.draw_widjets()
        self.auth_win.mainloop()


if __name__ == "__main__":
    win = AqsiWindow(icon="aqsi_icon.ico", back_image="aqsi_bg_short.png")
    win.run()
