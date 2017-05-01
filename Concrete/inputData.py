from ConcretePy.Concrete.configuracoes import Configuracoes


class InputData:
    def __init__(self, lajes={}, vigas={}, pilares={}, config=Configuracoes()):
        self.lajes = lajes
        self.vigas = vigas
        self.pilares = pilares
        self.config = config
        self.table_rows_compat_lajes = []
        self.table_rows_compat_lajes_indices = []
