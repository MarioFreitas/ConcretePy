class Configurações:
    def __init__(self):
        self.gama_f = 1.4

        self.c_min_laje = 0.02
        self.c_laje = self.c_min_laje

        self.fck = 35e6
        self.fcd = self.fck / 1.4

        self.fyk = 500e6
        self.fyd = self.fyk/1.1

        self.lamb = 0.8
        self.alfa_c = 0.85

    def mudar_c_min(self, valor):
        self.c_min_laje = valor
        if self.c_laje < self.c_min_laje:
            self.c_laje = self.c_min_laje

    def mudar_fck(self, valor):
        self.fck = valor
        self.fcd = self.fck / 1.4

        if self.fck > 50e6:
            self.lamb = 0.8 - (self.fck - 50)/400
            self.alfa_c = 0.85*(1 - (self.fck - 50)/200)
