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
        self.x_m = None
        self.m = None
        self.m_reg = None
        self.m_org = None

        self.fileNameV = None
        self.x_v = None
        self.v = None
        self.v_reg = None
        self.v_org = None

        self.momentos = {}
        self.cortantes = {}

    def __repr__(self):
        s = 'Viga {}\nL = {}\nh = {}\nbw = {}'.format(self.numero, self.l, self.h, self.bw)
        return s

    def ler_csv_momentos(self, fileName=None, reg_check=True):
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

        self.x_m = np.array(x)
        self.m_org = np.array(m)

        try:
            mr = np.array([])
            for i in range(len(self.nos) - 1):
                i0 = x.index(self.nos[i])
                i1 = x.index(self.nos[i + 1])
                mri = m[i0: i1]
                p = np.polyfit(self.x_m[i0: i1], mri, 2)
                mri = p[0] * (self.x_m[i0: i1] ** 2) + p[1] * self.x_m[i0: i1] + p[2]
                mr = np.append(mr, mri)
            mr = np.append(mr, m[-1])
        except (IndexError, ValueError):
            return True

        self.m_reg = mr

        if reg_check:
            self.m = self.m_reg
        else:
            self.m = self.m_org

    def procurar_momentos(self):
        n = 0
        for i, x, m in zip(range(len(self.x_m)), self.x_m, self.m):
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

    def ler_csv_cortantes(self, fileName=None, reg_check=False):
        if fileName is None:
            return

        self.fileNameV = fileName
        x = []
        v = []

        try:
            with open(fileName, 'r') as file:
                n = int(file.readline())

                for i in range(n):
                    line = file.readline()
                    line = line.split('\t')
                    x.append(float(line[0]))
                    v.append(float(line[1]) * 1e3)
        except FileNotFoundError:
            return True

        try:
            assert round(x[-1]) == round(self.l)
        except AssertionError:
            return True

        self.x_v = np.array(x)
        self.v_org = np.array(v)

        try:
            vr = np.array([])
            for i in range(len(self.nos) - 1):
                i0 = x.index(self.nos[i])
                i1 = x.index(self.nos[i + 1])
                vri = v[i0: i1]
                p = np.polyfit(self.x_v[i0: i1], vri, 1)
                vri = p[0] * self.x_v[i0: i1] + p[1]
                vr = np.append(vr, vri)
            vr = np.append(vr, v[-1])
        except (IndexError, ValueError):
            return True

        self.v_reg = vr

        if reg_check:
            self.v = self.v_reg
        else:
            self.v = self.v_org

    def procurar_cortantes(self):
        pares_nos = list(zip(self.nos[0:-1], self.nos[1:]))
        x = list(self.x_v)
        v = list(self.v)
        for i, j in enumerate(pares_nos):
            i0 = x.index(j[0])
            i1 = x.index(j[1])
            xi = x[i0 + 1: i1 + 1]
            vi = v[i0 + 1: i1 + 1]
            self.cortantes.update({i + 1: Cortante(i + 1, xi, vi, self.momentos, self)})


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
        self.diametroEstribo = 0.0063

        self.Msd = self.config.gama_f * self.Msk

        self.possibilidades = None
        self.armadura = None

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

                if numero_barras <= 1:
                    num = 2
                else:
                    num = numero_barras

                numero_barras = num

                if numero_barras - 2 * (linhas - 1) < 2:
                    break

                esps = (numero_barras - 1 - 2 * (linhas - 1))
                n = (numero_barras - 2 * (linhas - 1))
                sh = (1 / esps) * (bw - 2 * c - 2 * phi_w - n * diametro)

                if linhas == 1:
                    a = 0
                elif linhas == 2:
                    a = (sv_min + diametro) * ((numero_barras - 2) / numero_barras)
                else:
                    a = ((numero_barras - 4) * 2 * (sv_min + diametro) + 2 * (sv_min + diametro)) / numero_barras

                ver = self.verificar_espacamento_horizontal(sh_min, sh)
                ver = ver and self.verificar_taxa_de_armadura(As_adotada)
                ver = ver and self.verificar_kx(kx)
                ver = ver and self.verificar_armadura_concentrada(a)

                if ver:
                    self.possibilidades.append(
                        ArmaduraFlexao(numero_barras, diametro, linhas, As_calc, As_adotada, sh, d))
                    break

    def verificar_espacamento_horizontal(self, s_min, sh):
        return sh > s_min

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
            # kxlim = kxlim2_3_dict[fck]
            return kx < 0.45
        else:
            if fck <= 50:
                return kx <= 0.45
            else:
                return kx <= 0.35

    def verificar_armadura_concentrada(self, a):
        return a / self.h < 0.1

    def calc_espacamento_v_min(self, diametro):
        diametro_brita = self.config.diametro_brita
        return max(0.02, diametro, 0.5 * diametro_brita)

    def calc_espacamento_h_min(self, diametro):
        diametro_brita = self.config.diametro_brita
        return max(0.02, diametro, 1.2 * diametro_brita)

    def escolher_armadura(self, indice):
        self.armadura = self.possibilidades[indice]
        Ic = (self.bw * self.h ** 3) / 12
        Iii = (self.config.Es / self.config.Ecs) * self.armadura.As_adotada

    def verificar_els_fissura(self):
        Mr = 0.25 * self.bw * (self.h ** 2) * self.config.fctk_inf
        if self.Msd < Mr:
            return 'Não há formação de fissura'

        diametro = round(self.armadura.diametro, 3)

        if diametro <= 8.:
            return 'Abertura de fissura ok'
        else:
            s_max = espacamento_max_fissura[diametro]
            if self.armadura.espacamento <= s_max:
                return 'Abertura de fissura ok'
            else:
                return 'Abertura de fissura FALHOU'

    def verificar_els_deformacao(self, armadura):
        Mr = 0.25 * self.bw * (self.h ** 2) * self.config.fct_m


