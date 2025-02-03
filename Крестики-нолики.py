from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import random

class Visual(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Крестики-нолики")
        self.setGeometry(700, 250, 500, 500)
        
        self.stacked_widget = QStackedWidget()
        self.logic = Logic(self)
        self.initUI()
        
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)
        
    def initUI(self):
        self.first_page()
        self.second_page()
        
    def first_page(self):
        self.page1 = QWidget()
        layout = QVBoxLayout()
        
        background_label = QLabel(self.page1)
        pixmap = QPixmap("D:/RUDN/python/project/xo.png")  # Path to first page image
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        background_label.setGeometry(0, 0, 500, 500)

        label1 = QLabel("Добро пожаловать в игру Крестики-нолики!\nЭто простая игра, в которой нужно \n заполнить три клетки в ряд одной фигурой.")
        label1.setAlignment(Qt.AlignCenter)
        label1.setStyleSheet("font-size: 18px;")
        
        label2 = QLabel("Правила:\n- Вы всегда начинаете за X.\n- Нажмите на ячейку, чтобы сделать ход.")
        label2.setAlignment(Qt.AlignCenter)
        label2.setStyleSheet("font-size: 18px;")
        
        label3 = QLabel("Режимы:\n- Легкий режим — рандомно генерирует `О` в ячейки.\n- Сложный режим — игра с искусственным интеллектом.")
        label3.setAlignment(Qt.AlignCenter)
        label3.setStyleSheet("font-size: 18px;")
        
        button_layout = QHBoxLayout()
        self.btn_easy = QPushButton("Легкий")
        self.btn_hard = QPushButton("Сложный")
        self.btn_easy.setStyleSheet("font-size: 18px;")
        self.btn_hard.setStyleSheet("font-size: 18px;")
        
        self.btn_easy.clicked.connect(lambda: self.start_game(easy=True))
        self.btn_hard.clicked.connect(lambda: self.start_game(easy=False))
        
        button_layout.addWidget(self.btn_easy)
        button_layout.addWidget(self.btn_hard)
        
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label3)
        layout.addLayout(button_layout)
        
        self.page1.setLayout(layout)
        self.stacked_widget.addWidget(self.page1)
    
    def second_page(self):
        self.page2 = QWidget()
        layout = QVBoxLayout()
        
        background_label = QLabel(self.page2)
        pixmap = QPixmap("D:/RUDN/python/project/xo2.png")  # Path to second page image
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        background_label.setGeometry(0, 0, 500, 500)

        self.label_status = QLabel("Вы играете за X. Нажмите на ячейку ниже.")
        self.label_status.setAlignment(Qt.AlignCenter)
        self.label_status.setStyleSheet("font-size: 18px;")
        
        self.grid_layout = QGridLayout()
        self.buttons = []
        for i in range(3):
            row_buttons = []
            for j in range(3):
                btn = QPushButton("")
                btn.setFixedSize(100, 100)
                btn.setStyleSheet("font-size: 18px;")
                btn.clicked.connect(lambda _, x=i, y=j: self.logic.player_move(x, y))
                self.grid_layout.addWidget(btn, i, j)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
        
        button_layout = QHBoxLayout()
        btn_back = QPushButton("Назад")
        btn_restart = QPushButton("Перезапуск")
        
        btn_back.setStyleSheet("font-size: 18px;")
        btn_restart.setStyleSheet("font-size: 18px;")
        
        btn_back.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        btn_restart.clicked.connect(self.logic.reset_game)
        
        button_layout.addWidget(btn_back)
        button_layout.addWidget(btn_restart)
        
        layout.addWidget(self.label_status)
        layout.addLayout(self.grid_layout)
        layout.addLayout(button_layout)
        
        self.page2.setLayout(layout)
        self.stacked_widget.addWidget(self.page2)
        
    def start_game(self, easy=True):
        self.logic.set_difficulty(easy)
        self.stacked_widget.setCurrentIndex(1)

class Logic:
    def __init__(self, ui):
        self.ui = ui
        self.board = [[None, None, None], [None, None, None], [None, None, None]]
        self.easy_mode = True  # Default to easy mode

    def set_difficulty(self, easy):
        self.easy_mode = easy

    def player_move(self, x, y):
        if self.board[x][y] is None:
            self.board[x][y] = 'X'
            self.ui.buttons[x][y].setText('X')
            if not self.check_winner():
                self.computer_move()

    def computer_move(self):
        if self.easy_mode:
            # Easy mode: Randomly place 'O'
            empty_cells = []
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] is None:
                        empty_cells.append((i, j))

            if empty_cells:
                x, y = random.choice(empty_cells)
                self.board[x][y] = 'O'
                self.ui.buttons[x][y].setText('O')
                self.check_winner()
        else:
            # Hard mode: Use Minimax
            best_score = -float('inf')
            best_move = None
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] is None:
                        self.board[i][j] = 'O'
                        score = self.minimax(self.board, False)
                        self.board[i][j] = None
                        if score > best_score:
                            best_score = score
                            best_move = (i, j)
            if best_move:
                x, y = best_move
                self.board[x][y] = 'O'
                self.ui.buttons[x][y].setText('O')
                self.check_winner()

    def minimax(self, board, is_maximizing):
        winner = self.get_winner()
        if winner == 'X':
            return -1  # AI wants to avoid this
        elif winner == 'O':
            return 1  # AI wants this
        elif winner == 'Ничья!':
            return 0  # Neutral outcome

        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        board[i][j] = 'O'
                        score = self.minimax(board, False)
                        board[i][j] = None
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        board[i][j] = 'X'
                        score = self.minimax(board, True)
                        board[i][j] = None
                        best_score = min(score, best_score)
            return best_score
        
    def get_winner(self):
        # Check rows and columns
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] is not None:
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] is not None:
                return self.board[0][i]

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            return self.board[0][2]

        # Check for Ничья!
        for row in self.board:
            for cell in row:
                if cell is None:
                    return None
        return 'Ничья!'

    def check_winner(self):
        winner = self.get_winner()
        if winner:
            self.ui.label_status.setText("Ничья!" if winner == 'Ничья!' else f"Победил {winner}!")
            return True
        return False

    def reset_game(self):
        self.board = [[None, None, None], [None, None, None], [None, None, None]]
        for row in self.ui.buttons:
            for btn in row:
                btn.setText("")
        self.ui.label_status.setText("Вы играете за X. Нажмите на ячейку ниже.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Visual()
    window.show()
    sys.exit(app.exec_())
