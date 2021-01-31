import sys
from Main2 import *
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import *  # убрать при сдаче


# from PyQt5 import Q

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Main2.ui', self)  # Загружаем дизайн
        self.Id_button.clicked.connect(self.Init_Group)
        self.Date_button.clicked.connect(self.statistic_start)
        # Обратите внимание: имя элемента такое же как в QTDesigner



    def Init_Group(self):
        self.Loading.setText('Загрузка...')
        self.group = Group(int(self.Group_id.text()), self)
        self.Loading.setText(' ')

    def statistic_start(self):
        time_from = self.Date_from.text().split('.')
        time_to = self.Date_to.text().split('.')
        self.Return.setText(self.group.statistic(time_from, time_to))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    try:
        sys.exit(app.exec_())
    except Exception:
        print('ex')