class ArmaduraFlexao:
    def __init__(self, numero_barras, diametro, linhas, As_calc, As_adotada, espacamento, d):
        self.numero_barras = int(numero_barras)
        self.diametro = diametro
        self.linhas = linhas
        self.As_calc = As_calc
        self.As_adotada = As_adotada
        self.espacamento = espacamento
        self.d = d

    def __str__(self):
        s = f'{self.numero_barras} barras de {self.diametro*1e3} mm dispostas em {self.linhas} linhas\n'
        s += f'Área de aço calculada: {self.As_calc*1e4:.2f} cm²\nÁrea de aço adotada: {self.As_adotada*1e4:.2f} cm²\n'
        s += f'Espaçamento: {self.espacamento*100:.2f} cm'
        return s


class Cortante:
    def __init__(self, numero, x, v, momentos, viga):
        self.numero = numero
        self.x = x
        self.v = v
        self.momentos = momentos
        self.config = viga.config
        self.numero_viga = viga.numero
        self.bw = viga.bw
        self.h = viga.h

        self.l = self.x[-1] - self.x[0]
        self.d = None
        self.buscar_d()
        self.Vsd = self.config.gama_f*max(np.abs(self.v))
        self.Vrd2 = 0.27 * self.config.alfa_v2 * self.config.fcd * self.bw * self.d
        self.Vc = 0.6 * self.config.fctd * self.bw * self.d
        self.Vsw = self.Vsd - self.Vc

        self.Asw_s_min = 0.2 * (self.config.fct_m / self.config.fywk) * self.bw

        self.diametro = 0.0063
        self.Asw_s = None
        self.espacamento = None
        self.s_max = None
        self.lg = None
        self.comprimento = None
        self.numero_de_estribos = None
        self.espacamento_max()
        self.dimensionar_estribos()
        self.comprimento_estribo()

    def buscar_d(self):
        n = self.numero * 2 - 1
        self.d = self.momentos[n].armadura.d

    def verificar_altura_minima(self):
        dmin = self.Vsd / (0.27 * self.config.alfa_v2 * self.config.fcd * self.bw)
        if self.d > dmin:
            return True
        else:
            return False

    def verificar_esmagamento_biela(self):
        return self.Vsd < self.Vrd2

    def espacamento_max(self):
        if self.Vsd <= 0.67*self.Vrd2:
            self.s_max = min(0.6*self.d, 0.3)
        else:
            self.s_max = min(0.3 * self.d, 0.2)

    def dimensionar_estribos(self):
        Vsd_max_min = 0.9 * self.config.fywd * self.d * self.Asw_s_min + self.Vc
        if self.Vsd < Vsd_max_min:
            self.Asw_s = self.Asw_s_min
        else:
            self.Asw_s = (self.Vsw)/(0.9 * self.config.fywd * self.d)

        self.espacamento = min((2*(0.25*self.diametro**2)/self.Asw_s*self.l), self.s_max)
        self.numero_de_estribos = np.ceil(self.l/self.espacamento)
        self.espacamento = self.l/self.numero_de_estribos

    def comprimento_estribo(self):
        self.lg = max(10*self.diametro, 0.07)
        b = self.bw - 2*self.config.c_viga
        h = self.h - 2*self.config.c_viga
        self.comprimento = 2*(self.lg + b + h)

    def __str__(self):
        s = f'Viga: {self.numero_viga}\nSeção: {self.numero}\nDiâmetro: {self.diametro*1e3} mm\n'
        s += f'Quantidade: {self.numero_de_estribos:.0f} estribos\nEspaçamento: {self.espacamento*100:.1f} cm\n'
        s += f'Espaçamento Máximo: {self.s_max*100:.1f} cm\n'
        s += f'Comprimento do Estribo: {self.comprimento} m\n'
        s += f'Comprimento do Gancho: {self.lg} m'
        return s

