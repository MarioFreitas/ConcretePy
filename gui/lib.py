from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from itertools import cycle


def get_text(obj):
    """
    This function takes a GUI child widget that contains text and returns the text as string.
    :param obj: Any text yielding widget
    :return: Widget's text (str)
    """
    if str(type(obj)) == "<class 'PyQt5.QtWidgets.QLineEdit'>":
        if obj.text() == '':
            return obj.placeholderText()
        else:
            return obj.text()
    elif str(type(obj)) == "<class 'PyQt5.QtWidgets.QTextEdit'>":
        return obj.toPlainText()
    elif str(type(obj)) == "<class 'PyQt5.QtWidgets.QListWidget'>":
        return obj.currentItem().text()
    elif str(type(obj)) == "<class 'PyQt5.QtWidgets.QComboBox'>":
        return obj.currentText()
    elif str(type(obj)) == "<class 'PyQt5.QtWidgets.QTableWidgetItem'>":
        return obj.text()


def get_enabled(obj):
    if obj.isEnabled():
        return get_text(obj)
    else:
        return None


class MplWidget(QWidget):
    def __init__(self, parent=None):
        super(MplWidget, self).__init__(parent)

        self.mplCanvas = MplCanvas(self)
        self.mpl_toolbar = NavigationToolbar(self.mplCanvas, self)
        self.gridLabel = QLabel('Show Grid', self)
        self.gridChkBox = QCheckBox(self)
        self.gridChkBox.stateChanged.connect(self.grid_toggle)

        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(self.mplCanvas, 1, 1, 1, 3)
        self.gridLayout.addWidget(self.gridLabel, 2, 1)
        self.gridLayout.addWidget(self.gridChkBox, 2, 2)
        self.gridLayout.addWidget(self.mpl_toolbar, 2, 3)

        self.setLayout(self.gridLayout)

    def grid_toggle(self):
        self.mplCanvas.axes.grid(self.gridChkBox.isChecked())
        self.mplCanvas.draw()


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot_momento(self, x, m):
        self.axes.cla()

        cycol = cycle('brgcmk')
        self.axes.plot(x, -m/1e3, c=next(cycol), label='Momento Fletor')

        self.axes.legend(fontsize=11)
        self.axes.set_title('Diagrama de Momento Fletor')

        self.axes.set_xlabel('x (m)')
        self.axes.set_ylabel('Momento Fletor (kN.m)')
        self.fig.tight_layout()
        self.draw()
