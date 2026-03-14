import heapq
from collections import deque
from NodeP import NodeP


class buscaP(object):

    def __init__(self):
        self.contador_push = 0

    # --------------------------------------------------------------------------
    # SUCESSORES PARA GRID
    # --------------------------------------------------------------------------
    def sucessores_grid(self, st, nx, ny, mapa, mapa_custo):
        f = []
        x, y = st[0], st[1]
        # DIREITA
        if y + 1 < ny:
            if mapa[x][y + 1] == 0:
                suc = [x, y + 1]
                custo = mapa_custo[x][y + 1]

                f.append((suc, custo))

        # ESQUERDA
        if y - 1 >= 0:
            if mapa[x][y - 1] == 0:
                suc = [x, y - 1]
                custo = mapa_custo[x][y - 1]
                f.append((suc, custo))

        # ABAIXO
        if x + 1 < nx:
            if mapa[x + 1][y] == 0:
                suc = [x + 1, y]
                custo = mapa_custo[x + 1][y]

                f.append((suc, custo))

        # ACIMA
        if x - 1 >= 0:
            if mapa[x - 1][y] == 0:
                suc = [x - 1, y]
                custo = mapa_custo[x - 1][y]
                f.append((suc, custo))
        return f

    # --------------------------------------------------------------------------
    # INSERE NA LISTA MANTENDO-A ORDENADA
    # --------------------------------------------------------------------------
    def inserir_ordenado(self, lista, no):
        for i, n in enumerate(lista):
            if no.v1 < n.v1:
                lista.insert(i, no)
                break
        else:
            lista.append(no)

    # --------------------------------------------------------------------------
    # EXIBE O CAMINHO ENCONTRADO NA ÁRVORE DE BUSCA
    # --------------------------------------------------------------------------
    def exibirCaminho(self, node):
        caminho = []
        while node is not None:
            caminho.append(node.estado)
            node = node.pai
        caminho.reverse()
        return caminho

    # --------------------------------------------------------------------------
    # GERA H DE FORMA ALEATÓRIA
    # --------------------------------------------------------------------------
    def heuristica_manhattan(self, estado_atual, estado_destino):
        # estado é (x, y)
        x_atual, y_atual = estado_atual
        x_destino, y_destino = estado_destino

        # h(n) = |x1 - x2| + |y1 - y2|
        return abs(x_atual - x_destino) + abs(y_atual - y_destino)
    # -----------------------------------------------------------------------------
    # CUSTO UNIFORME
    # -----------------------------------------------------------------------------

    def custo_uniforme(self, inicio, fim, nx, ny, mapa, mapa_custo): #grafo
        # Origem igual a destino
        if inicio == fim:
            return [inicio]

        t_inicio = tuple(inicio)
        t_fim = tuple(fim)

        fila_prioridade = []
        raiz = NodeP(None, t_inicio, custo_g=0, custo_h=0) # grafo
        self.contador_push += 1

        heapq.heappush(fila_prioridade, (raiz.v1, self.contador_push,raiz))

        visitado = {t_inicio: raiz}

        # loop de busca
        while fila_prioridade:
            # remove o primeiro nó
            _, _, atual = heapq.heappop(fila_prioridade)

            if atual.custo_g > visitado[atual.estado].custo_g:
                continue

            # Chegou ao objetivo: UCS garante ótimo (custos >= 0)
            if atual.estado == t_fim:
                caminho = self.exibirCaminho(atual)
                return caminho, atual.custo_g

            # Gera sucessores a partir do grid
            filhos = self.sucessores_grid(atual.estado, nx, ny, mapa, mapa_custo)  # grid

            for novo_estado_list, custo_aresta in filhos:
                t_novo = tuple(novo_estado_list)
                # custo acumulado até o sucessor
                novo_custo_g = atual.custo_g + custo_aresta
                v1 = novo_custo_g

                if (t_novo not in visitado) or (novo_custo_g < visitado[t_novo].custo_g):
                    filho = NodeP(atual, t_novo, custo_g=novo_custo_g, custo_h=0)  # grid
                    self.contador_push += 1

                    visitado[t_novo] = filho
                    heapq.heappush(fila_prioridade, (filho.v1, self.contador_push, filho))

        # Sem caminho
        return None, None

    # -----------------------------------------------------------------------------
    # GREEDY
    # -----------------------------------------------------------------------------
    def greedy(self, inicio, fim, nx, ny, mapa, mapa_custo):
        self.contador_push = 0

        if inicio == fim:
            return [inicio], 0

        t_inicio = tuple(inicio)
        t_fim = tuple(fim)

        fila_prioridade = []

        custo_h_inicial = self.heuristica_manhattan(t_inicio, t_fim)

        # Inicialize o custo_f para consistência, embora não seja usado como prioridade no Greedy
        raiz = NodeP(None, t_inicio, custo_g=0, custo_h=custo_h_inicial)

        self.contador_push += 1

        heapq.heappush(fila_prioridade, (raiz.custo_h, self.contador_push, raiz))

        # Controle de nós visitados
        visitado = {t_inicio: raiz}

        # loop de busca
        while fila_prioridade:
            # remove o primeiro nó
            _, _, atual = heapq.heappop(fila_prioridade)

            if atual.estado == t_fim:
                # Retorna o caminho e o custo G real.
                caminho = self.exibirCaminho(atual)
                return caminho, atual.custo_g, atual.custo_h

            filhos = self.sucessores_grid(atual.estado, nx, ny, mapa, mapa_custo)

            for novo_estado_list, custo_aresta in filhos:
                t_novo = tuple(novo_estado_list)

                novo_custo_g = atual.custo_g + custo_aresta
                novo_custo_h = self.heuristica_manhattan(t_novo, t_fim)
                novo_custo_f = novo_custo_g + novo_custo_h

                if t_novo not in visitado:
                    filho = NodeP(atual, t_novo, custo_g=novo_custo_g, custo_h=novo_custo_h)
                    self.contador_push += 1


                    visitado[t_novo] = filho
                    heapq.heappush(fila_prioridade, (filho.custo_h, self.contador_push, filho))

        # Sem caminho
        return None, None

    # -----------------------------------------------------------------------------
    # A ESTRELA
    # -----------------------------------------------------------------------------
    def a_estrela(self, inicio, fim, nx, ny, mapa, mapa_custo):
        self.contador_push = 0

        if inicio == fim:
            return [inicio], 0, 0

        t_inicio = tuple(inicio)
        t_fim = tuple(fim)

        fila_prioridade = []

        custo_h_inicial = self.heuristica_manhattan(t_inicio, t_fim)
        raiz = NodeP(None, t_inicio, custo_g=0, custo_h=custo_h_inicial)
        self.contador_push += 1

        # Prioridade: f = g + h
        heapq.heappush(fila_prioridade, (raiz.custo_g + raiz.custo_h, self.contador_push, raiz))

        visitado = {t_inicio: raiz}

        while fila_prioridade:
            _, _, atual = heapq.heappop(fila_prioridade)

            if atual.custo_g > visitado[atual.estado].custo_g:
                continue

            if atual.estado == t_fim:
                caminho = self.exibirCaminho(atual)
                return caminho, atual.custo_g, atual.custo_h

            # Sucessores do grid
            filhos = self.sucessores_grid(atual.estado, nx, ny, mapa, mapa_custo)

            for novo_estado_list, custo_aresta in filhos:
                t_novo = tuple(novo_estado_list)
                novo_custo_g = atual.custo_g + custo_aresta
                novo_custo_h = self.heuristica_manhattan(t_novo, t_fim)

                if (t_novo not in visitado) or (novo_custo_g < visitado[t_novo].custo_g):
                    filho = NodeP(atual, t_novo, custo_g=novo_custo_g, custo_h=novo_custo_h)
                    self.contador_push += 1
                    visitado[t_novo] = filho
                    heapq.heappush(fila_prioridade, (filho.custo_g + filho.custo_h, self.contador_push, filho))

        # Sem caminho
        return None, None, None

    # -----------------------------------------------------------------------------
    # AI ESTRELA
    # -----------------------------------------------------------------------------
    def aia_estrela(self, inicio, fim, nx, ny, mapa, mapa_custo):
        self.contador_push = 0

        if inicio == fim:
            return [inicio], 0, 0

        t_inicio = tuple(inicio)
        t_fim = tuple(fim)

        if not hasattr(self, "heuristicas_adaptadas"):
            self.heuristicas_adaptadas = {}

        def h_adaptada(estado):
            if estado in self.heuristicas_adaptadas:
                return self.heuristicas_adaptadas[estado]
            else:
                return self.heuristica_manhattan(estado, t_fim)

        # Limite inicial de f = g + h
        limite = h_adaptada(t_inicio)

        while True:
            lim_acima = []
            lista = deque()
            visitado = {}

            raiz = NodeP(None, t_inicio, custo_g=0, custo_h=h_adaptada(t_inicio))
            lista.append(raiz)
            visitado[t_inicio] = raiz

            while lista:
                atual = lista.popleft()
                f_atual = atual.custo_g + atual.custo_h

                if atual.estado == t_fim:
                    caminho = self.exibirCaminho(atual)

                    custo_objetivo = atual.custo_g
                    for no_visitado in visitado.values():
                        g_n = no_visitado.custo_g
                        self.heuristicas_adaptadas[no_visitado.estado] = max(
                            0, custo_objetivo - g_n
                        )
                    # ---------------------------------------------------

                    return caminho, atual.custo_g, limite

                # Gera sucessores a partir do grid
                filhos = self.sucessores_grid(atual.estado, nx, ny, mapa, mapa_custo)

                for novo_estado_list, custo_aresta in filhos:
                    t_novo = tuple(novo_estado_list)
                    novo_g = atual.custo_g + custo_aresta
                    novo_h = h_adaptada(t_novo)
                    f_novo = novo_g + novo_h

                    if f_novo <= limite:
                        if (t_novo not in visitado) or (novo_g < visitado[t_novo].custo_g):
                            filho = NodeP(atual, t_novo, custo_g=novo_g, custo_h=novo_h)
                            visitado[t_novo] = filho
                            self.inserir_ordenado(lista, filho)
                    else:
                        lim_acima.append(f_novo)

            if lim_acima:
                limite = sum(lim_acima) / len(lim_acima)
            else:
                return None, None, None
