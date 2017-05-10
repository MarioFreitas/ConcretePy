import numpy as np
from ConcretePy.Concrete.configuracoes import Configuracoes
from ConcretePy.Concrete.tabelas import *


class Laje:
    def __init__(self, numero, lx, ly, h, apoio, config=Configuracoes()):
        # Caracterização da laje
        self.numero = numero
        self.lx = lx
        self.ly = ly
        self.h = h
        self.apoio = apoio
        self.config = config

        self.lamb = self.ly / self.lx

        # Carregamento
        self.carga = None

        # Coeficientes de Marcus
        self.vx = None
        self.vx_ = None
        self.vy = None
        self.vy_ = None
        self.mx = None
        self.mx_ = None
        self.my = None
        self.my_ = None

        # Reações
        self.Vx = None
        self.Vx_ = None
        self.Vy = None
        self.Vy_ = None

        # Momentos
        self.Mx = None
        self.My = None
        self.Xx1 = None
        self.Xx2 = None
        self.Xy1 = None
        self.Xy2 = None

        self.omega = None
        self.verFlecha = None

    def verificar_els_deformacao(self, omega):
        self.omega = omega
        D = (self.config.Ecs * self.h ** 3) / 12
        fi = (omega * self.carga.carga_total * self.lx ** 4) / D

        ksi_t = 0.68
        alfa_f = ksi_t
        fdif = alfa_f * fi
        ftotal = fi + fdif

        if ftotal <= self.lx / 250:
            self.verFlecha = True
            return True
        else:
            self.verFlecha = False
            return False

    def calc_cargas(self,
                    superior_espessura, superior_densidade,
                    inferior_espessura, inferior_densidade,
                    contrapiso_espessura, contrapiso_densidade,
                    parede_caso, parede_espessura, parede_perimetro, parede_altura,
                    carga_utilizacao):
        self.carga = Carga(superior_espessura, superior_densidade,
                           inferior_espessura, inferior_densidade,
                           contrapiso_espessura, contrapiso_densidade,
                           parede_caso, parede_espessura, parede_perimetro, parede_altura,
                           carga_utilizacao,
                           self.lx, self.ly, self.h)

    def calc_reacoes(self, vx, vx_, vy, vy_):
        self.vx = vx
        self.vx_ = vx_
        self.vy = vy
        self.vy_ = vy_

        try:
            self.Vx = self.vx * self.carga.carga_total * self.lx / 10
        except:
            self.Vx = None
        try:
            self.Vx_ = self.vx_ * self.carga.carga_total * self.lx / 10
        except:
            self.Vx_ = None
        try:
            self.Vy = self.vy * self.carga.carga_total * self.lx / 10
        except:
            self.Vy = None
        try:
            self.Vy_ = self.vy_ * self.carga.carga_total * self.lx / 10
        except:
            self.Vy_ = None

    def calc_momentos(self, mx=0, mx_=0, my=0, my_=0):
        self.mx = mx
        self.mx_ = mx_
        self.my = my
        self.my_ = my_

        if self.lamb <= 2:
            self.Mx = Momento(self.mx * self.carga.carga_total * (self.lx ** 2) / 100, 'Mx', self)
            self.My = Momento(self.my * self.carga.carga_total * (self.lx ** 2) / 100, 'My', self)

            if self.apoio == 'Caso 1':
                pass
            elif self.apoio == 'Caso 2A':
                self.Xx1 = Momento(self.mx_ * self.carga.carga_total * (self.lx ** 2) / 100, 'Xx1', self)
            elif self.apoio == 'Caso 2B':
                self.Xy1 = Momento(self.mx_ * self.carga.carga_total * (self.lx ** 2) / 100, 'Xx1', self)
            elif self.apoio == 'Caso 3':
                self.Xx1 = Momento(self.mx_ * self.carga.carga_total * (self.lx ** 2) / 100, 'Xx1', self)
                self.Xy1 = Momento(self.my_ * self.carga.carga_total * (self.lx ** 2) / 100, 'Xy1', self)
            elif self.apoio == 'Caso 4A':
                self.Xx1 = Momento(self.mx_ * self.carga.carga_total * (self.lx ** 2) / 100, 'Xx1', self)
                self.Xx2 = Momento(self.mx_ * self.carga.carga_total * (self.lx ** 2) / 100, 'Xx2', self)
            elif self.apoio == 'Caso 4B':
                self.Xy1 = Momento(self.my_ * self.carga.carga_total * (self.lx ** 2) / 100, 'Xy1', self)
                self.Xy2 = Momento(self.my_ * self.carga.carga_total * (self.lx ** 2) / 100, 'Xy2', self)
            elif self.apoio == 'Caso 5A':
                self.Xx1 = Momento(self.mx_ * self.carga.carga_total * (self.lx ** 2) / 100, 'Xx1', self)
                self.Xy1 = Momento(self.my_ * self.carga.carga_total * (self.lx ** 2) / 100, 'Xy1', self)
                self.Xy2 = Momento(self.mx_ * self.carga.carga_total * (self.lx ** 2) / 100, 'Xx2', self)
            elif self.apoio == 'Caso 5B':
                self.Xx1 = Momento(self.mx_ * self.carga.carga_total * (self.lx ** 2) / 100, 'Xx1', self)
                self.Xx2 = Momento(self.my_ * self.carga.carga_total * (self.lx ** 2) / 100, 'Xy2', self)
                self.Xy1 = Momento(self.my_ * self.carga.carga_total * (self.lx ** 2) / 100, 'Xy1', self)
            elif self.apoio == 'Caso 6':
                self.Xx1 = Momento(self.mx_ * self.carga.carga_total * (self.lx ** 2) / 100, 'Xx1', self)
                self.Xx2 = Momento(self.mx_ * self.carga.carga_total * (self.lx ** 2) / 100, 'Xx2', self)
                self.Xy1 = Momento(self.my_ * self.carga.carga_total * (self.lx ** 2) / 100, 'Xy1', self)
                self.Xy2 = Momento(self.my_ * self.carga.carga_total * (self.lx ** 2) / 100, 'Xy2', self)
        else:
            self.Mx = Momento(self.mx * self.carga.carga_total * (self.lx ** 2) / 100, 'Mx', self)
            self.Xx1 = Momento(self.mx_ * self.carga.carga_total * (self.lx ** 2) / 100, 'Xx1', self)
            self.Xy1 = Momento(self.my_ * self.carga.carga_total * (self.lx ** 2) / 100, 'Xy1', self)

    def __repr__(self):
        return 'Laje L{}'.format(self.numero)