if __name__ == '__main__':
    # from matplotlib import pyplot as plt
    #
    # v1 = Viga(1, 12, 0.65, 0.15, (0, 5, 12))
    # v1.ler_csv_momentos('C:/Python36/Lib/site-packages/ConcretePy/save/diagrams/Honorato-m.txt', reg_check=False)
    # # plt.plot(v1.x_m, -v1.m/1000)
    # # plt.show()
    #
    # v1.procurar_momentos()
    #
    # v1.momentos[1].dimensionar_flexao()
    # v1.momentos[1].escolher_armadura(1)
    # # print(v1.momentos[1].armadura)
    #
    # v1.momentos[2].dimensionar_flexao()
    # v1.momentos[2].escolher_armadura(1)
    # # print(v1.momentos[2].armadura)
    #
    # v1.momentos[3].dimensionar_flexao()
    # v1.momentos[3].escolher_armadura(0)
    # # print(v1.momentos[3].armadura)
    #
    # v1.ler_csv_cortantes('C:/Python36/Lib/site-packages/ConcretePy/save/diagrams/Honorato-v.txt', reg_check=False)
    # v1.procurar_cortantes()
    # print(v1.cortantes[2].d)
    # print(v1.cortantes[2].verificar_altura_minima())
    # print(v1.cortantes[2].verificar_esmagamento_biela())
    # print(v1.cortantes[1])
    # print(v1.cortantes[2])

    v1 = Viga(1, 12, 0.60, 0.15, (0, 6, 12))
    v1.ler_csv_momentos('C:/Python36/Lib/site-packages/ConcretePy/save/diagrams/teste3-m.txt', reg_check=True)
    v1.procurar_momentos()
    v1.momentos[1].dimensionar_flexao()
    v1.momentos[2].dimensionar_flexao()
    v1.momentos[3].dimensionar_flexao()
    v1.momentos[1].escolher_armadura(0)
    v1.momentos[2].escolher_armadura(0)
    v1.momentos[3].escolher_armadura(0)

    v1.ler_csv_cortantes('C:/Python36/Lib/site-packages/ConcretePy/save/diagrams/teste3-v.txt', reg_check=False)
    v1.procurar_cortantes()
    print(v1.cortantes[1].d)
    print(v1.cortantes[1].verificar_altura_minima())
    print(v1.cortantes[1].verificar_esmagamento_biela())
    print(v1.cortantes[1])
    print(v1.cortantes[2])

    # x = v1.cortantes[1].x
    # v = v1.cortantes[1].v
    # from matplotlib import pyplot as plt
    # plt.plot(x, v)
    # plt.show()

    #
    # for i in v1.momentos[1].possibilidades:
    #     print(f'{i}\n')
    #     print(v1.momentos, v1.momentos[1], v1.momentos[2], v1.momentos[3], sep='\n\n')
    #
    # v1.momentos[1].escolher_armadura(0)
    # print(v1.momentos[1].verificar_els_fissura())
