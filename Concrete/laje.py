class Laje:
    def __init__(self, numero, lx, ly, h, apoio):
        self.numero = numero
        self.lx = lx
        self.ly = ly
        self.h = h
        self.apoio = apoio

        self.lamb = self.ly / self.lx

        self.carga = None
        self.kx = None
        self.mx = None
        self.nx = None
        self.my = None
        self.ny = None

    def calc_cargas(self,
                    superior_espessura, superior_densidade,
                    inferior_espessura, inferior_densidade,
                    contrapiso_espessura, contrapiso_densidade,
                    parede_caso, parede_espessura, parede_perimetro, parede_altura,
                    carga_utilizacao):
        self.carga = Load(superior_espessura, superior_densidade,
                          inferior_espessura, inferior_densidade,
                          contrapiso_espessura, contrapiso_densidade,
                          parede_caso, parede_espessura, parede_perimetro, parede_altura,
                          carga_utilizacao,
                          self.lx, self.ly)

    def calc_momentos(self, kx=None, mx=None, nx=None, my=None, ny=None):
        self.kx = kx
        self.mx = mx
        self.nx = nx
        self.my = my
        self.ny = ny

        # TODO definir momentos para lambda > 2 e lambda < 2

    def compatibilizar_momentos(self):
        pass
        # TODO compatibilizar momentos

    def dimensionar(self):
        pass
        # TODO dimensionar para os momentos

    def verificar_tudo(self):
        pass
        # TODO verificar itens de norma

    def calc_ancoragem(self):
        pass
        # TODO calcular ancoragens


class Load:
    def __init__(self,
                 superior_espessura, superior_densidade,
                 inferior_espessura, inferior_densidade,
                 contrapiso_espessura, contrapiso_densidade,
                 parede_caso, parede_espessura, parede_perimetro, parede_altura,
                 carga_utilizacao,
                 lx, ly):
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

        if self.parede_perimetro == 0 or self.parede_espessura == 0:
            pass
        elif self.parede_caso == 'Laje em cruz':
            self.parede_carga = self.parede_espessura * self.parede_perimetro * self.parede_altura / (lx * ly)
        elif self.parede_caso == 'Paralelo ao menor vão':
            self.parede_carga = 2 * self.parede_espessura * self.parede_altura * self.parede_perimetro / (lx ** 2)
        elif self.parede_caso == 'Perpendicular ao menor vão':
            raise AttributeError('Dimensionar como viga!')

        self.carga_permanente = self.superior_carga + self.inferior_carga + self.contrapiso_carga + self.parede_carga
        self.carga_total = self.carga_utilizacao + self.carga_permanente
