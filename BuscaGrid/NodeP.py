from Node import Node

class NodeP(Node):
    def __init__(self, pai=None, estado=None, custo_g=0,
                 anterior=None, proximo=None, custo_h=0):
        super().__init__(pai, estado, custo_g, anterior, proximo)
        self.custo_g = custo_g  # O custo real do caminho (g(n)). Sobrescreve v1 com um nome claro.
        self.custo_h = custo_h  # O custo heurístico/adicional (h(n))
        self.custo_f = self.custo_g + self.custo_h  # O custo total f(n) para A*

    def __lt__(self, other):
        # Esta comparação é usada para ordenar a fila de prioridade
        return self.custo_f < other.custo_f