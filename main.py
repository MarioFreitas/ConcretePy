from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
from gui.mainWindowGUI import Ui_MainWindow
from gui.lib import *
from ConcretePy.Concrete.configurações import Configurações
from ConcretePy.Concrete.inputData import InputData
from ConcretePy.Concrete.laje import Laje


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Ajustes Visuais
        self.setupUi(self)
        self.setWindowIcon(QIcon('./img/icon_64.ico'))

        # InputData
        self.inputData = InputData()

        # Ações
        self.actionSair.triggered.connect(sys.exit)
        self.actionDevelopment_Tool.triggered.connect(self.dev_tool)

        # Botões
        self.add_btn_carac_laje.clicked.connect(self.add_laje)
        self.remov_btn__carac_laje.clicked.connect(self.remove_laje)

        # DEBUG OPTIONS
        DEBUG = True
        if DEBUG:
            self.lx_le_carac_laje.setText('400')
            self.ly_le_carac_laje.setText('400')
            self.h_le_carac_laje.setText('12')
            self.espessura_revest_sup_le_carg_laje.setText('0.7')
            self.peso_revest_sup_le_carg_laje.setText('18')
            self.espessura_revest_inf_le_carg_laje.setText('1.5')
            self.peso_revest_inf_le_carg_laje.setText('12.5')
            self.espessura_contrap_le_carg_laje.setText('1.5')
            self.peso_contrap_le_carg_laje.setText('21')
            self.espessura_parede_le_carg_laje.setText('15')
            self.perimetro_parede_le_carg_laje.setText('200')
            self.altura_parede_le_carg_laje.setText('260')
            self.utiliz_le_carg_laje.setText('2')

        self.showMaximized()

    def check_error01(self, tuple):
        for i in tuple:
            try:
                float(i)
            except ValueError:
                icon = QStyle.SP_MessageBoxWarning
                self.error01 = QMessageBox()
                self.error01.setText('Preencha os campos de texto com números reais')
                self.error01.setWindowTitle('Erro 01')
                self.error01.setWindowIcon(self.error01.style().standardIcon(icon))
                self.error01.setIcon(QMessageBox.Warning)
                self.error01.show()
                return False
        return True

    def add_laje(self):
        numero = get_text(self.nlaje_cbox_carac_laje)
        lx = get_text(self.lx_le_carac_laje)
        ly = get_text(self.ly_le_carac_laje)
        h = get_text(self.h_le_carac_laje)
        apoio = get_text(self.apoio_cbox_carac_laje)
        apoio = apoio.split(' ')[0:2]
        apoio = ' '.join(apoio)

        if not self.check_error01((lx, ly, h)):
            return

        numero = int(numero)
        lx = float(lx) / 100
        ly = float(ly) / 100
        h = float(h) / 100

        self.inputData.lajes.update({numero: Laje(numero, lx, ly, h, apoio, self.inputData.config)})

        if self.nlaje_cbox_carac_laje.currentIndex() + 1 == self.nlaje_cbox_carac_laje.count():
            self.nlaje_cbox_carac_laje.addItem(str(int(get_text(self.nlaje_cbox_carac_laje)) + 1))
            self.nlaje_cbox_carg_laje.addItem(str(int(get_text(self.nlaje_cbox_carac_laje))))
            self.nlaje_cbox_momento_laje.addItem(str(int(get_text(self.nlaje_cbox_carac_laje))))
            self.nlaje_cbox_dim_laje.addItem(str(int(get_text(self.nlaje_cbox_carac_laje))))
            self.nlaje_cbox_carac_laje.setCurrentIndex(self.nlaje_cbox_carac_laje.currentIndex() + 1)
        else:
            self.nlaje_cbox_carac_laje.setCurrentIndex(self.nlaje_cbox_carac_laje.currentIndex() + 1)

        self.update_carac_laje_text()

    def remove_laje(self):
        if self.nlaje_cbox_carac_laje.currentIndex() + 1 == self.nlaje_cbox_carac_laje.count() - 1:
            numero = int(get_text(self.nlaje_cbox_carac_laje))
            self.inputData.lajes.pop(numero)
            self.nlaje_cbox_carac_laje.removeItem(numero)
            self.nlaje_cbox_carg_laje.removeItem(numero - 1)
            self.nlaje_cbox_dim_laje.removeItem(numero - 1)
            self.nlaje_cbox_momento_laje.removeItem(numero - 1)
            self.update_carac_laje_text()
        else:
            icon = QStyle.SP_MessageBoxWarning
            self.msgRemoveStory = QMessageBox()
            self.msgRemoveStory.setText('Remova primeiro a última laje adicionada.')
            self.msgRemoveStory.setWindowTitle('Erro de Remoção')
            self.msgRemoveStory.setWindowIcon(self.msgRemoveStory.style().standardIcon(icon))
            self.msgRemoveStory.show()

    def update_carac_laje_text(self):
        s = ''

        for i in range(1, len(self.inputData.lajes) + 1):
            laje = self.inputData.lajes[i]
            s += 'Laje {}\nlx = {} m\nly = {} m\nh = {} cm\nTipo de apoio: {}\n\n'.format(laje.numero, laje.lx, laje.ly,
                                                                                          laje.h * 100, laje.apoio)

        self.textBrowser_carc_laje.setText(s)

    def dev_tool(self):
        self.devDialog = QWidget()

        self.devDialog.setGeometry(300, 300, 800, 200)
        self.devDialog.setWindowTitle('Development Tool')

        self.devDialog.textEdit = QTextEdit(self)
        self.devDialog.btn = QPushButton('Executar', self)
        self.devDialog.btn.clicked.connect(self.dev_tool_exec)
        self.devDialog.layout = QGridLayout()
        self.devDialog.layout.addWidget(self.devDialog.textEdit, 1, 1)
        self.devDialog.layout.addWidget(self.devDialog.btn, 2, 1)
        self.devDialog.setLayout(self.devDialog.layout)

        # s = 'compare_anal_sol(1)'
        # self.devDialog.textEdit.setText(s)

        self.devDialog.show()

    def dev_tool_exec(self):
        exec(get_text(self.devDialog.textEdit))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = MainWindow()
    sys.exit(app.exec_())