class Carga:
    def __init__(self,
                 superior_espessura, superior_densidade,
                 inferior_espessura, inferior_densidade,
                 contrapiso_espessura, contrapiso_densidade,
                 parede_caso, parede_espessura, parede_perimetro, parede_altura,
                 carga_utilizacao, lx, ly, h):
        self.superior_espessura = superior_espessura
        self.superior_densidade = superior_densidade
        self.inferior_espessura = inferior_espessura
        self.inferior_densidade = inferior_densidade
        self.contrapiso_espessura = contrapiso_espessura
        self.contrapiso_densidade = contrapiso_densidade
        self.parede_caso = parede_caso
        self.parede_espessura = parede_espessura
        self.parede_perimetro = parede_perimetro
        self.parede_altura = parede_altura
        self.carga_utilizacao = carga_utilizacao

        self.superior_carga = self.superior_espessura * self.superior_densidade
        self.inferior_carga = self.inferior_espessura * self.inferior_densidade
        self.contrapiso_carga = self.contrapiso_espessura * self.contrapiso_densidade

        self.parede_densidade = 13000 * (self.parede_espessura - 0.05) + 21000 * 0.05
        if self.parede_perimetro == 0 or self.parede_espessura == 0:
            self.parede_carga = 0
        elif self.parede_caso == 'Laje em cruz':
            self.parede_carga = self.parede_densidade * self.parede_perimetro * self.parede_altura / (lx * ly)
        elif self.parede_caso == 'Paralelo ao menor vão':
            self.parede_carga = 2 * self.parede_densidade * self.parede_altura * self.parede_perimetro / (lx ** 2)
        elif self.parede_caso == 'Perpendicular ao menor vão':
            raise AttributeError('Dimensionar como viga!')

        self.peso_proprio = h * 25000

        self.carga_permanente = self.superior_carga + self.inferior_carga + self.contrapiso_carga + self.parede_carga + \
                                self.peso_proprio
        self.carga_total = self.carga_utilizacao + self.carga_permanente


