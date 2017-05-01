import numpy as np
from ConcretePy.Concrete.configuracoes import Configuracoes
from ConcretePy.Concrete.tabelas import *


class Viga:
    def __init__(self, numero, l, h, b, nos, config=Configuracoes()):
        self.numero = numero
        self.l = l
        self.h = h
        self.bw = b
        self.nos = nos
        self.config = config

        self.sigma_cd = 0.85 * self.config.fcd

        self.fileNameM = None
        self.x = None
        self.m = None
        self.m_reg = None
        self.m_org = None

        self.momentos = {}

    def __repr__(self):
        s = 'Viga {}\nL = {}\nh = {}\nbw = {}'.format(self.numero, self.l, self.h, self.bw)
        return s

    def ler_csv(self, fileName=None, reg_check=False):
        if fileName is None:
            return

        self.fileNameM = fileName
        x = []
        m = []

        try:
            with open(fileName, 'r') as file:
                n = int(file.readline())

                for i in range(n):
                    line = file.readline()
                    line = line.split('\t')
                    x.append(float(line[0]))
                    m.append(float(line[1]) * 1e3)
        except FileNotFoundError:
            return True

        try:
            assert round(x[-1]) == round(self.l)
        except AssertionError:
            return True

        self.x = np.array(x)
        self.m_org = np.array(m)

        try:
            mr = np.array([])
            for i in range(len(self.nos) - 1):
                i0 = x.index(self.nos[i])
                i1 = x.index(self.nos[i + 1])
                mri = m[i0: i1]
                p = np.polyfit(self.x[i0: i1], mri, 2)
                mri = p[0] * (self.x[i0: i1] ** 2) + p[1] * self.x[i0: i1] + p[2]
                mr = np.append(mr, mri)
            mr = np.append(mr, m[-1])
        except (IndexError, ValueError):
            return True

        self.m_reg = mr

        if reg_check:
            self.m = self.m_reg
        else:
            self.m = self.m_org

        self.decalagem()

    def decalagem(self):
        pass

    def procurar_momentos(self):
        n = 0
        for i, x, m in zip(range(len(self.x)), self.x, self.m):
            if i == 0:
                x_ant = x
                m_ant = m
                continue

            if i == 1:
                if m >= m_ant:
                    cres = True
                else:
                    cres = False
                x_ant = x
                m_ant = m
                continue

            cres_ant = cres
            if m >= m_ant:
                cres = True
            else:
                cres = False

            if cres != cres_ant:
                n += 1
                if cres_ant:
                    tipo = '+'
                else:
                    tipo = '-'
                self.momentos.update({n: Momento(n, tipo, m_ant, x_ant, self)})

            x_ant = x
            m_ant = m


class Momento:
    def __init__(self, num, tipo, modulo, pos, viga):
        self.id = num
        self.tipo = tipo
        self.Msk = abs(modulo)
        self.pos = pos
        self.l = viga.l
        self.h = viga.h
        self.bw = viga.bw
        self.config = viga.config
        self.diametroEstribo = 0.005

        self.Msd = self.config.gama_f * self.Msk

        self.possibilidades = None

    def __str__(self):
        s = f'id: {self.id}\nTipo: {self.tipo}\nModulo: {self.Msk}\nPos: {self.pos}'
        return s

    def dimensionar_flexao(self):
        c = self.config.c_viga
        h = self.h
        bw = self.bw
        phi_w = self.diametroEstribo
        d_brita = self.config.diametro_brita
        Msd = self.Msd
        fcd = self.config.fcd
        alfa_c = self.config.alfa_c
        lamb = self.config.lamb
        fyd = self.config.fyd

        linhas_tp = (1, 2, 3)
        self.possibilidades = []
        for diametro in barras:
            sh_min = self.calc_espacamento_h_min(diametro)
            sv_min = self.calc_espacamento_v_min(diametro)

            for linhas in linhas_tp:
                if linhas == 1:
                    d = h - (c + phi_w + diametro / 2)
                elif linhas == 2:
                    d = h - (c + phi_w + diametro + sv_min / 2)
                elif linhas == 3:
                    d = h - (c + phi_w + 3 / 2 * diametro + sv_min)

                kmd = Msd / (bw * fcd * d ** 2)
                kx = (1 - np.sqrt(1 - 2 * kmd / alfa_c)) / lamb
                kz = 1 - 0.5 * lamb * kx
                As_calc = Msd / (kz * d * fyd)

                Aphi = (np.pi * ((diametro / 2) ** 2))
                numero_barras = np.ceil(As_calc / Aphi)
                As_adotada = numero_barras * Aphi

                ver = self.verificar_espacamento_horizontal(sh_min, diametro, numero_barras, linhas)
                ver = ver and self.verificar_taxa_de_armadura(As_adotada)
                ver = ver and self.verificar_kx(kx)

                if ver and numero_barras > 1:
                    self.possibilidades.append(ArmaduraFlexao(numero_barras, diametro, linhas, As_calc, As_adotada))
                    break

    def verificar_espacamento_horizontal(self, s_min, diametro, n, linhas):
        c = self.config.c_viga
        phi_w = self.diametroEstribo
        bw = self.bw
        if linhas == 1:
            return bw > 2 * c + 2 * phi_w + n * diametro + (n - 1) * s_min
        elif linhas == 2:
            return bw > 2 * c + 2 * phi_w + (n - 2) * diametro + (n - 3) * s_min
        elif linhas == 3:
            return bw > 2 * c + 2 * phi_w + (n - 4) * diametro + (n - 5) * s_min

    def verificar_taxa_de_armadura(self, As):
        h = self.h
        bw = self.bw
        fck = round(self.config.fck / 1e6, 0)
        rho_min = rho_min_dict[fck]

        Asmin = rho_min * bw * h
        Asmax = 0.04 * bw * h

        return Asmin < As < h

    def verificar_kx(self, kx):
        fck = round(self.config.fck / 1e6, 0)
        if self.tipo == '+':
            kxlim = kxlim2_3_dict[fck]
            return kx < kxlim
        else:
            if fck <= 50:
                return kx <= 0.45
            else:
                return kx <= 0.35

    def calc_espacamento_v_min(self, diametro):
        diametro_brita = self.config.diametro_brita
        return max(0.02, diametro, 0.5 * diametro_brita)

    def calc_espacamento_h_min(self, diametro):
        diametro_brita = self.config.diametro_brita
        return max(0.02, diametro, 1.2 * diametro_brita)


class ArmaduraFlexao:
    def __init__(self, numero_barras, diametro, linhas, As_calc, As_adotada):
        self.numero_barras = int(numero_barras)
        self.diametro = diametro
        self.linhas = linhas
        self.As_calc = As_calc
        self.As_adotada = As_adotada

    def __str__(self):
        s = f'{self.numero_barras} barras de {self.diametro*1e3} mm dispostas em {self.linhas} linhas\n'
        s += f'Área de aço calculada: {self.As_calc*1e4:.2f} cm²\nÁrea de aço adotada: {self.As_adotada*1e4:.2f} cm²'
        return s


if __name__ == '__main__':
    v1 = Viga(1, 12, 0.60, 0.15, (0, 6, 12))
    v1.ler_csv('C:/Python36/Lib/site-packages/ConcretePy/save/momentos/teste3-m.txt', reg_check=True)
    v1.procurar_momentos()
    v1.momentos[1].dimensionar_flexao()
    for i in v1.momentos[1].possibilidades:
        print(f'{i}\n')
        # print(v1.momentos, v1.momentos[1], v1.momentos[2], v1.momentos[3], sep='\n\n')
