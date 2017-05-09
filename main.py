from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import re
import sys
import pickle
from ConcretePy.gui.mainWindowGUI import Ui_MainWindow
from ConcretePy.gui.lib import *
from ConcretePy.Concrete.inputData import InputData
from ConcretePy.Concrete.outputData import OutputData
from ConcretePy.Concrete.laje import Laje
from ConcretePy.Concrete.viga import Viga


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Ajustes Visuais
        self.setupUi(self)
        self.setWindowIcon(QIcon('./img/icon_64.ico'))
        qss = self.open_qss('./gui/css/darkBlue/style.qss')
        # self.setStyleSheet(qss)
        app.setStyleSheet(qss)

        # InputData / OutputData
        self.inputData = InputData()
        self.outputData = OutputData()
        self.file = None
        self.fileName = None

        # Ajustes da GUI e Conexões
        self.init_menus()
        self.init_lajes()
        self.init_vigas()
        self.init_pilares()

        self.show()

        # DEBUG OPTIONS
        DEBUG = True
        if DEBUG:
            ### Lajes ###
            # Caracterização
            self.lx_le_carac_laje.setText('400')
            self.ly_le_carac_laje.setText('800')
            self.h_le_carac_laje.setText('12')
            self.apoio_cbox_carac_laje.setCurrentIndex(2)
            self.add_btn_carac_laje.click()
            self.apoio_cbox_carac_laje.setCurrentIndex(3)
            self.lx_le_carac_laje.setText('400')
            self.ly_le_carac_laje.setText('400')
            self.add_btn_carac_laje.click()
            self.lx_le_carac_laje.setText('400')
            self.ly_le_carac_laje.setText('400')
            self.add_btn_carac_laje.click()

            # Cargas
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
            self.add_btn_carg_laje.click()
            self.add_btn_carg_laje.click()
            self.add_btn_carg_laje.click()

            # Reações
            self.vx_le_reac_laje.setText('4.38')
            self.v_x_le_reac_laje.setText('6.25')
            self.vy_le_reac_laje.setText('1.83')
            self.v_y_le_reac_laje.setDisabled(True)
            self.add_btn_reac_laje.click()
            self.v_y_le_reac_laje.setDisabled(False)
            self.vx_le_reac_laje.setText('2.17')
            self.v_x_le_reac_laje.setText('3.17')
            self.vy_le_reac_laje.setText('2.17')
            self.v_y_le_reac_laje.setText('3.17')
            self.add_btn_reac_laje.click()
            self.vx_le_reac_laje.setText('2.17')
            self.v_x_le_reac_laje.setText('3.17')
            self.vy_le_reac_laje.setText('2.17')
            self.v_y_le_reac_laje.setText('3.17')
            self.add_btn_reac_laje.click()

            # Momentos
            self.lambda_le_momento_laje.setText('1')
            self.mx_le_momento_laje.setText('7.03')
            self.my_le_momento_laje.setText('1.48')
            self.nx_le_momento_laje.setText('12.5')
            # self.nx_le_momento_laje.setDisabled(True)
            self.ny_le_momento_laje.setDisabled(True)
            self.add_btn_momento_laje.click()
            self.mx_le_momento_laje.setText('2.69')
            self.nx_le_momento_laje.setText('6.99')
            self.my_le_momento_laje.setText('2.69')
            self.ny_le_momento_laje.setText('6.99')
            self.ny_le_momento_laje.setDisabled(False)
            self.add_btn_momento_laje.click()
            self.mx_le_momento_laje.setText('2.69')
            self.nx_le_momento_laje.setText('6.99')
            self.my_le_momento_laje.setText('2.69')
            self.ny_le_momento_laje.setText('6.99')
            self.ny_le_momento_laje.setDisabled(False)
            self.add_btn_momento_laje.click()

            # Compatibilização
            self.add_linha_btn_compat_laje.click()
            self.add_linha_btn_compat_laje.click()
            self.add_linha_btn_compat_laje.click()
            self.compat_table_compat_laje.cellWidget(0, 1).setCurrentIndex(2)
            self.compat_table_compat_laje.cellWidget(0, 2).setCurrentIndex(1)
            self.compat_table_compat_laje.cellWidget(0, 3).setCurrentIndex(2)
            self.compat_table_compat_laje.cellWidget(1, 1).setCurrentIndex(2)
            self.compat_table_compat_laje.cellWidget(1, 2).setCurrentIndex(2)
            self.compat_table_compat_laje.cellWidget(1, 3).setCurrentIndex(2)
            self.compat_table_compat_laje.cellWidget(2, 0).setCurrentIndex(1)
            self.compat_table_compat_laje.cellWidget(2, 2).setCurrentIndex(2)
            self.compat_momentos_laje()

            # Dimensionamento
            self.actionDimensionar_Lajes.trigger()

            ### Vigas ###
            # Carcterização
            self.l_le_carac_viga.setText('12')
            self.h_le_carac_viga.setText('60')
            self.bw_le_carac_viga.setText('15')
            self.nos_le_carac_viga.setText('0, 6, 12')
            self.add_btn_carac_viga.click()

            # Momentos
            self.import_le_momentos_viga.setText('C:/Python36/Lib/site-packages/ConcretePy/save/diagrams/teste3-m.txt')
            self.add_btn_momentos_viga.click()

            # Dimensionar Flexao
            self.actionDimensionar_Vigas_Flexao.trigger()

            # Cortantes
            self.import_le_cortantes_viga.setText('C:/Python36/Lib/site-packages/ConcretePy/save/diagrams/teste3-v.txt')
            self.add_btn_cortantes_viga.click()

    def open_qss(self, path):
        """
        opens a Qt stylesheet with a path relative to the project

        Note: it changes the urls in the Qt stylesheet (in memory), and makes these urls relative to the project
        Warning: the urls in the Qt stylesheet should have the forward slash ('/') as the pathname separator
        """
        with open(path) as f:
            qss = f.read()
            pattern = r'url\((.*?)\);'
            for url in sorted(set(re.findall(pattern, qss)), key=len, reverse=True):
                directory, basename = os.path.split(path)
                new_url = os.path.join(directory, *url.split('/'))
                new_url = os.path.normpath(new_url)
                new_url = new_url.replace(os.path.sep, '/')
                qss = qss.replace(url, new_url)
            return qss

    def init_menus(self):
        self.actionNovo.triggered.connect(self.new_file)
        self.actionAbrir.triggered.connect(self.open_file)
        self.actionSalvar.triggered.connect(self.save_file)
        self.actionSalvar_Como.triggered.connect(self.save_file_as)
        self.actionSair.triggered.connect(sys.exit)
        self.actionDevelopment_Tool.triggered.connect(self.dev_tool)

    def init_lajes(self):
        # Ações
        self.actionDimensionar_Lajes.triggered.connect(self.dimensionar_todas_lajes)

        # Botões
        self.add_btn_carac_laje.clicked.connect(self.add_laje)
        self.remov_btn_carac_laje.clicked.connect(self.remove_laje)
        self.add_btn_carg_laje.clicked.connect(self.add_carga_laje)
        self.add_btn_reac_laje.clicked.connect(self.add_reac_laje)
        self.add_btn_momento_laje.clicked.connect(self.add_momento_laje)
        self.add_linha_btn_compat_laje.clicked.connect(self.add_linha_compat_laje)
        self.remov_linha_btn_compat_laje.clicked.connect(self.remov_linha_compat_laje)
        self.add_compt_btn_compat_laje.clicked.connect(self.compat_momentos_laje)
        # self.add_btn_dim_laje.clicked.connect(self.dimensionar_elemento_laje)
        self.verificar_btn_els_laje.clicked.connect(self.verificar_els_laje)

        # ComboBox Index Change
        self.nlaje_cbox_carac_laje.currentIndexChanged.connect(self.change_carac_cbox_laje)
        self.nlaje_cbox_carg_laje.currentIndexChanged.connect(self.change_carga_cbox_laje)
        self.nlaje_cbox_reac_laje.currentIndexChanged.connect(self.change_reac_cbox_laje)
        self.nlaje_cbox_momento_laje.currentIndexChanged.connect(self.change_momento_cbox_laje)
        # self.nlaje_cbox_dim_laje.currentIndexChanged.connect(self.change_dim_cbox_laje)

    def init_vigas(self):
        # Widget Momentos Plt
        self.widget_momentos_vigas.mpl = MplWidget(self)
        self.widget_momentos_vigas.grid = QGridLayout()
        self.widget_momentos_vigas.setLayout(self.widget_momentos_vigas.grid)
        self.widget_momentos_vigas.grid.addWidget(self.widget_momentos_vigas.mpl, 1, 1)

        # Widget Cortantes Plt
        self.widget_cortantes_vigas.mpl = MplWidget(self)
        self.widget_cortantes_vigas.grid = QGridLayout()
        self.widget_cortantes_vigas.setLayout(self.widget_cortantes_vigas.grid)
        self.widget_cortantes_vigas.grid.addWidget(self.widget_cortantes_vigas.mpl, 1, 1)

        # Ações
        self.actionDimensionar_Vigas_Flexao.triggered.connect(self.dimensionar_flexao_todas_vigas)

        # Botões
        self.add_btn_carac_viga.clicked.connect(self.add_viga)
        self.remov_btn_carac_viga.clicked.connect(self.rem_viga)
        self.import_btn_momentos_viga.clicked.connect(self.import_momentos_vigas)
        self.add_btn_momentos_viga.clicked.connect(self.add_momentos_vigas)
        self.add_btn_cortantes_viga.clicked.connect(self.add_cortantes_vigas)

        # ComboBox Index Change
        self.nviga_cbox_carac_viga.currentIndexChanged.connect(self.change_carac_cbox_viga)
        self.nviga_cbox_dim_flex_viga.currentIndexChanged.connect(self.change_nviga_cbox_dim_flex_viga)
        self.sec_cbox_dim_flex_viga.currentIndexChanged.connect(self.change_sec_cbox_dim_flex_viga)

    def init_pilares(self):
        pass

    # Menu methods
    def save_file(self):
        if self.fileName is None:
            self.save_file_as()
        else:
            # Save compat table indices
            for i in range(self.compat_table_compat_laje.rowCount()):
                row = []
                for j in range(4):
                    row.append(self.compat_table_compat_laje.cellWidget(i, j).currentIndex())
                self.inputData.table_rows_compat_lajes_indices.append(row)

            with open(self.fileName, 'w') as file:
                nlajes = len(self.inputData.lajes)
                nvigas = len(self.inputData.vigas)
                file.write(f'{nlajes}, {nvigas}\n\n')

                for i in range(1, len(self.inputData.lajes) + 1):
                    laje = self.inputData.lajes[i]
                    numero = laje.numero
                    lx = laje.lx
                    ly = laje.ly
                    h = laje.h
                    apoio = laje.apoio
                    superior_espessura = laje.carga.superior_espessura
                    superior_densidade = laje.carga.superior_densidade
                    inferior_espessura = laje.carga.inferior_espessura
                    inferior_densidade = laje.carga.inferior_densidade
                    contrapiso_espessura = laje.carga.contrapiso_espessura
                    contrapiso_densidade = laje.carga.contrapiso_densidade
                    parede_caso = laje.carga.parede_caso
                    parede_espessura = laje.carga.parede_espessura
                    parede_perimetro = laje.carga.parede_perimetro
                    parede_altura = laje.carga.parede_altura
                    carga_utilizacao = laje.carga.carga_utilizacao
                    vx = laje.vx
                    vx_ = laje.vx_
                    vy = laje.vy
                    vy_ = laje.vy_
                    mx = laje.mx
                    mx_ = laje.mx_
                    my = laje.my
                    my_ = laje.my_
                    file.write(f'Laje {i}\n')
                    file.write(f'Laje({numero}, {lx}, {ly}, {h}, "{apoio}")\n')
                    file.write(f'calc_cargas({superior_espessura}, {superior_densidade}, {inferior_espessura}, {inferior_densidade}, {contrapiso_espessura}, {contrapiso_densidade}, "{parede_caso}", {parede_espessura}, {parede_perimetro}, {parede_altura}, {carga_utilizacao})\n')
                    file.write(f'{vx}, {vx_}, {vy}, {vy_}, {mx}, {mx_}, {my}, {my_}\n\n')

                file.write(f'{self.inputData.table_rows_compat_lajes_indices}\n\n')

                for i in range(1, len(self.inputData.vigas) + 1):
                    viga = self.inputData.vigas[i]
                    numero = viga.numero
                    l = viga.l
                    h = viga.h
                    bw = viga.bw
                    nos = viga.nos
                    fileNameM = viga.fileNameM
                    file.write(f'Viga {i}\n')
                    file.write(f'Viga({numero}, {l}, {h}, {bw}, {nos})\n')
                    file.write(f'{fileNameM}\n\n')

    def save_file_as(self):
        self.fileName = QFileDialog.getSaveFileName(self, 'Salvar como', './save', filter="ConctrePy File(*.cpfl)")[0]
        if self.fileName == '':
            self.fileName = None
            return
        self.setWindowTitle('ConcretePy - [{}]'.format(self.fileName))
        self.save_file()

    def open_file(self, trigger, fileName=None):
        if fileName is not None:
            self.fileName = fileName
        else:
            fileName = QFileDialog.getOpenFileName(self, 'Abrir arquivo', './save', filter="ConctrePy File(*.cpfl)")[0]
            if fileName == '':
                return None
            self.new_file()
            self.fileName = fileName
        self.setWindowTitle('ConcretePy - [{}]'.format(self.fileName))

        with open(self.fileName, 'r') as file:
            [nlajes, nvigas] = file.readline().split(', ')
            nlajes = int(nlajes)
            nvigas = int(nvigas)
            file.readline()

            for i in range(1, nlajes + 1):
                file.readline()
                laje = eval(file.readline())
                self.inputData.lajes.update({i: laje})
                self.inputData.lajes[i].calc_cargas
                eval(f'self.inputData.lajes[{i}].{file.readline()}')
                [vx,  vx_, vy, vy_, mx, mx_, my, my_] = file.readline().split(', ')
                self.inputData.lajes[i].vx = eval(vx)
                self.inputData.lajes[i].vx_ = eval(vx_)
                self.inputData.lajes[i].vy = eval(vy)
                self.inputData.lajes[i].vy_ = eval(vy_)
                self.inputData.lajes[i].mx = eval(mx)
                self.inputData.lajes[i].mx_ = eval(mx_)
                self.inputData.lajes[i].my = eval(my)
                self.inputData.lajes[i].my_ = eval(my_)
                file.readline()

            self.inputData.table_rows_compat_lajes_indices = eval(file.readline())
            file.readline()

            for i in range(1, nvigas + 1):
                file.readline()
                viga = eval(file.readline())
                self.inputData.vigas.update({i: viga})
                self.inputData.vigas[i].fileNameM = file.readline()


        # Carregar Lajes na GUI
        for i in self.inputData.lajes:
            self.nlaje_cbox_carac_laje.addItem(str(int(get_text(self.nlaje_cbox_carac_laje)) + 1))
            self.nlaje_cbox_carg_laje.addItem(str(int(get_text(self.nlaje_cbox_carac_laje))))
            self.nlaje_cbox_momento_laje.addItem(str(int(get_text(self.nlaje_cbox_carac_laje))))
            self.nlaje_cbox_dim_laje.addItem(str(int(get_text(self.nlaje_cbox_carac_laje))))
            self.nlaje_cbox_reac_laje.addItem(str(int(get_text(self.nlaje_cbox_carac_laje))))
            self.nlaje_cbox_carac_laje.setCurrentIndex(self.nlaje_cbox_carac_laje.currentIndex() + 1)

        for i in self.inputData.lajes:
            self.add_btn_reac_laje.click()
            self.add_btn_momento_laje.click()

        # Carregar tabela de compatibilização
        self.inputData.table_rows_compat_lajes = []
        for i, j in zip(range(len(self.inputData.table_rows_compat_lajes_indices)),
                        self.inputData.table_rows_compat_lajes_indices):
            self.add_linha_btn_compat_laje.click()
            for k, l in zip(range(4), j):
                self.compat_table_compat_laje.cellWidget(i, k).setCurrentIndex(l)
        self.add_compt_btn_compat_laje.click()

        self.dimensionar_todas_lajes()

        self.update_carac_laje_text()
        self.update_carga_laje_text()

        for i in self.inputData.vigas:
            n = int(get_text(self.nviga_cbox_carac_viga))
            self.nviga_cbox_carac_viga.addItem(str(n + 1))
            self.nviga_cbox_momentos_viga.addItem(str(n))
            self.nviga_cbox_dim_flex_viga.addItem(str(n))
            self.nviga_cbox_cortantes_viga.addItem(str(n))
            self.nviga_cbox_carac_viga.setCurrentIndex(self.nviga_cbox_carac_viga.currentIndex() + 1)

        self.nviga_cbox_carac_viga.setCurrentIndex(0)
        self.update_carac_viga_text()

    def new_file(self):
        self.inputData = InputData()
        self.outputData = OutputData()
        tp = [i for i in dir(self)]
        for i in tp:
            if str(type(eval('self.{}'.format(i)))) == "<class 'PyQt5.QtWidgets.QLineEdit'>":
                eval("self.{}.setText('')".format(i))
            elif str(type(eval('self.{}'.format(i)))) == "<class 'PyQt5.QtWidgets.QTextEdit'>":
                eval("self.{}.setText('')".format(i))
            elif str(type(eval('self.{}'.format(i)))) == "<class 'PyQt5.QtWidgets.QTextBrowser'>":
                eval("self.{}.clear()".format(i))
            elif str(type(eval('self.{}'.format(i)))) == "<class 'PyQt5.QtWidgets.QTableWidgetItem'>":
                eval("self.{}.clear()".format(i))

        for i in range(self.compat_table_compat_laje.rowCount()):
            self.compat_table_compat_laje.removeRow(0)

        tp = (self.nlaje_cbox_momento_laje, self.nlaje_cbox_reac_laje, self.nlaje_cbox_dim_laje,
              self.nlaje_cbox_carg_laje, self.nlaje_cbox_carac_laje)

        for i in tp:
            i.clear()

        self.nlaje_cbox_carac_laje.addItem('1')
        self.apoio_cbox_carac_laje.setCurrentIndex(0)
        self.caso_parede_cbox_carg_laje.setCurrentIndex(0)

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

    # Error pop-ups
    def check_error01(self, tp):
        for i in tp:
            try:
                float(i)
            except ValueError:
                error_title = "Error 01"
                error_msg = "Preencha os campos de texto com números reais."
                QMessageBox.warning(self, error_title, error_msg, QMessageBox.Ok)
                return False
        return True

    # Laje methods
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
            # self.nlaje_cbox_dim_laje.addItem(str(int(get_text(self.nlaje_cbox_carac_laje))))
            self.nlaje_cbox_reac_laje.addItem(str(int(get_text(self.nlaje_cbox_carac_laje))))
            self.nlaje_cbox_els_laje.addItem(str(int(get_text(self.nlaje_cbox_carac_laje))))
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
            self.nlaje_cbox_reac_laje.removeItem(numero - 1)
            self.nlaje_cbox_momento_laje.removeItem(numero - 1)
            self.update_carac_laje_text()
            if self.nlaje_cbox_carac_laje.currentIndex() != 0:
                self.nlaje_cbox_carac_laje.setCurrentIndex(self.nlaje_cbox_carac_laje.currentIndex() - 1)
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
            s += """Laje {}
        lx = {} m
        ly = {} m
        h = {} cm
        Tipo de apoio: {}
""".format(laje.numero, laje.lx, laje.ly, laje.h * 100, laje.apoio)

        self.textBrowser_carc_laje.setText(s)

    def add_carga_laje(self):
        numero = get_text(self.nlaje_cbox_carg_laje)
        espessura_revest_sup = get_text(self.espessura_revest_sup_le_carg_laje)
        densidade_revest_sup = get_text(self.peso_revest_sup_le_carg_laje)
        espessura_revest_inf = get_text(self.espessura_revest_inf_le_carg_laje)
        densidade_revest_inf = get_text(self.peso_revest_inf_le_carg_laje)
        espessura_contrapiso = get_text(self.espessura_contrap_le_carg_laje)
        densidade_contrapiso = get_text(self.peso_contrap_le_carg_laje)
        caso_parede = get_text(self.caso_parede_cbox_carg_laje)
        espessura_parede = get_text(self.espessura_parede_le_carg_laje)
        perimetro_parede = get_text(self.perimetro_parede_le_carg_laje)
        altura_parede = get_text(self.altura_parede_le_carg_laje)
        carga_utiliz = get_text(self.utiliz_le_carg_laje)

        tp = (espessura_revest_sup, espessura_revest_inf, espessura_parede, espessura_contrapiso, carga_utiliz,
              densidade_contrapiso, densidade_revest_inf, densidade_revest_sup, perimetro_parede, altura_parede)

        if not self.check_error01(tp):
            return

        numero = int(numero)
        espessura_revest_sup = float(espessura_revest_sup) / 100
        espessura_revest_inf = float(espessura_revest_inf) / 100
        espessura_contrapiso = float(espessura_contrapiso) / 100
        espessura_parede = float(espessura_parede) / 100
        densidade_revest_sup = float(densidade_revest_sup) * 1e3
        densidade_revest_inf = float(densidade_revest_inf) * 1e3
        densidade_contrapiso = float(densidade_contrapiso) * 1e3
        perimetro_parede = float(perimetro_parede) / 100
        altura_parede = float(altura_parede) / 100
        carga_utiliz = float(carga_utiliz) * 1e3

        self.inputData.lajes[numero].calc_cargas(
            espessura_revest_sup, densidade_revest_sup,
            espessura_revest_inf, densidade_revest_inf,
            espessura_contrapiso, densidade_contrapiso,
            caso_parede, espessura_parede, perimetro_parede, altura_parede,
            carga_utiliz)

        if self.nlaje_cbox_carg_laje.currentIndex() <= self.nlaje_cbox_carg_laje.count() - 2:
            self.nlaje_cbox_carg_laje.setCurrentIndex(self.nlaje_cbox_carg_laje.currentIndex() + 1)

        self.update_carga_laje_text()

    def update_carga_laje_text(self):
        s = ''

        for i in range(1, len(self.inputData.lajes) + 1):
            laje = self.inputData.lajes[i]
            carga = self.inputData.lajes[i].carga
            if carga is None:
                s += 'Laje {}\nCargas ainda não adicionadas\n\n'.format(laje.numero)
            else:
                s += """Laje {}
        Peso próprio: {:.2f} kN/m²
        Carga permanente: {:.2f} kN/m²
        Carga de utilização: {:.2f} kN/m²
        Carga total: {:.2f} kN/m²\n\n""".format(laje.numero, carga.peso_proprio / 1e3,
                                                carga.carga_permanente / 1e3,
                                                carga.carga_utilizacao / 1e3, carga.carga_total / 1e3)

        self.textBrowser_carg_laje.setText(s)

    def add_reac_laje(self):
        numero = get_enabled(self.nlaje_cbox_reac_laje)
        vx = get_enabled(self.vx_le_reac_laje)
        vx_ = get_enabled(self.v_x_le_reac_laje)
        vy = get_enabled(self.vy_le_reac_laje)
        vy_ = get_enabled(self.v_y_le_reac_laje)

        tp = list(i for i in (vx, vx_, vy, vy_) if i is not None)

        if not self.check_error01(tp):
            return

        numero = int(numero)

        try:
            vx = float(vx)
        except:
            pass

        try:
            vx_ = float(vx_)
        except:
            pass

        try:
            vy = float(vy)
        except:
            pass

        try:
            vy_ = float(vy_)
        except:
            pass

        self.inputData.lajes[numero].calc_reacoes(vx, vx_, vy, vy_)

        if self.nlaje_cbox_reac_laje.currentIndex() <= self.nlaje_cbox_reac_laje.count() - 2:
            self.nlaje_cbox_reac_laje.setCurrentIndex(self.nlaje_cbox_reac_laje.currentIndex() + 1)

        self.update_reac_laje_text()

    def update_reac_laje_text(self):
        s = ''

        def get_reac(V):
            if V is None:
                return 0
            else:
                return V

        for i in range(1, len(self.inputData.lajes) + 1):
            laje = self.inputData.lajes[i]
            Vx = self.inputData.lajes[i].Vx
            Vx_ = self.inputData.lajes[i].Vx_
            Vy = self.inputData.lajes[i].Vy
            Vy_ = self.inputData.lajes[i].Vy_
            s += """Laje {}
        Reação Vx: {:.2f} kN.m
        Reação Vx': {:.2f} kN.m
        Reação Vy: {:.2f} kN.m
        Reação Vy': {:.2f} kN.m

""".format(laje.numero, get_reac(Vx) / 1e3, get_reac(Vx_) / 1e3, get_reac(Vy) / 1e3, get_reac(Vy_) / 1e3)

        self.textBrowser_reac_laje.setText(s)

    def add_momento_laje(self):
        numero = get_enabled(self.nlaje_cbox_momento_laje)
        mx = get_enabled(self.mx_le_momento_laje)
        my = get_enabled(self.my_le_momento_laje)
        nx = get_enabled(self.nx_le_momento_laje)
        ny = get_enabled(self.ny_le_momento_laje)

        tp = list(i for i in (mx, my, nx, ny) if i is not None)

        if not self.check_error01(tp):
            return

        numero = int(numero)

        try:
            mx = float(mx)
        except:
            pass

        try:
            my = float(my)
        except:
            pass

        try:
            nx = float(nx)
        except:
            pass

        try:
            ny = float(ny)
        except:
            pass

        self.inputData.lajes[numero].calc_momentos(mx, nx, my, ny)

        if self.nlaje_cbox_momento_laje.currentIndex() <= self.nlaje_cbox_momento_laje.count() - 2:
            self.nlaje_cbox_momento_laje.setCurrentIndex(self.nlaje_cbox_momento_laje.currentIndex() + 1)

        self.update_momento_laje_text()

    def update_momento_laje_text(self):
        s = ''

        def get_momento(M):
            if M is None:
                return 0
            else:
                return M.momento_calc

        for i in range(1, len(self.inputData.lajes) + 1):
            laje = self.inputData.lajes[i]
            Mx = self.inputData.lajes[i].Mx
            My = self.inputData.lajes[i].My
            Xx1 = self.inputData.lajes[i].Xx1
            Xx2 = self.inputData.lajes[i].Xx2
            Xy1 = self.inputData.lajes[i].Xy1
            Xy2 = self.inputData.lajes[i].Xy2

            s += """Laje {}
        Momento Mx: {:.2f} kN.m
        Momento My: {:.2f} kN.m
        Momento Xx1: {:.2f} kN.m
        Momento Xx2: {:.2f} kN.m
        Momento Xy1: {:.2f} kN.m
        Momento Xy2: {:.2f} kN.m

""".format(laje.numero,
           get_momento(Mx) / 1e3,
           get_momento(My) / 1e3,
           - get_momento(Xx1) / 1e3,
           - get_momento(Xx2) / 1e3,
           - get_momento(Xy1) / 1e3,
           - get_momento(Xy2) / 1e3)

        self.textBrowser_momentos_laje.setText(s)

    def add_linha_compat_laje(self):
        new_row = [QComboBox(), QComboBox(), QComboBox(), QComboBox()]
        for i in range(len(self.inputData.lajes)):
            new_row[0].addItem(str(i + 1))
            new_row[2].addItem(str(i + 1))
        for i in ('x1', 'x2', 'y1', 'y2'):
            new_row[1].addItem(i)
            new_row[3].addItem(i)

        self.inputData.table_rows_compat_lajes.append(new_row)

        i = self.compat_table_compat_laje.rowCount()
        self.compat_table_compat_laje.insertRow(i)
        self.compat_table_compat_laje.setCellWidget(i, 0, self.inputData.table_rows_compat_lajes[i][0])
        self.compat_table_compat_laje.setCellWidget(i, 1, self.inputData.table_rows_compat_lajes[i][1])
        self.compat_table_compat_laje.setCellWidget(i, 2, self.inputData.table_rows_compat_lajes[i][2])
        self.compat_table_compat_laje.setCellWidget(i, 3, self.inputData.table_rows_compat_lajes[i][3])

    def remov_linha_compat_laje(self):
        self.compat_table_compat_laje.removeRow(self.compat_table_compat_laje.currentRow())

    def compat_momentos_laje(self):
        rows = self.compat_table_compat_laje.rowCount()
        s = ''

        for i in range(rows):
            l1 = int(get_text(self.compat_table_compat_laje.cellWidget(i, 0)))
            l2 = int(get_text(self.compat_table_compat_laje.cellWidget(i, 2)))
            s1 = get_text(self.compat_table_compat_laje.cellWidget(i, 1))
            s2 = get_text(self.compat_table_compat_laje.cellWidget(i, 3))

            m1 = eval('self.inputData.lajes[{}].X{}'.format(l1, s1))
            m2 = eval('self.inputData.lajes[{}].X{}'.format(l1, s1))

            if m1 is None or m2 is None:
                icon = QStyle.SP_MessageBoxWarning
                self.error02 = QMessageBox()
                self.error02.setText('Não é possível compatibilizar momentos nulos')
                self.error02.setWindowTitle('Erro 02')
                self.error02.setWindowIcon(self.error02.style().standardIcon(icon))
                self.error02.setIcon(QMessageBox.Warning)
                self.error02.show()
                return

            if l1 == l2:
                icon = QStyle.SP_MessageBoxWarning
                self.error03 = QMessageBox()
                self.error03.setText('Não é possível compatibilizar um momentos consigo mesmo')
                self.error03.setWindowTitle('Erro 03')
                self.error03.setWindowIcon(self.error03.style().standardIcon(icon))
                self.error03.setIcon(QMessageBox.Warning)
                self.error03.show()
                return

            mc = eval('self.inputData.lajes[{}].X{}.compatibilizar_momentos(self.inputData.lajes[{}].X{})'.format(l1,
                                                                                                                  s1,
                                                                                                                  l2,
                                                                                                                  s2))

            s += 'Compatibilização de L{} e L{}: {:.2f} kN.m\n'.format(self.inputData.lajes[l1].numero,
                                                                       self.inputData.lajes[l2].numero, -mc / 1e3)

        self.textBrowser_compat_laje.setText(s)

    def dimensionar_todas_lajes(self):
        for laje in self.inputData.lajes.values():
            for momento in (laje.Mx, laje.My, laje.Xx1, laje.Xx2, laje.Xy1, laje.Xy2):
                try:
                    momento.dimensionar_todos()
                    self.outputData.momentos_lajes.update({momento.id_compt: momento})
                except AttributeError:
                    pass

        self.update_dim_laje_text()

    def update_dim_laje_text(self):
        s = ''
        for i in self.outputData.momentos_lajes.values():
            numer_laje = i.numero_laje
            tipo = i.tipo
            armadura = i.armadura

            s += 'Laje {} - Momento {}\n'.format(numer_laje, tipo)

            for j, k in armadura.items():
                if j is None:
                    s += '  Armadura:\n    {}\n'.format(str(k))
                else:
                    s += '  Vizinho: {} - '.format(j.numero_laje)
                    s += 'Armadura:\n    {}\n'.format(str(k))
            s += '\n'

        self.textBrowser_dim_laje.setText(s)

    def dimensionar_elemento_laje(self):
        pass

    def verificar_els_laje(self):
        n = get_text(self.nlaje_cbox_els_laje)
        omega = get_text(self.kalmanok_le_els_laje)

        if not self.check_error01((omega,)):
            return

        n = int(n)
        omega = float(omega)

        flag = self.inputData.lajes[n].verificar_els_deformacao(omega)

        if not flag:
            error_title = "Error 11"
            error_msg = "Laje não passou no ELS-DEF."
            QMessageBox.warning(self, error_title, error_msg, QMessageBox.Ok)

        self.update_els_laje_text()

    def update_els_laje_text(self):
        s = ''
        for laje in self.inputData.lajes.values():
            s += f'Laje {laje.numero}\nVerificação de flecha: {laje.verFlecha}\n\n'

        self.textBrowser_els_laje.setText(s)

    def change_carac_cbox_laje(self):
        try:
            n = int(get_text(self.nlaje_cbox_carac_laje))
            self.lx_le_carac_laje.setText(str(self.inputData.lajes[n].lx * 100))
            self.ly_le_carac_laje.setText(str(self.inputData.lajes[n].ly * 100))
            self.h_le_carac_laje.setText(str(self.inputData.lajes[n].h * 100))
            text = str(self.inputData.lajes[n].apoio)
            if text == 'Caso 1':
                text = 'Caso 1 - Ax1-Ax2-Ay1-Ay2'
            elif text == 'Caso 2A':
                text = 'Caso 2A - Ex1-Ax2-Ay1-Ay2'
            elif text == 'Caso 2B':
                text = 'Caso 2B - Ax1-Ax2-Ey1-Ay2'
            elif text == 'Caso 3':
                text = 'Caso 3 - Ex1-Ax2-Ey1-Ay2'
            elif text == 'Caso 4A':
                text = 'Caso 4A - Ex1-Ex2-Ay1-Ay2'
            elif text == 'Caso 4B':
                text = 'Caso 4B - Ax1-Ax2-Ey1-Ey2'
            elif text == 'Caso 5A':
                text = 'Caso 5A - Ex1-Ex2-Ey1-Ay2'
            elif text == 'Caso 5B':
                text = 'Caso 5B - Ex1-Ax2-Ey1-Ey2'
            elif text == 'Caso 6':
                text = 'Caso 6 - Ex1-Ex2-Ey1-Ey2'
            self.apoio_cbox_carac_laje.setCurrentIndex(self.apoio_cbox_carac_laje.findText(text))
        except KeyError:
            pass
        except ValueError:
            pass

    def change_carga_cbox_laje(self):
        try:
            n = int(get_text(self.nlaje_cbox_carg_laje))
            self.espessura_revest_sup_le_carg_laje.setText(str(self.inputData.lajes[n].carga.superior_espessura * 100))
            self.peso_revest_sup_le_carg_laje.setText(str(self.inputData.lajes[n].carga.superior_densidade / 1e3))
            self.espessura_revest_inf_le_carg_laje.setText(str(self.inputData.lajes[n].carga.inferior_espessura * 100))
            self.peso_revest_inf_le_carg_laje.setText(str(self.inputData.lajes[n].carga.inferior_densidade / 1e3))
            self.espessura_contrap_le_carg_laje.setText(str(self.inputData.lajes[n].carga.contrapiso_espessura * 100))
            self.peso_contrap_le_carg_laje.setText(str(self.inputData.lajes[n].carga.contrapiso_densidade / 1e3))
            self.espessura_parede_le_carg_laje.setText(str(self.inputData.lajes[n].carga.parede_espessura * 100))
            self.perimetro_parede_le_carg_laje.setText(str(self.inputData.lajes[n].carga.parede_perimetro * 100))
            self.altura_parede_le_carg_laje.setText(str(self.inputData.lajes[n].carga.parede_altura * 100))
            self.utiliz_le_carg_laje.setText(str(self.inputData.lajes[n].carga.carga_utilizacao / 1e3))
            self.caso_parede_cbox_carg_laje.setCurrentIndex(
                self.caso_parede_cbox_carg_laje.findText(self.inputData.lajes[n].carga.parede_caso))
        except KeyError:
            pass
        except AttributeError:
            pass
        except ValueError:
            pass

    def change_reac_cbox_laje(self):
        try:
            n = int(get_text(self.nlaje_cbox_reac_laje))
            self.lambda_le_reac_laje.setText(str(self.inputData.lajes[n].lamb))
            self.vx_le_reac_laje.setEnabled(True)
            self.v_x_le_reac_laje.setEnabled(True)
            self.vy_le_reac_laje.setEnabled(True)
            self.v_y_le_reac_laje.setEnabled(True)
            self.vx_le_reac_laje.setText(str(self.inputData.lajes[n].vx))
            self.v_x_le_reac_laje.setText(str(self.inputData.lajes[n].vx_))
            self.vy_le_reac_laje.setText(str(self.inputData.lajes[n].vy))
            self.v_y_le_reac_laje.setText(str(self.inputData.lajes[n].vy_))
            apoio = self.inputData.lajes[n].apoio
            if apoio == 'Caso 1':
                self.v_x_le_reac_laje.setDisabled(True)
                self.v_x_le_reac_laje.setText('')
                self.v_y_le_reac_laje.setDisabled(True)
                self.v_y_le_reac_laje.setText('')
            elif apoio == 'Caso 2A':
                self.v_x_le_reac_laje.setDisabled(True)
                self.v_x_le_reac_laje.setText('')
            elif apoio == 'Caso 2B':
                self.v_y_le_reac_laje.setDisabled(True)
                self.v_y_le_reac_laje.setText('')
            elif apoio == 'Caso 3':
                pass
            elif apoio == 'Caso 4A':
                self.v_x_le_reac_laje.setDisabled(True)
                self.v_x_le_reac_laje.setText('')
                self.vy_le_reac_laje.setDisabled(True)
                self.vy_le_reac_laje.setText('')
            elif apoio == 'Caso 4B':
                self.vx_le_reac_laje.setDisabled(True)
                self.vx_le_reac_laje.setText('')
                self.v_y_le_reac_laje.setDisabled(True)
                self.v_y_le_reac_laje.setText('')
            elif apoio == 'Caso 5A':
                self.vy_le_reac_laje.setDisabled(True)
                self.vy_le_reac_laje.setText('')
            elif apoio == 'Caso 5B':
                self.vx_le_reac_laje.setDisabled(True)
                self.vx_le_reac_laje.setText('')
            elif apoio == 'Caso 6':
                self.vx_le_reac_laje.setDisabled(True)
                self.vx_le_reac_laje.setText('')
                self.vy_le_reac_laje.setDisabled(True)
                self.vy_le_reac_laje.setText('')
        except KeyError:
            pass
        except ValueError:
            pass

    def change_momento_cbox_laje(self):
        try:
            n = int(get_text(self.nlaje_cbox_momento_laje))
            self.lambda_le_momento_laje.setText(str(self.inputData.lajes[n].lamb))
            self.mx_le_momento_laje.setEnabled(True)
            self.nx_le_momento_laje.setEnabled(True)
            self.my_le_momento_laje.setEnabled(True)
            self.ny_le_momento_laje.setEnabled(True)
            self.mx_le_momento_laje.setText(str(self.inputData.lajes[n].mx))
            self.nx_le_momento_laje.setText(str(self.inputData.lajes[n].mx_))
            self.my_le_momento_laje.setText(str(self.inputData.lajes[n].my))
            self.ny_le_momento_laje.setText(str(self.inputData.lajes[n].my_))
            apoio = self.inputData.lajes[n].apoio
            if apoio == 'Caso 1':
                self.nx_le_momento_laje.setDisabled(True)
                self.nx_le_momento_laje.setText('')
                self.ny_le_momento_laje.setDisabled(True)
                self.ny_le_momento_laje.setText('')
            elif apoio == 'Caso 2A':
                self.nx_le_momento_laje.setDisabled(True)
                self.nx_le_momento_laje.setText('')
            elif apoio == 'Caso 2B':
                self.ny_le_momento_laje.setDisabled(True)
                self.ny_le_momento_laje.setText('')
            elif apoio == 'Caso 3':
                pass
            elif apoio == 'Caso 4A':
                self.nx_le_momento_laje.setDisabled(True)
                self.nx_le_momento_laje.setText('')
            elif apoio == 'Caso 4B':
                self.ny_le_momento_laje.setDisabled(True)
                self.ny_le_momento_laje.setText('')
            elif apoio == 'Caso 5A':
                pass
            elif apoio == 'Caso 5B':
                pass
            elif apoio == 'Caso 6':
                pass
        except KeyError:
            pass
        except ValueError:
            pass

    def change_dim_cbox_laje(self):
        n = int(get_text(self.nlaje_cbox_carg_laje))
        try:
            self.lx_le_carac_laje.setText(str(self.inputData.lajes[n].lx * 100))
        except KeyError:
            pass

    # Viga Methods
    def add_viga(self):
        n = get_text(self.nviga_cbox_carac_viga)
        l = get_text(self.l_le_carac_viga)
        h = get_text(self.h_le_carac_viga)
        bw = get_text(self.bw_le_carac_viga)
        nos = get_text(self.nos_le_carac_viga)

        if not self.check_error01((l, h, bw)):
            return

        try:
            nos = list(eval(nos))
            for i in range(len(nos)):
                nos[i] = float(nos[i])
        except:
            error_title = "Error 02"
            error_msg = "Elementos do tuple apoio devem ser números reais"
            QMessageBox.warning(self, error_title, error_msg, QMessageBox.Ok)
            return

        n = int(n)
        l = float(l)
        h = float(h) / 100
        bw = float(bw) / 100

        try:
            assert round(l, 2) == round(nos[-1], 2)
        except AssertionError:
            error_title = "Error 03"
            error_msg = "Último elemento da tuple nós deve ser igual ao comprimento da viga"
            QMessageBox.warning(self, error_title, error_msg, QMessageBox.Ok)
            return

        self.inputData.vigas.update({n: Viga(n, l, h, bw, nos, self.inputData.config)})

        if self.nviga_cbox_carac_viga.currentIndex() + 1 == self.nviga_cbox_carac_viga.count():
            self.nviga_cbox_carac_viga.addItem(str(n + 1))
            self.nviga_cbox_momentos_viga.addItem(str(n))
            self.nviga_cbox_dim_flex_viga.addItem(str(n))
            self.nviga_cbox_cortantes_viga.addItem(str(n))
            self.nviga_cbox_carac_viga.setCurrentIndex(self.nviga_cbox_carac_viga.currentIndex() + 1)
        else:
            self.nviga_cbox_carac_viga.setCurrentIndex(self.nviga_cbox_carac_viga.currentIndex() + 1)

        self.update_carac_viga_text()

    def rem_viga(self):
        if self.nviga_cbox_carac_viga.currentIndex() + 1 == self.nviga_cbox_carac_viga.count() - 1:
            numero = int(get_text(self.nviga_cbox_carac_viga))
            self.inputData.vigas.pop(numero)
            self.nviga_cbox_carac_viga.removeItem(numero)
            self.nviga_cbox_momentos_viga.removeItem(numero - 1)
            self.nviga_cbox_dim_flex_viga.removeItem(numero - 1)
            self.nviga_cbox_cortantes_viga.removeItem(numero - 1)
            self.update_carac_viga_text()
            if self.nviga_cbox_carac_viga.currentIndex() != 0:
                self.nviga_cbox_carac_viga.setCurrentIndex(self.nviga_cbox_carac_viga.currentIndex() - 1)
        else:
            error_title = "Error 05"
            error_msg = "Remova primeiro a última viga adicionada"
            QMessageBox.warning(self, error_title, error_msg, QMessageBox.Ok)

    def update_carac_viga_text(self):
        s = ''

        for i in range(1, len(self.inputData.vigas) + 1):
            viga = self.inputData.vigas[i]
            s += """Viga {}
    l = {} m
    h = {} cm
    bw = {} cm
    Nós: {}
\n""".format(viga.numero, viga.l, viga.h * 100, viga.bw * 100, viga.nos)

        self.textBrowser_carc_viga.setText(s)

    def import_momentos_vigas(self):
        n = int(get_text(self.nviga_cbox_momentos_viga))
        fileName = QFileDialog.getOpenFileName(self, 'Importar Momento', './save/diagrams',
                                               filter="Arquivo de Texto(*.txt)")[0]
        self.import_le_momentos_viga.setText(fileName)
        self.add_momentos_vigas()

    def add_momentos_vigas(self):
        n = int(get_text(self.nviga_cbox_momentos_viga))
        fileName = get_text(self.import_le_momentos_viga)

        flag = self.inputData.vigas[n].ler_csv_momentos(fileName)
        if flag:
            error_title = "Error 04"
            error_msg = "Apoios incompatíveis com diagrama de momento fornecido"
            QMessageBox.warning(self, error_title, error_msg, QMessageBox.Ok)
            return

        x = self.inputData.vigas[n].x_m
        m = self.inputData.vigas[n].m
        self.widget_momentos_vigas.mpl.mplCanvas.plot_momento(x, m)

    def dimensionar_flexao_todas_vigas(self):
        for viga in self.inputData.vigas.keys():
            self.inputData.vigas[viga].procurar_momentos()
            for momento in self.inputData.vigas[viga].momentos.keys():
                self.inputData.vigas[viga].momentos[momento].dimensionar_flexao()

        self.change_nviga_cbox_dim_flex_viga()
        self.change_sec_cbox_dim_flex_viga()
        # self.update_dim_flex_text()
        self.update_dim_flex_text2()

    def update_dim_flex_text(self):
        s = ''
        viga = int(get_text(self.nviga_cbox_dim_flex_viga))
        sec = int(get_text(self.sec_cbox_dim_flex_viga))
        for i in range(len(self.inputData.vigas[viga].momentos[sec].possibilidades)):
            s += f'Possibilidade {i+1}:\n'
            s += str(self.inputData.vigas[viga].momentos[sec].possibilidades[i])
            s += '\n\n'
        self.textBrowser_dim_flex_viga.setText(s)

    def update_dim_flex_text2(self):
        s = ''
        for viga in self.inputData.vigas.values():
            for i, sec in zip(range(len(viga.momentos.values())), viga.momentos.values()):
                armadura = sec.armadura
                s += f'Viga {viga.numero} - Seção {i+1}\n{armadura}\n\n'

        self.textBrowser_dim_flex_viga2.setText(s)

    def add_cortantes_vigas(self):
        n = int(get_text(self.nviga_cbox_cortantes_viga))
        fileName = get_text(self.import_le_cortantes_viga)

        flag = self.inputData.vigas[n].ler_csv_cortantes(fileName)
        if flag:
            error_title = "Error 04"
            error_msg = "Apoios incompatíveis com diagrama de momento fornecido"
            QMessageBox.warning(self, error_title, error_msg, QMessageBox.Ok)
            return

        x = self.inputData.vigas[n].x_v
        v = self.inputData.vigas[n].v
        self.widget_cortantes_vigas.mpl.mplCanvas.plot_cortante(x, v)

    def dimensionar_cortante_todas_vigas(self):
        for viga in self.inputData.vigas.keys():
            self.inputData.vigas[viga].procurar_momentos()
            for momento in self.inputData.vigas[viga].momentos.keys():
                self.inputData.vigas[viga].momentos[momento].dimensionar_flexao()

        self.change_nviga_cbox_dim_flex_viga()
        self.change_sec_cbox_dim_flex_viga()

    def change_nviga_cbox_dim_flex_viga(self):
        viga = int(get_text(self.nviga_cbox_dim_flex_viga))
        self.sec_cbox_dim_flex_viga.clear()
        for i in range(len(self.inputData.vigas[viga].momentos)):
            self.sec_cbox_dim_flex_viga.addItem(f'{i+1}')
        self.sec_cbox_dim_flex_viga.setCurrentIndex(0)

    def change_sec_cbox_dim_flex_viga(self):
        viga = int(get_text(self.nviga_cbox_dim_flex_viga))
        sec = int(get_text(self.sec_cbox_dim_flex_viga))
        self.comb_cbox_dim_flex_viga.clear()
        for i in range(len(self.inputData.vigas[viga].momentos[sec].possibilidades)):
            self.comb_cbox_dim_flex_viga.addItem(f'{i+1}')
        self.comb_cbox_dim_flex_viga.setCurrentIndex(0)

        self.update_dim_flex_text()

    def change_carac_cbox_viga(self):
        try:
            n = int(get_text(self.nviga_cbox_carac_viga))
            self.l_le_carac_viga.setText(str(self.inputData.vigas[n].l))
            self.h_le_carac_viga.setText(str(self.inputData.vigas[n].h * 100))
            self.bw_le_carac_viga.setText(str(self.inputData.vigas[n].bw * 100))
            text = '{}'.format(self.inputData.vigas[n].nos)
            text = text.strip('[')
            text = text.strip(']')
            self.nos_le_carac_viga.setText(text)
        except KeyError:
            pass
        except ValueError:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = MainWindow()
    sys.exit(app.exec_())
