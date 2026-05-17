import random
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                             QTextEdit, QGroupBox, QRadioButton, QButtonGroup,
                             QMessageBox, QComboBox, QScrollArea, QFrame, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# переменные для игры в рулетку:
RED = "red"
BLACK = "black"
ZERO = "0"
ZEROX2 = "00"

# Цвета чисел для европейской рулетки (0-36)
EURO_COLORS = {
    0: "green",
    1: RED, 2: BLACK, 3: RED, 4: BLACK, 5: RED, 6: BLACK, 7: RED, 8: BLACK, 9: RED, 10: BLACK,
    11: BLACK, 12: RED, 13: BLACK, 14: RED, 15: BLACK, 16: RED, 17: BLACK, 18: RED,
    19: RED, 20: BLACK, 21: RED, 22: BLACK, 23: RED, 24: BLACK, 25: RED, 26: BLACK, 27: RED,
    28: BLACK, 29: RED, 30: BLACK, 31: RED, 32: BLACK, 33: RED, 34: BLACK, 35: RED, 36: BLACK
}

# Цвета чисел для американской рулетки (0, 00, 1-36)
USA_COLORS = {
    0: "green",
    "00": "green",
    1: RED, 2: BLACK, 3: RED, 4: BLACK, 5: RED, 6: BLACK, 7: RED, 8: BLACK, 9: RED, 10: BLACK,
    11: BLACK, 12: RED, 13: BLACK, 14: RED, 15: BLACK, 16: RED, 17: BLACK, 18: RED,
    19: RED, 20: BLACK, 21: RED, 22: BLACK, 23: RED, 24: BLACK, 25: RED, 26: BLACK, 27: RED,
    28: BLACK, 29: RED, 30: BLACK, 31: RED, 32: BLACK, 33: RED, 34: BLACK, 35: RED, 36: BLACK
}

BALIC = 1000

class CasinoGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.balance = BALIC
        self.current_game_widget = None  # Для отслеживания текущего виджета игры
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Казино SWAG.com')
        self.setGeometry(100, 100, 1200, 800)
        
        # Определяем шрифты
        self.bold_font = QFont("Arial", 12, QFont.Bold)
        self.title_font = QFont("Arial", 24, QFont.Bold)
        self.balance_font = QFont("Arial", 18, QFont.Bold)
        self.info_font = QFont("Arial", 16, QFont.Bold)
        self.button_font = QFont("Arial", 14, QFont.Bold)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        self.main_layout = QVBoxLayout()
        central_widget.setLayout(self.main_layout)
        
        # Заголовок
        title_label = QLabel("Добро пожаловать в Казино SWAG.com")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(self.title_font)
        title_label.setStyleSheet("color: gold; padding: 20px;")
        self.main_layout.addWidget(title_label)
        
        # Баланс
        self.balance_label = QLabel(f"💰 Баланс: {self.balance} $ 💰")
        self.balance_label.setAlignment(Qt.AlignCenter)
        self.balance_label.setFont(self.balance_font)
        self.balance_label.setStyleSheet("color: green; background-color: lightyellow; padding: 10px; border-radius: 10px;")
        self.main_layout.addWidget(self.balance_label)
        
        # Создаем контейнер для меню и игр с прокруткой
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        self.main_layout.addWidget(self.scroll_area)
        
        # Контейнер для содержимого
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.scroll_area.setWidget(self.content_widget)
        
        # Создаем главное меню
        self.create_main_menu()
        
    def create_main_menu(self):
        """Создает главное меню"""
        # Очищаем контент
        self.clear_content()
        
        # Кнопки выбора игры
        games_group = QGroupBox("ВЫБЕРИТЕ ИГРУ")
        games_group.setFont(self.button_font)
        games_group.setStyleSheet("QGroupBox { border: 2px solid gray; border-radius: 10px; margin-top: 10px; }")
        
        games_layout = QVBoxLayout()
        games_layout.setSpacing(15)
        
        # Стиль для кнопок игр
        button_style = """
            QPushButton {
                background-color: gold;
                color: black;
                font-size: 18px;
                font-weight: bold;
                padding: 15px;
                border-radius: 10px;
                border: 2px solid darkorange;
                min-height: 60px;
            }
            QPushButton:hover {
                background-color: darkorange;
                color: white;
            }
            QPushButton:pressed {
                background-color: orange;
            }
        """
        
        self.btn_roulette_eu = QPushButton("🎲 ЕВРОПЕЙСКАЯ РУЛЕТКА 🎲")
        self.btn_roulette_eu.setStyleSheet(button_style)
        self.btn_roulette_eu.clicked.connect(self.show_roulette_eu)
        games_layout.addWidget(self.btn_roulette_eu)
        
        self.btn_roulette_usa = QPushButton("🎰 АМЕРИКАНСКАЯ РУЛЕТКА 🎰")
        self.btn_roulette_usa.setStyleSheet(button_style)
        self.btn_roulette_usa.clicked.connect(self.show_roulette_usa)
        games_layout.addWidget(self.btn_roulette_usa)
        
        self.btn_russian = QPushButton("💀 РУССКАЯ РУЛЕТКА 💀")
        self.btn_russian.setStyleSheet(button_style)
        self.btn_russian.clicked.connect(self.show_russian_roulette)
        games_layout.addWidget(self.btn_russian)
        
        self.btn_twenty_one = QPushButton("🃏 ДВАДЦАТЬ ОДНО (БЛЭКДЖЕК) 🃏")
        self.btn_twenty_one.setStyleSheet(button_style)
        self.btn_twenty_one.clicked.connect(self.show_twenty_one)
        games_layout.addWidget(self.btn_twenty_one)
        
        self.btn_exit = QPushButton("❌ ВЫХОД ❌")
        self.btn_exit.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                border-radius: 10px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        self.btn_exit.clicked.connect(self.close)
        games_layout.addWidget(self.btn_exit)
        
        games_group.setLayout(games_layout)
        self.content_layout.addWidget(games_group)
        
    def clear_content(self):
        """Полностью очищает контентную область"""
        # Удаляем все виджеты из content_layout
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # Сбрасываем указатель на текущую игру
        self.current_game_widget = None
        
    def show_main_menu(self):
        """Показать главное меню"""
        self.create_main_menu()
        
    def get_color_style(self, color):
        """Возвращает стиль для кнопки числа"""
        if color == RED:
            return "background-color: #ff4444; color: white; font-weight: bold;"
        elif color == BLACK:
            return "background-color: #222222; color: white; font-weight: bold;"
        else:  # green for zero
            return "background-color: #00aa00; color: white; font-weight: bold;"
    
    def show_roulette_eu(self):
        """Показать игру Европейская рулетка"""
        self.clear_content()
        
        # Создаем виджет игры
        game_widget = QWidget()
        game_layout = QVBoxLayout(game_widget)
        
        # Кнопка возврата
        back_btn = QPushButton("◀ ВЕРНУТЬСЯ В ГЛАВНОЕ МЕНЮ")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: gray;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: darkgray;
            }
        """)
        back_btn.clicked.connect(self.show_main_menu)
        game_layout.addWidget(back_btn)
        
        # Информация
        info_label = QLabel("🎲 ЕВРОПЕЙСКАЯ РУЛЕТКА - ВЫБЕРИТЕ СТАВКУ 🎲")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setFont(self.info_font)
        info_label.setStyleSheet("color: darkblue; padding: 10px;")
        game_layout.addWidget(info_label)
        
        # Группа выбора типа ставки
        bet_type_group = QGroupBox("ТИП СТАВКИ")
        bet_type_group.setFont(self.bold_font)
        bet_type_layout = QHBoxLayout()
        
        self.bet_on_color = QRadioButton("🎨 Ставка на цвет")
        self.bet_on_number = QRadioButton("🔢 Ставка на число")
        self.bet_on_color.setChecked(True)
        
        for rb in [self.bet_on_color, self.bet_on_number]:
            rb.setFont(self.bold_font)
            bet_type_layout.addWidget(rb)
        
        bet_type_group.setLayout(bet_type_layout)
        game_layout.addWidget(bet_type_group)
        
        # Выбор цвета (изначально видим)
        self.color_group = QGroupBox("ВЫБЕРИТЕ ЦВЕТ")
        self.color_group.setFont(self.bold_font)
        color_layout = QHBoxLayout()
        
        self.red_radio = QRadioButton("🔴 КРАСНЫЙ")
        self.black_radio = QRadioButton("⚫ ЧЕРНЫЙ")
        self.red_radio.setFont(self.bold_font)
        self.black_radio.setFont(self.bold_font)
        color_layout.addWidget(self.red_radio)
        color_layout.addWidget(self.black_radio)
        self.color_group.setLayout(color_layout)
        game_layout.addWidget(self.color_group)
        
        # Выбор числа (изначально скрыт)
        self.number_group = QGroupBox("ВЫБЕРИТЕ ЧИСЛО (0-36)")
        self.number_group.setFont(self.bold_font)
        self.number_group.setVisible(False)
        
        number_grid = QGridLayout()
        number_grid.setSpacing(5)
        
        # Создаем кнопки для чисел 0-36
        self.number_buttons = []
        for i in range(37):
            btn = QPushButton(str(i))
            color = EURO_COLORS[i]
            btn.setStyleSheet(f"""
                {self.get_color_style(color)}
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
                min-width: 50px;
                min-height: 40px;
            """)
            btn.clicked.connect(lambda checked, num=i: self.select_euro_number(num))
            row = (i) // 6
            col = (i) % 6
            number_grid.addWidget(btn, row, col)
        
        self.number_group.setLayout(number_grid)
        game_layout.addWidget(self.number_group)
        
        # Поле для отображения выбранного числа
        self.selected_number_label = QLabel("Выбранное число: не выбрано")
        self.selected_number_label.setFont(self.bold_font)
        self.selected_number_label.setStyleSheet("color: blue; padding: 5px;")
        self.selected_number_label.setVisible(False)
        game_layout.addWidget(self.selected_number_label)
        
        # Ставка
        bet_layout = QHBoxLayout()
        bet_label = QLabel("💰 СТАВКА:")
        bet_label.setFont(self.bold_font)
        bet_layout.addWidget(bet_label)
        self.bet_input = QLineEdit()
        self.bet_input.setFont(self.bold_font)
        bet_layout.addWidget(self.bet_input)
        game_layout.addLayout(bet_layout)
        
        # Кнопка игры
        play_btn = QPushButton("СДЕЛАТЬ СТАВКУ")
        play_btn.setStyleSheet("""
            QPushButton {
                background-color: green;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: darkgreen;
            }
        """)
        play_btn.clicked.connect(self.play_roulette_eu)
        game_layout.addWidget(play_btn)
        
        # Результат
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFont(self.bold_font)
        game_layout.addWidget(self.result_text)
        
        # Подключаем переключение типа ставки
        self.bet_on_color.toggled.connect(self.toggle_euro_bet_type)
        self.bet_on_number.toggled.connect(self.toggle_euro_bet_type)
        
        self.content_layout.addWidget(game_widget)
        self.current_game_widget = game_widget
        self.selected_euro_number = None
    
    def toggle_euro_bet_type(self):
        """Переключение между ставкой на цвет и число"""
        if self.bet_on_color.isChecked():
            self.color_group.setVisible(True)
            self.number_group.setVisible(False)
            self.selected_number_label.setVisible(False)
        else:
            self.color_group.setVisible(False)
            self.number_group.setVisible(True)
            self.selected_number_label.setVisible(True)
    
    def select_euro_number(self, number):
        """Выбор числа в европейской рулетке"""
        self.selected_euro_number = number
        color = EURO_COLORS[number]
        color_name = "КРАСНЫЙ" if color == RED else "ЧЕРНЫЙ" if color == BLACK else "ЗЕЛЕНЫЙ"
        self.selected_number_label.setText(f"Выбранное число: {number} ({color_name})")
        self.selected_number_label.setStyleSheet(f"color: {color}; padding: 5px; font-weight: bold;")
    
    def play_roulette_eu(self):
        try:
            bet = int(self.bet_input.text())
            if bet > self.balance:
                QMessageBox.warning(self, "Ошибка", f"У вас нет столько денег! Ваш баланс: {self.balance}$")
                return
            
            # Генерируем результат
            result_number = random.randint(0, 36)
            result_color = EURO_COLORS[result_number]
            result_color_name = "КРАСНЫЙ" if result_color == RED else "ЧЕРНЫЙ" if result_color == BLACK else "ЗЕЛЕНЫЙ"
            
            win_amount = 0
            win_message = ""
            
            if self.bet_on_color.isChecked():
                # Ставка на цвет
                if not (self.red_radio.isChecked() or self.black_radio.isChecked()):
                    QMessageBox.warning(self, "Ошибка", "Выберите цвет!")
                    return
                
                choice = RED if self.red_radio.isChecked() else BLACK
                
                if choice == result_color:
                    win_amount = int(bet * 1.5)
                    self.balance += win_amount
                    win_message = f"✅🎉 ВЫ ВЫИГРАЛИ! +{win_amount}$ 🎉✅"
                else:
                    self.balance -= bet
                    win_message = f"❌😢 Вы проиграли! -{bet}$ 😢❌"
                
                self.result_text.append(f"🎲 Выпало число: {result_number} ({result_color_name})")
                self.result_text.append(win_message)
                
            else:
                # Ставка на число
                if self.selected_euro_number is None:
                    QMessageBox.warning(self, "Ошибка", "Выберите число!")
                    return
                
                if self.selected_euro_number == result_number:
                    win_amount = bet * 35
                    self.balance += win_amount
                    self.result_text.append(f"🎲 Выпало число: {result_number} ({result_color_name})")
                    self.result_text.append(f"✅🎉 ДЖЕКПОТ! ВЫ УГАДАЛИ ЧИСЛО! +{win_amount}$ 🎉✅")
                else:
                    self.balance -= bet
                    self.result_text.append(f"🎲 Выпало число: {result_number} ({result_color_name})")
                    self.result_text.append(f"❌😢 Вы не угадали число! -{bet}$ 😢❌")
            
            self.update_balance()
            self.result_text.append(f"💰 Новый баланс: {self.balance}$ 💰\n")
            self.result_text.append("="*50 + "\n")
            self.bet_input.clear()
            
            if self.balance <= 0:
                self.update_balance()
            
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректную сумму!")
    
    def show_roulette_usa(self):
        """Показать игру Американская рулетка"""
        self.clear_content()
        
        game_widget = QWidget()
        game_layout = QVBoxLayout(game_widget)
        
        # Кнопка возврата
        back_btn = QPushButton("◀ ВЕРНУТЬСЯ В ГЛАВНОЕ МЕНЮ")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: gray;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: darkgray;
            }
        """)
        back_btn.clicked.connect(self.show_main_menu)
        game_layout.addWidget(back_btn)
        
        info_label = QLabel("🎰 АМЕРИКАНСКАЯ РУЛЕТКА - ВЫБЕРИТЕ СТАВКУ 🎰")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setFont(self.info_font)
        info_label.setStyleSheet("color: darkblue; padding: 10px;")
        game_layout.addWidget(info_label)
        
        # Группа выбора типа ставки
        bet_type_group = QGroupBox("ТИП СТАВКИ")
        bet_type_group.setFont(self.bold_font)
        bet_type_layout = QHBoxLayout()
        
        self.usa_bet_on_color = QRadioButton("🎨 Ставка на цвет")
        self.usa_bet_on_number = QRadioButton("🔢 Ставка на число (0, 00, 1-36)")
        self.usa_bet_on_color.setChecked(True)
        
        for rb in [self.usa_bet_on_color, self.usa_bet_on_number]:
            rb.setFont(self.bold_font)
            bet_type_layout.addWidget(rb)
        
        bet_type_group.setLayout(bet_type_layout)
        game_layout.addWidget(bet_type_group)
        
        # Выбор цвета
        self.usa_color_group = QGroupBox("ВЫБЕРИТЕ ЦВЕТ")
        self.usa_color_group.setFont(self.bold_font)
        usa_color_layout = QHBoxLayout()
        
        self.usa_red = QRadioButton("🔴 КРАСНЫЙ")
        self.usa_black = QRadioButton("⚫ ЧЕРНЫЙ")
        self.usa_red.setFont(self.bold_font)
        self.usa_black.setFont(self.bold_font)
        usa_color_layout.addWidget(self.usa_red)
        usa_color_layout.addWidget(self.usa_black)
        self.usa_color_group.setLayout(usa_color_layout)
        game_layout.addWidget(self.usa_color_group)
        
        # Выбор числа (изначально скрыт)
        self.usa_number_group = QGroupBox("ВЫБЕРИТЕ ЧИСЛО")
        self.usa_number_group.setFont(self.bold_font)
        self.usa_number_group.setVisible(False)
        
        usa_number_grid = QGridLayout()
        usa_number_grid.setSpacing(5)
        
        # Создаем кнопки для чисел 0, 00, 1-36
        self.usa_number_buttons = []
        
        # Кнопка для 0
        btn_0 = QPushButton("0")
        btn_0.setStyleSheet(self.get_color_style("green"))
        btn_0.setFont(self.bold_font)
        btn_0.clicked.connect(lambda: self.select_usa_number(0))
        usa_number_grid.addWidget(btn_0, 0, 0, 1, 3)
        
        # Кнопка для 00
        btn_00 = QPushButton("00")
        btn_00.setStyleSheet(self.get_color_style("green"))
        btn_00.setFont(self.bold_font)
        btn_00.clicked.connect(lambda: self.select_usa_number("00"))
        usa_number_grid.addWidget(btn_00, 0, 3, 1, 3)
        
        # Кнопки для чисел 1-36
        for i in range(1, 37):
            btn = QPushButton(str(i))
            color = USA_COLORS[i]
            btn.setStyleSheet(f"""
                {self.get_color_style(color)}
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
                min-width: 50px;
                min-height: 40px;
            """)
            btn.clicked.connect(lambda checked, num=i: self.select_usa_number(num))
            row = ((i-1) // 6) + 1
            col = (i-1) % 6
            usa_number_grid.addWidget(btn, row, col)
        
        self.usa_number_group.setLayout(usa_number_grid)
        game_layout.addWidget(self.usa_number_group)
        
        # Поле для отображения выбранного числа
        self.usa_selected_number_label = QLabel("Выбранное число: не выбрано")
        self.usa_selected_number_label.setFont(self.bold_font)
        self.usa_selected_number_label.setStyleSheet("color: blue; padding: 5px;")
        self.usa_selected_number_label.setVisible(False)
        game_layout.addWidget(self.usa_selected_number_label)
        
        # Ставка
        bet_layout = QHBoxLayout()
        bet_label = QLabel("💰 СТАВКА:")
        bet_label.setFont(self.bold_font)
        bet_layout.addWidget(bet_label)
        self.usa_bet = QLineEdit()
        self.usa_bet.setFont(self.bold_font)
        bet_layout.addWidget(self.usa_bet)
        game_layout.addLayout(bet_layout)
        
        # Кнопка
        play_btn = QPushButton("СДЕЛАТЬ СТАВКУ")
        play_btn.setStyleSheet("""
            QPushButton {
                background-color: green;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: darkgreen;
            }
        """)
        play_btn.clicked.connect(self.play_roulette_usa)
        game_layout.addWidget(play_btn)
        
        self.usa_result = QTextEdit()
        self.usa_result.setReadOnly(True)
        self.usa_result.setFont(self.bold_font)
        game_layout.addWidget(self.usa_result)
        
        # Подключаем переключение типа ставки
        self.usa_bet_on_color.toggled.connect(self.toggle_usa_bet_type)
        self.usa_bet_on_number.toggled.connect(self.toggle_usa_bet_type)
        
        self.content_layout.addWidget(game_widget)
        self.current_game_widget = game_widget
        self.selected_usa_number = None
    
    def toggle_usa_bet_type(self):
        """Переключение между ставкой на цвет и число в американской рулетке"""
        if self.usa_bet_on_color.isChecked():
            self.usa_color_group.setVisible(True)
            self.usa_number_group.setVisible(False)
            self.usa_selected_number_label.setVisible(False)
        else:
            self.usa_color_group.setVisible(False)
            self.usa_number_group.setVisible(True)
            self.usa_selected_number_label.setVisible(True)
    
    def select_usa_number(self, number):
        """Выбор числа в американской рулетке"""
        self.selected_usa_number = number
        if number == "00":
            color = "green"
            color_name = "ЗЕЛЕНЫЙ"
        else:
            color = USA_COLORS[number]
            color_name = "КРАСНЫЙ" if color == RED else "ЧЕРНЫЙ" if color == BLACK else "ЗЕЛЕНЫЙ"
        self.usa_selected_number_label.setText(f"Выбранное число: {number} ({color_name})")
        self.usa_selected_number_label.setStyleSheet(f"color: {color}; padding: 5px; font-weight: bold;")
    
    def play_roulette_usa(self):
        try:
            bet = int(self.usa_bet.text())
            if bet > self.balance:
                QMessageBox.warning(self, "Ошибка", f"У вас нет столько денег! Ваш баланс: {self.balance}$")
                return
            
            # Генерируем результат
            result_number = random.choice([0, "00"] + list(range(1, 37)))
            result_color = USA_COLORS[result_number]
            result_color_name = "КРАСНЫЙ" if result_color == RED else "ЧЕРНЫЙ" if result_color == BLACK else "ЗЕЛЕНЫЙ"
            
            if self.usa_bet_on_color.isChecked():
                # Ставка на цвет
                if not (self.usa_red.isChecked() or self.usa_black.isChecked()):
                    QMessageBox.warning(self, "Ошибка", "Выберите цвет!")
                    return
                
                choice = RED if self.usa_red.isChecked() else BLACK
                
                if choice == result_color:
                    self.balance += bet
                    self.usa_result.append(f"🎰 Выпало число: {result_number} ({result_color_name})")
                    self.usa_result.append(f"✅🎉 ВЫ ВЫИГРАЛИ! +{bet}$ 🎉✅")
                else:
                    self.balance -= bet
                    self.usa_result.append(f"🎰 Выпало число: {result_number} ({result_color_name})")
                    self.usa_result.append(f"❌😢 Вы проиграли! -{bet}$ 😢❌")
            else:
                # Ставка на число
                if self.selected_usa_number is None:
                    QMessageBox.warning(self, "Ошибка", "Выберите число!")
                    return
                
                if self.selected_usa_number == result_number:
                    win_amount = bet * 35
                    self.balance += win_amount
                    self.usa_result.append(f"🎰 Выпало число: {result_number} ({result_color_name})")
                    self.usa_result.append(f"✅🎉 ДЖЕКПОТ! ВЫ УГАДАЛИ ЧИСЛО! +{win_amount}$ 🎉✅")
                else:
                    self.balance -= bet
                    self.usa_result.append(f"🎰 Выпало число: {result_number} ({result_color_name})")
                    self.usa_result.append(f"❌😢 Вы не угадали число! -{bet}$ 😢❌")
            
            self.update_balance()
            self.usa_result.append(f"💰 Новый баланс: {self.balance}$ 💰\n")
            self.usa_result.append("="*50 + "\n")
            self.usa_bet.clear()
            
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректную сумму!")
    
    def show_russian_roulette(self):
        """Показать игру Русская рулетка"""
        self.clear_content()
        
        game_widget = QWidget()
        game_layout = QVBoxLayout(game_widget)
        
        # Кнопка возврата
        back_btn = QPushButton("◀ ВЕРНУТЬСЯ В ГЛАВНОЕ МЕНЮ")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: gray;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: darkgray;
            }
        """)
        back_btn.clicked.connect(self.show_main_menu)
        game_layout.addWidget(back_btn)
        
        info_label = QLabel("💀 РУССКАЯ РУЛЕТКА - ВЫБЕРИТЕ КОЛИЧЕСТВО ВЫСТРЕЛОВ (1-4) 💀")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setFont(self.info_font)
        info_label.setStyleSheet("color: darkred; padding: 10px;")
        game_layout.addWidget(info_label)
        
        # Выбор
        choice_layout = QHBoxLayout()
        choice_label = QLabel("🔫 КОЛИЧЕСТВО ВЫСТРЕЛОВ:")
        choice_label.setFont(self.bold_font)
        choice_layout.addWidget(choice_label)
        self.shots_combo = QComboBox()
        self.shots_combo.setFont(self.bold_font)
        for i in range(1, 5):
            self.shots_combo.addItem(str(i))
        choice_layout.addWidget(self.shots_combo)
        game_layout.addLayout(choice_layout)
        
        # Ставка
        bet_layout = QHBoxLayout()
        bet_label = QLabel("💰 СТАВКА:")
        bet_label.setFont(self.bold_font)
        bet_layout.addWidget(bet_label)
        self.russian_bet = QLineEdit()
        self.russian_bet.setFont(self.bold_font)
        bet_layout.addWidget(self.russian_bet)
        game_layout.addLayout(bet_layout)
        
        # Кнопка
        play_btn = QPushButton("ИСПЫТАТЬ СУДЬБУ")
        play_btn.setStyleSheet("""
            QPushButton {
                background-color: darkred;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: red;
            }
        """)
        play_btn.clicked.connect(self.play_russian_roulette)
        game_layout.addWidget(play_btn)
        
        self.russian_result = QTextEdit()
        self.russian_result.setReadOnly(True)
        self.russian_result.setFont(self.bold_font)
        game_layout.addWidget(self.russian_result)
        
        self.content_layout.addWidget(game_widget)
        self.current_game_widget = game_widget
    
    def play_russian_roulette(self):
        try:
            shots = int(self.shots_combo.currentText())
            bet = int(self.russian_bet.text())
            
            if bet > self.balance:
                QMessageBox.warning(self, "Ошибка", f"У вас нет столько денег! Ваш баланс: {self.balance}$")
                return
            
            result = random.randint(1, 4)
            self.russian_result.append(f"🔫 Случайное число: {result}")
            
            if shots >= result:
                self.russian_result.append("💀💀💀 БАБАХ! Вы проиграли! 💀💀💀")
                self.balance -= bet
                self.update_balance()
                QMessageBox.critical(self, "Игра окончена", "💀 Вы проиграли в русскую рулетку! 💀")
                self.show_main_menu()
            else:
                win_multiplier = shots
                win = bet * win_multiplier
                self.balance += win
                self.russian_result.append(f"✅🍀 ВЫ ВЫЖИЛИ! Выигрыш: +{win}$ 🍀✅")
                self.update_balance()
            
            self.russian_result.append(f"💰 Новый баланс: {self.balance}$ 💰\n")
            self.russian_result.append("="*50 + "\n")
            self.russian_bet.clear()
            
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректную сумму!")
    
    def show_twenty_one(self):
        """Показать игру Блэкджек"""
        self.clear_content()
        
        game_widget = QWidget()
        game_layout = QVBoxLayout(game_widget)
        
        # Кнопка возврата
        back_btn = QPushButton("◀ ВЕРНУТЬСЯ В ГЛАВНОЕ МЕНЮ")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: gray;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: darkgray;
            }
        """)
        back_btn.clicked.connect(self.show_main_menu)
        game_layout.addWidget(back_btn)
        
        info_label = QLabel("🃏 ИГРА 21 (БЛЭКДЖЕК) 🃏")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setFont(self.info_font)
        info_label.setStyleSheet("color: darkgreen; padding: 10px;")
        game_layout.addWidget(info_label)
        
        # Ставка
        bet_layout = QHBoxLayout()
        bet_label = QLabel("💰 СТАВКА:")
        bet_label.setFont(self.bold_font)
        bet_layout.addWidget(bet_label)
        self.bj_bet = QLineEdit()
        self.bj_bet.setFont(self.bold_font)
        bet_layout.addWidget(self.bj_bet)
        game_layout.addLayout(bet_layout)
        
        # Кнопка
        start_btn = QPushButton("НАЧАТЬ ИГРУ")
        start_btn.setStyleSheet("""
            QPushButton {
                background-color: green;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: darkgreen;
            }
        """)
        start_btn.clicked.connect(self.start_blackjack)
        game_layout.addWidget(start_btn)
        
        self.content_layout.addWidget(game_widget)
        self.current_game_widget = game_widget
    
    def start_blackjack(self):
        try:
            self.bj_bet_amount = int(self.bj_bet.text())
            if self.bj_bet_amount > self.balance:
                QMessageBox.warning(self, "Ошибка", f"У вас нет столько денег! Ваш баланс: {self.balance}$")
                return
            if self.bj_bet_amount <= 0:
                QMessageBox.warning(self, "Ошибка", "Ставка должна быть положительной!")
                return
            
            self.play_blackjack()
            
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректную сумму!")
    
    def play_blackjack(self):
        CARD_VALUES = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
            '7': 7, '8': 8, '9': 9, '10': 10,
            'Валет': 10, 'Дама': 10, 'Король': 10, 'Туз': None
        }
        
        CARD_NAMES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 
                      'Валет', 'Дама', 'Король', 'Туз']
        
        def get_deck():
            deck = []
            for _ in range(4):
                for card in CARD_NAMES:
                    deck.append(card)
            random.shuffle(deck)
            return deck
        
        def calculate_score(hand):
            score = 0
            aces = 0
            
            for card in hand:
                if card == 'Туз':
                    aces += 1
                    score += 11
                else:
                    score += CARD_VALUES[card]
            
            while score > 21 and aces > 0:
                score -= 10
                aces -= 1
            
            return score
        
        self.clear_content()
        
        game_widget = QWidget()
        game_layout = QVBoxLayout(game_widget)
        
        # Кнопка возврата
        back_btn = QPushButton("◀ ВЕРНУТЬСЯ В ГЛАВНОЕ МЕНЮ")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: gray;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: darkgray;
            }
        """)
        back_btn.clicked.connect(self.show_main_menu)
        game_layout.addWidget(back_btn)
        
        deck = get_deck()
        player_hand = []
        dealer_hand = []
        
        player_hand.append(deck.pop())
        dealer_hand.append(deck.pop())
        player_hand.append(deck.pop())
        dealer_hand.append(deck.pop())
        
        # Интерфейс игры
        game_info = QLabel("🃏 ИГРА 21 (БЛЭКДЖЕК) 🃏")
        game_info.setAlignment(Qt.AlignCenter)
        game_info.setFont(self.info_font)
        game_info.setStyleSheet("color: darkgreen; padding: 10px;")
        game_layout.addWidget(game_info)
        
        player_label = QLabel(f"🎴 ВАШИ КАРТЫ: {', '.join(player_hand)}")
        player_label.setFont(self.bold_font)
        game_layout.addWidget(player_label)
        
        player_score_label = QLabel(f"📊 ВАШИ ОЧКИ: {calculate_score(player_hand)}")
        player_score_label.setFont(self.bold_font)
        game_layout.addWidget(player_score_label)
        
        dealer_label = QLabel(f"🎴 КАРТЫ ДИЛЕРА: [?], {dealer_hand[1]}")
        dealer_label.setFont(self.bold_font)
        game_layout.addWidget(dealer_label)
        
        # Кнопки действий
        actions_layout = QHBoxLayout()
        hit_btn = QPushButton("ВЗЯТЬ КАРТУ")
        stand_btn = QPushButton("ОСТАНОВИТЬСЯ")
        
        for btn in [hit_btn, stand_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: orange;
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: darkorange;
                }
            """)
            btn.setFont(self.bold_font)
        
        actions_layout.addWidget(hit_btn)
        actions_layout.addWidget(stand_btn)
        game_layout.addLayout(actions_layout)
        
        bj_log = QTextEdit()
        bj_log.setReadOnly(True)
        bj_log.setFont(self.bold_font)
        game_layout.addWidget(bj_log)
        
        self.content_layout.addWidget(game_widget)
        
        # Сохраняем переменные для использования в функциях
        self.current_deck = deck
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.player_label = player_label
        self.player_score_label = player_score_label
        self.dealer_label = dealer_label
        self.hit_btn = hit_btn
        self.stand_btn = stand_btn
        self.bj_log = bj_log
        
        # Временно сохраняем функции
        self.calculate_score = calculate_score
        
        # Привязываем действия
        hit_btn.clicked.connect(lambda: self.blackjack_hit())
        stand_btn.clicked.connect(lambda: self.blackjack_stand())
    
    def blackjack_hit(self):
        new_card = self.current_deck.pop()
        self.player_hand.append(new_card)
        self.bj_log.append(f"📤 Вы взяли: {new_card}")
        
        self.player_label.setText(f"🎴 ВАШИ КАРТЫ: {', '.join(self.player_hand)}")
        player_score = self.calculate_score(self.player_hand)
        self.player_score_label.setText(f"📊 ВАШИ ОЧКИ: {player_score}")
        
        if player_score > 21:
            self.bj_log.append("💀💀💀 ПЕРЕБОР! Вы проиграли! 💀💀💀")
            self.balance -= self.bj_bet_amount
            self.update_balance()
            self.hit_btn.setEnabled(False)
            self.stand_btn.setEnabled(False)
            QMessageBox.information(self, "Результат", f"Вы проиграли! Ваш баланс: {self.balance}$")
        elif player_score == 21:
            self.bj_log.append("🎉 У ВАС 21 ОЧКО! 🎉")
            self.blackjack_stand()
    
    def blackjack_stand(self):
        self.hit_btn.setEnabled(False)
        self.stand_btn.setEnabled(False)
        
        self.bj_log.append("\n--- ХОД ДИЛЕРА ---")
        player_score = self.calculate_score(self.player_hand)
        
        # Ход дилера
        dealer_score = self.calculate_score(self.dealer_hand)
        self.dealer_label.setText(f"🎴 КАРТЫ ДИЛЕРА: {', '.join(self.dealer_hand)}")
        
        while dealer_score < 17:
            new_card = self.current_deck.pop()
            self.dealer_hand.append(new_card)
            self.bj_log.append(f"📤 Дилер взял: {new_card}")
            dealer_score = self.calculate_score(self.dealer_hand)
            self.dealer_label.setText(f"🎴 КАРТЫ ДИЛЕРА: {', '.join(self.dealer_hand)}")
        
        # Определение победителя
        self.bj_log.append("\n=== РЕЗУЛЬТАТ ===")
        self.bj_log.append(f"📊 ВАШИ ОЧКИ: {player_score}")
        self.bj_log.append(f"📊 ОЧКИ ДИЛЕРА: {dealer_score}")
        
        if dealer_score > 21:
            self.bj_log.append("✅🎉 У ДИЛЕРА ПЕРЕБОР! ВЫ ВЫИГРАЛИ! 🎉✅")
            self.balance += self.bj_bet_amount
        elif player_score > dealer_score:
            self.bj_log.append("✅🎉 ПОЗДРАВЛЯЮ! ВЫ ВЫИГРАЛИ! 🎉✅")
            self.balance += self.bj_bet_amount
        elif player_score < dealer_score:
            self.bj_log.append("❌😢 ВЫ ПРОИГРАЛИ! 😢❌")
            self.balance -= self.bj_bet_amount
        else:
            self.bj_log.append("🤝 НИЧЬЯ! Ставка возвращена. 🤝")
        
        self.update_balance()
        
        QMessageBox.information(self, "Результат игры", f"Игра окончена! Ваш баланс: {self.balance}$")
    
    def update_balance(self):
        self.balance_label.setText(f"💰 Баланс: {self.balance} $ 💰")
        if self.balance <= 0:
            reply = QMessageBox.question(self, "Игра окончена", 
                                        "У вас закончились деньги! Хотите начать заново?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.balance = BALIC
                self.update_balance()
                self.show_main_menu()
            else:
                self.close()

def main():
    app = QApplication(sys.argv)
    window = CasinoGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()