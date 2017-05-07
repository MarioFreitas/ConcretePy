import numpy as np


class Configuracoes:
    def __init__(self):
        # Fatores de Segurança
        self.gama_f = 1.4
        self.gama_c = 1.4
        self.gama_s = 1.15

        # Cobrimentos
        self.c_min_laje = 0.02
        self.c_min_viga_pilar = 0.025
        self.c_min_solo = 0.03
        self.c_laje = self.c_min_laje
        self.c_viga = self.c_min_viga_pilar
        self.c_pilar = self.c_min_viga_pilar
        self.c_solo = self.c_min_solo

        # Fissuras
        self.w_k_max = 0.0004

        # Britas
        self.brita = 'Brita 1 - granito'
        self.diametro_brita = 0.0019
        self.alfa_e = 1.0

        # Propriedades do Concreto
        self.fck = 30e6
        self.fct_m = (0.3 * (self.fck / 1e6) ** (2 / 3)) * 1e6
        self.fctk_inf = 0.7 * self.fct_m
        self.fctk_sup = 1.3 * self.fct_m
        self.fctd = self.fctk_inf / self.gama_c
        self.fcd = self.fck / self.gama_c
        self.lamb = 0.8
        self.alfa_c = 0.85
        self.Eci = (self.alfa_e * 5600 * ((self.fck / 1e6) ** (1 / 2))) * 1e6
        self.alfa_i = min(1., 0.8 + 0.2 * (self.fck / 1e6) / 80)
        self.Ecs = self.alfa_i * self.Eci
        self.alfa_v2 = 1 - (self.fck/1e6)/250

        # Propriedades do Aço
        self.fyk = 500e6
        self.fyd = self.fyk / self.gama_s
        self.fywk = self.fyk
        self.fywd = self.fyd
        self.Es = 210e9


    def mudar_c_min(self, valor):
        self.c_min_laje = valor
        if self.c_laje < self.c_min_laje:
            self.c_laje = self.c_min_laje

    def mudar_fck(self, valor):
        self.fck = valor
        self.fcd = self.fck / 1.4
        self.alfa_i = min(1., 0.8 + 0.2 * (self.fck / 1e6) / 80)
        self.alfa_v2 = 1 - (self.fck / 1e6) / 250

        if self.fck <= 50e6:
            self.fct_m = (0.3 * (self.fck / 1e6) ** (2 / 3)) * 1e6
            self.fctk_inf = 0.7 * self.fct_m
            self.fctk_sup = 1.3 * self.fct_m
            self.lamb = 0.8
            self.alfa_c = 0.85
            self.Eci = (self.alfa_e * 5600 * ((self.fck / 1e6) ** (1 / 2))) * 1e6
            self.Ecs = self.alfa_i * self.Eci

        else:
            self.fct_m = (2.12 * np.log(1 + 0.11 * (self.fck / 1e6))) * 1e6
            self.fctk_inf = 0.7 * self.fct_m
            self.fctk_sup = 1.3 * self.fct_m
            self.lamb = (0.8 - ((self.fck / 1e6) - 50) / 400) * 1e6
            self.alfa_c = (0.85 * (1 - ((self.fck / 1e6) - 50) / 200)) * 1e6
            self.Eci = (21.5 * 1e3 * self.alfa_e * 5600 * (((self.fck / 1e6) / 10 + 1.25) ** (1 / 3))) * 1e6
            self.Ecs = self.alfa_i * self.Eci
