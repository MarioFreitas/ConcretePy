from ConcretePy.Concrete.configurações import Configurações


class InputData:
    def __init__(self, lajes={}, vigas={}, pilares={}, config=Configurações()):
        self.lajes = lajes
        self.vigas = vigas
        self.pilares = pilares
        self.config = config