class Momento:
    id_num = 1

    def __init__(self, momento_calc, tipo, laje):
        self.momento_calc = momento_calc
        self.tipo = tipo
        self.numero_laje = laje.numero
        self.lx = laje.lx
        self.ly = laje.ly
        self.h = laje.h
        self.config = laje.config

        self.momento_compt = {None: self.momento_calc}
        self.armadura = {}
        self.id_compt = self.id_num
        Momento.id_num += 1

    def compatibilizar_momentos(self, other):
        if None in self.momento_compt:
            self.momento_compt = {}
        if None in other.momento_compt:
            other.momento_compt = {}

        mc = max((self.momento_calc + other.momento_calc) / 2, 0.8 * max(self.momento_calc, other.momento_calc))
        self.momento_compt.update({other: mc})
        other.momento_compt.update({self: mc})
        other.id_compt = self.id_num

        return mc

    def dimensionar(self, vizinho, M):
        if self.tipo == 'Mx' or self.tipo == 'Xx1' or self.tipo == 'Xx2':
            s_max = min(2 * self.h, 0.2)
        else:
            s_max = 0.33
        s_min = 0.1
        step = 0.005

        s_list = list(np.arange(s_max, s_min - step, -step))
        for i in barras:
            flag = False
            for j in s_list:
                diametro = i
                espacamento = j

                d = self.h - self.config.c_laje - diametro / 2

                Msd = self.config.gama_f * M
                kmd = Msd / (self.config.fcd * d ** 2)
                kx = (1 - np.sqrt(1 - 2 * kmd / self.config.alfa_c)) / self.config.lamb
                kz = 1 - 0.5 * self.config.lamb * kx
                As_calc = Msd / (kz * d * self.config.fyd)

                As = (np.pi * (diametro / 2) ** 2) / (espacamento + diametro)
                if As < As_calc:
                    continue

                if not self.verificar_tudo(kmd, As, diametro, espacamento):
                    continue
                else:
                    flag = True
                    break

            if flag:
                break

        dominio = self.verificar_dominio(kx)

        if self.tipo == 'Mx':
            comprimento = self.lx
        elif self.tipo == 'My':
            comprimento = self.ly
        elif self.tipo == 'Xx1' or self.tipo == 'Xx2':
            comprimento = 0.25 * self.lx + 0.25 * vizinho.lx
        elif self.tipo == 'Xy1' or self.tipo == 'Xy2':
            comprimento = 0.25 * self.ly + 0.25 * vizinho.ly

        self.armadura.update({vizinho: Armadura(diametro, espacamento, comprimento, d, kmd, kx, kz, As, dominio)})

    def dimensionar_todos(self):
        for vizinho, M in self.momento_compt.items():
            self.dimensionar(vizinho, M)

    def verificar_kmdlim(self, kmd):
        fck = self.config.fck
        if fck <= 50e6:
            if kmd <= 0.251:
                return True
        elif fck <= 55e6:
            if kmd <= 0.197:
                return True
        elif fck <= 60e6:
            if kmd <= 0.189:
                return True
        elif fck <= 65e6:
            if kmd <= 0.182:
                return True
        elif fck <= 70e6:
            if kmd <= 0.174:
                return True
        elif fck <= 75e6:
            if kmd <= 0.167:
                return True
        elif fck <= 80e6:
            if kmd <= 0.160:
                return True
        elif fck <= 85e6:
            if kmd <= 0.153:
                return True
        elif fck <= 90e6:
            if kmd <= 0.146:
                return True
        return False

    def verificar_dominio(self, kx):
        kxlim23 = 0.259
        kxlim34 = 0.628
        kxlim44a = 1
        if kx < kxlim23:
            return 'Domínio 1 ou 2'
        elif kx < kxlim34:
            return 'Domínio 3'
        elif kx < kxlim34:
            return 'Domínio 4'
        else:
            return 'Domínio 4a ou 5'

    def verificar_taxa_de_armadura(self, As):
        h = self.h
        fck = self.config.fck

        if fck <= 30e6:
            rho_min = 0.0015
        elif fck <= 35e6:
            rho_min = 0.00164
        elif fck <= 40e6:
            rho_min = 0.00179
        elif fck <= 45e6:
            rho_min = 0.00194
        elif fck <= 50e6:
            rho_min = 0.00208
        elif fck <= 55e6:
            rho_min = 0.00211
        elif fck <= 60e6:
            rho_min = 0.00219
        elif fck <= 65e6:
            rho_min = 0.00226
        elif fck <= 70e6:
            rho_min = 0.00233
        elif fck <= 75e6:
            rho_min = 0.00239
        elif fck <= 80e6:
            rho_min = 0.00245
        elif fck <= 85e6:
            rho_min = 0.00251
        elif fck <= 90e6:
            rho_min = 0.00256

        Asmin = rho_min * 1 * h
        Asmax = 0.04 * 1 * h

        return Asmin < As < h

    def verificar_bitola(self, diametro):
        return diametro < self.h / 8

    def verificar_espacamento(self, espacamento):
        if self.tipo == 'Mx' or self.tipo == 'Xx1' or self.tipo == 'Xx2':
            s_max = min(2 * self.h, 0.2)
        else:
            s_max = 0.33

        s_min = 0.1

        return s_min < espacamento < s_max

    def verificar_tudo(self, kmd, As, diametro, espacamento):
        # print(self.verificar_kmdlim(kmd), self.verificar_taxa_de_armadura(As),
        #       self.verificar_bitola(diametro), self.verificar_espacamento(espacamento, momento))
        return self.verificar_kmdlim(kmd) and self.verificar_taxa_de_armadura(As) and \
               self.verificar_bitola(diametro) and self.verificar_espacamento(espacamento)


class Armadura:
    def __init__(self, diametro, espacamento, comprimento, d, kmd, kx, kz, As, dominio):
        self.diametro = diametro
        self.espacamento = espacamento
        self.comprimento = comprimento
        self.d = d
        self.kmd = kmd
        self.kx = kx
        self.kz = kz
        self.As = As
        self.dominio = dominio

    def __repr__(self):
        s = '''Diâmetro: {:.1f} mm
    Espacamento: {:.1f} cm
    Comprimento: {:.2f} m
    Altura útil: {:.1f} cm'''.format(self.diametro * 1e3, self.espacamento * 100, self.comprimento, self.d * 100)
        return s


if __name__ == '__main__':
    laje1 = Laje(1, 6, 6, .12, 'Caso 1')
    laje1.calc_cargas(0.007, 18000, 0.015, 12500, 0.015, 21000, 'Laje em cruz', 0.15, 2, 2.6, 2000)
    laje1.calc_momentos(mx=4.23, my=4.23)
    laje1.Mx.dimensionar_todos()
    print(laje1)
    print(laje1.Mx.armadura[None])
    print(laje1.Mx.armadura[None].dominio)
