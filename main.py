import sys


from PyQt5.QtWidgets import QApplication, QMainWindow

from design.design import Ui_MainWindow
import os


class Morph(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # buttons
        self.btn_process.clicked.connect(self.process)
        self.btn_to_black.clicked.connect(self.to_black)
        self.btn_clear.clicked.connect(self.clear)

        # menu buttons
        self.action_open.triggered.connect(self.open_image)
        self.action_save.triggered.connect(self.save_image)

    def process(self):
        self.label_status.setText("Статус")

    def to_black(self):
        pass

    def clear(self):
        pass

    def open_image(self):
        pass

    def save_image(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MorphologicalProcess = Morph()
    MorphologicalProcess.show()
    sys.exit(app.exec_())
