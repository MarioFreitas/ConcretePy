from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
from gui.mainWindowGUI import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.setWindowIcon(QIcon('./img/icon_64.ico'))

        self.showMaximized()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = MainWindow()
    sys.exit(app.exec_())