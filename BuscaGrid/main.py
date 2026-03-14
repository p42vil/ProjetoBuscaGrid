import TextoGrid
import tkinter as tk
from tkinter import ttk

from BuscaNP import buscaNP
from BuscaP import buscaP

# pegar texto do arquivo mapa.txt
with open("mapa.txt", "r") as file:
    texto = file.read()

# pegar texto do arquivo mapa.txt
with open("mapa_ponderado.txt", "r") as file:
    texto_ponderado = file.read()

# criação de grid
grid = TextoGrid.converterTextoGrid(texto)
int_grid = TextoGrid.converterTextoGridInt(texto)
int_ponderado_grid = TextoGrid.converterTextoGridPonderadoInt(texto_ponderado)
cell_size = 15

# nx e ny
max_width = 0 # nx
max_height = len(grid) # ny

for row in grid:
    max_width = max(max_width, len(row))

# algoritmo
buscar = buscaNP()
buscaP = buscaP()

class GridApp:
    desenharcaminho = False
    desenhado = False

    # célula de inicio
    escolhendoInicio = False
    iniciocell = [-1, -1]

    # células finais
    escolhendoFinal = False
    finalcell = []

    caminho = None

    def __init__(self, master):
        self.master = master
        master.title("Segurança operacional")

        frame = tk.Frame(root)
        frame.pack(padx=30, pady=30, side=tk.LEFT)

        # BUSCA
        buscalist = ["AMPLITUDE", "PROFUNDIDADE", "PROFUNDIDADE LIMITADA",
                 "APROFUNDAMENTO ITERATIVO", "BIDIRECIONAL", "CUSTO UNIFORME", "GREEDY", "A*", "AIA*"]

        # mostra limite para algs com limite
        def on_combobox_select(event):
            if self.Combo.get() == "PROFUNDIDADE LIMITADA" or self.Combo.get() == "APROFUNDAMENTO ITERATIVO":
                self.inicio.pack_forget()
                self.final.pack_forget()
                self.fazer.pack_forget()

                self.label.pack(padx=5, pady=5)
                self.limite.pack(padx=5, pady=5)
                self.inicio.pack(padx=5, pady=5)
                self.final.pack(padx=5, pady=5)
                self.fazer.pack(padx=5, pady=10)
            else:
                self.label.pack_forget()
                self.limite.pack_forget()

        self.Combo = ttk.Combobox(frame, values=buscalist, state='readonly', width=30)
        #self.Combo.set("Escolher um método de busca")
        self.Combo.set("A*")
        self.Combo.pack(padx=5, pady=5)
        self.Combo.bind('<<ComboboxSelected>>', on_combobox_select)


        # LIMITE
        # verificar se é numeral
        def callback(P):
            return str.isdigit(P) or P == ""
        vcmd = (root.register(callback))

        # começar como 0
        initial_text_var = tk.StringVar(value="0")

        self.limite = tk.Entry(frame, width=10, validate='all', validatecommand=(vcmd, '%P'), textvariable=initial_text_var)
        self.limite.pack(padx=5, pady=5)
        self.limite.pack_forget()

        self.label = ttk.Label(frame, text="Limite:")
        self.label.pack(padx=5, pady=5)
        self.label.pack_forget()


        # INICIO
        self.inicio = tk.Button(frame, text="Escolher a célula de inicio", command=self.escolherInicio)
        self.inicio.pack(padx=5, pady=5)


        # FINAL
        self.final = tk.Button(frame, text="Escolher a célula do fim", command=self.escolherFinal)
        self.final.pack(padx=5, pady=5)


        # FAZER BUSCA
        self.fazer = tk.Button(frame, text="Fazer busca", command=self.fazerBusca)
        self.fazer.pack(padx=5, pady=10)


        # XY
        xlabel = tk.Label(root, text="y", font=("Arial", 10), fg="blue")
        xlabel.pack(side=tk.LEFT)
        ylabel = tk.Label(root, text="x", font=("Arial", 10), fg="blue")
        ylabel.pack()


        # GRID
        self.canvas = tk.Canvas(master, width=(max_width*cell_size)+cell_size, height=(max_height*cell_size)+cell_size, bg="white")
        self.canvas.pack(padx=10, pady=10, side=tk.LEFT)

        self.cell_size = cell_size  # Size of each cell in pixels
        self.cells = {}  # Dictionary to store cell IDs for easy access

        self.desenhar_grid()

        self.canvas.bind("<Button-1>", self.cell_click)

    def escolherInicio(self):
        self.escolhendoFinal = False
        self.final.config(text="Escolher a célula do final")

        if self.escolhendoInicio == True:
            self.escolhendoInicio = False
            self.inicio.config(text="Escolher a célula de inicio")
        else:
            self.escolhendoInicio = True
            self.inicio.config(text="Escolhendo")

    def escolherFinal(self):
        self.escolhendoInicio = False
        self.inicio.config(text="Escolher a célula de inicio")

        if self.escolhendoFinal == True:
            self.escolhendoFinal = False
            self.final.config(text="Escolher a célula do final")
        else:
            self.escolhendoFinal = True
            self.final.config(text="Escolhendo")

    def desabilitarEscolhas(self):
        self.escolhendoInicio = False
        self.escolherFinal = False
        self.inicio.config(text="Escolher a célula de inicio")
        self.final.config(text="Escolher a célula do final")

    def fazerBusca(self):
        tamanho = float('inf')
        custo_otimo = float('inf')
        custo_h_otimo = float('inf')

        destino = None
        self.caminho = None

        self.desabilitarEscolhas()

        # menor caminho entre os caminhos feitos

        match self.Combo.get():
            # não ponderado
            case "AMPLITUDE":
                for cell in self.finalcell:
                    alg = buscaNP.amplitude(buscar, self.iniciocell, cell, max_height, max_width, int_grid)
                    if alg != None:
                        if len(alg) < tamanho:
                            tamanho = len(alg)
                            self.caminho = alg
            case "PROFUNDIDADE":
                for cell in self.finalcell:
                    alg = buscaNP.profundidade(buscar, self.iniciocell, cell, max_height, max_width, int_grid)
                    if alg != None:
                        if len(alg) < tamanho:
                            tamanho = len(alg)
                            self.caminho = alg
            case "PROFUNDIDADE LIMITADA":
                for cell in self.finalcell:
                    alg = buscaNP.prof_limitada(buscar, self.iniciocell, cell, max_height, max_width, int_grid, int(self.limite.get()))
                    if alg != None:
                        if len(alg) < tamanho:
                            tamanho = len(alg)
                            self.caminho = alg
            case "APROFUNDAMENTO ITERATIVO":
                for cell in self.finalcell:
                    alg = buscaNP.aprof_iterativo(buscar, self.iniciocell, cell, max_height, max_width, int_grid, int(self.limite.get()))
                    if alg != None:
                        if len(alg) < tamanho:
                            tamanho = len(alg)
                            self.caminho = alg
            case "BIDIRECIONAL":
                for cell in self.finalcell:
                    alg = buscaNP.bidirecional(buscar, self.iniciocell, cell, max_height, max_width, int_grid)
                    if alg != None:
                        if len(alg) < tamanho:
                            tamanho = len(alg)
                            self.caminho = alg

            # ponderado
            # considera custo para saber melhor caminho

            case "CUSTO UNIFORME":
                for cell in self.finalcell:
                    alg, custo = buscaP.custo_uniforme(self.iniciocell, cell, max_height, max_width, int_grid, int_ponderado_grid)
                    if alg != None:
                        if custo < custo_otimo:
                            custo_otimo = custo
                            self.caminho = alg
            case "GREEDY":
                for cell in self.finalcell:
                    alg, custo_g, custo_h = buscaP.greedy(self.iniciocell, cell, max_height, max_width, int_grid, int_ponderado_grid)
                    if alg != None:
                        if custo_g < custo_otimo:
                            custo_otimo = custo_g
                            custo_h_otimo = custo_h
                            self.caminho = alg
                            destino = cell
            case "A*":
                for cell in self.finalcell:
                    alg, custo_g, custo_h = buscaP.a_estrela(self.iniciocell, cell, max_height, max_width, int_grid, int_ponderado_grid)
                    if alg != None:
                        if custo_g < custo_otimo:
                            custo_otimo = custo_g
                            custo_h_otimo = custo_h
                            self.caminho = alg
            case "AIA*":
                for cell in self.finalcell:
                    alg, custo_g, custo_h = buscaP.aia_estrela(self.iniciocell,  cell, max_height, max_width, int_grid, int_ponderado_grid)

                    if alg != None:
                        if custo_g < custo_otimo:
                            custo_otimo = custo_g
                            custo_h_otimo = custo_h
                            self.caminho = alg
            case _:
                self.caminho = None

        # desenhar caminho no grid
        if self.caminho != None:
            self.desenharcaminho = True
        else:
            self.iniciocell = [-1, -1]
            self.finalcell = []
            self.desenharcaminho = False
            print("Não foi possivel achar um caminho.")
            print("\n")

        self.desenhar_grid()

        # informação do caminho feito
        if self.caminho != None:
            if self.Combo.get() in ["CUSTO UNIFORME", "GREEDY", "A*", "AIA*"]:
                if self.Combo.get() == "CUSTO UNIFORME":
                    print(f"Caminho encontrado com custo total: {custo_otimo}")
                    print("Caminho feito:")

                    for index, cam in enumerate(self.caminho):
                        print(str(index) + ": [" + str(cam[1]) + ", " + str(cam[0]) + "]")

                if self.Combo.get() == "GREEDY":
                    print(f"Heuristica final (h): {custo_h_otimo}")

                    print("Heurística de cada célula do caminho:")
                    for index, cam in enumerate(self.caminho):
                        h_val = buscaP.heuristica_manhattan(cam, destino)
                        print(f"{index}: [{cam[1]}, {cam[0]}] -> h = {h_val}")

                if self.Combo.get() == "A*":
                    print(f"Caminho encontrado com custo total: {custo_otimo}")
                    print(f"Heurística final(h): {custo_h_otimo}")
                    print("Heurística de cada célula do caminho:")
                    for index, cam in enumerate(self.caminho):
                        h_val = buscaP.heuristica_manhattan(cam, self.finalcell[0])
                        print(f"{index}: [{cam[1]}, {cam[0]}] -> h = {h_val}")

                if self.Combo.get() == "AIA*":
                    print(f"Caminho encontrado com custo total: {custo_otimo}")
                    print(f"Limite final (f): {custo_h_otimo}")
                    print("Heurística adaptada de cada célula do caminho:")

                    for index, cam in enumerate(self.caminho):
                        h_val = buscaP.heuristica_manhattan(cam, self.finalcell[0])
                        if hasattr(buscaP, "heuristicas_adaptadas"):
                            h_val = buscaP.heuristicas_adaptadas.get(tuple(cam), h_val)
                        print(f"{index}: [{cam[1]}, {cam[0]}] -> h = {h_val}")
            else:
                print("Caminho feito:")

                for index, cam in enumerate(self.caminho):
                    print(str(index) + ": [" + str(cam[0]) + ", " + str(cam[1]) + "]")

            print("\n")

    def desenhar_grid(self):
        for row_index, row in enumerate(grid):
            for column_index, cell in enumerate(row):
                x1 = (column_index * self.cell_size) + cell_size
                y1 = (row_index * self.cell_size) + cell_size
                x2 = (x1 + self.cell_size) + cell_size
                y2 = (y1 + self.cell_size) + cell_size

                # texto do x e y
                if row_index == 0:
                    self.canvas.create_text(x1 + self.cell_size / 2, y1 - self.cell_size / 2, text=column_index)

                if column_index == 0:
                    self.canvas.create_text(x1 - self.cell_size / 2, y1 + self.cell_size / 2, text=row_index)

                # criar células
                if self.desenhado == False:
                    if cell == str(0):
                        cell_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray", fill="lightgray")
                    elif cell == str(1):
                        cell_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray", fill="black")

                    self.cells[(row_index, column_index)] = cell_id
                    self.canvas.create_text(x1 + self.cell_size / 2, y1 + self.cell_size / 2, text=int_ponderado_grid[row_index][column_index])
                    
                # pintar células se ouver mudança
                else:
                    if cell == str(0):
                        if self.desenharcaminho == True:
                            if self.canvas.itemcget(self.cells[(row_index,column_index)], "fill") != "blue" and self.canvas.itemcget(self.cells[(row_index,column_index)], "fill") != "green":
                                self.canvas.itemconfig(self.cells[(row_index,column_index)], outline="gray", fill="lightgray")
                        else:
                            self.canvas.itemconfig(self.cells[(row_index,column_index)], outline="gray", fill="lightgray")
                    elif cell == str(1):
                        self.canvas.itemconfig(self.cells[(row_index,column_index)], outline="gray", fill="black")

                if self.desenharcaminho == True:
                    for elem in self.caminho:
                        if self.canvas.itemcget(self.cells[(elem[0], elem[1])], "fill") != "blue" and self.canvas.itemcget(self.cells[(elem[0], elem[1])], "fill") != "green":
                            self.canvas.itemconfig(self.cells[(elem[0], elem[1])], fill="darkgray")

        self.desenhado = True


    def cell_click(self, event):
        clicked_cell = None

        if self.escolhendoInicio == True:
            # determinar célula clicada
            items = self.canvas.find_overlapping(event.x, event.y, event.x+1, event.y+1)

            # pegar celula debaixo do texto
            for item in items:
                if self.canvas.type(item) != 'text':
                    clicked_cell = item

            if clicked_cell != None:
                # checar cell
                for (row, col), cell_id in self.cells.items():
                    if cell_id == clicked_cell:
                        current_color = self.canvas.itemcget(cell_id, "fill")
                        if current_color != "black" and current_color != "darkgray" and current_color != "green":
                            # retorna cores a cinza se outras ja estiverem selecionadas
                            for (r, c), cell_id_prov in self.cells.items():
                                if self.canvas.itemcget(cell_id_prov, "fill") == "blue":
                                    self.canvas.itemconfig(cell_id_prov, fill="lightgray")

                            # add inicio
                            if current_color == "lightgray":
                                self.iniciocell = [row, col]
                            else:
                                self.iniciocell = [-1, -1]

                            new_color = "blue" if current_color == "lightgray" else "lightgray"
                            self.canvas.itemconfig(cell_id, fill=new_color)
                            self.escolhendoInicio = False
                            self.inicio.config(text="Escolher a célula de inicio")
                        break

        if self.escolhendoFinal == True:
            # determinar célula clicada
            items = self.canvas.find_overlapping(event.x, event.y, event.x + 1, event.y + 1)

            # pegar celula debaixo do texto
            for item in items:
                if self.canvas.type(item) != 'text':
                    clicked_cell = item

            if clicked_cell != None:
                # checar cell
                for (row, col), cell_id in self.cells.items():
                    if cell_id == clicked_cell:
                        current_color = self.canvas.itemcget(cell_id, "fill")
                        if current_color != "black" and current_color != "darkgray" and current_color != "blue":

                            # add final
                            if current_color == "lightgray":
                                self.finalcell.append([row, col])
                            else:
                                self.finalcell.remove([row, col])

                            new_color = "green" if current_color == "lightgray" else "lightgray"
                            self.canvas.itemconfig(cell_id, fill=new_color)
                        break


# rodar tkinter
root = tk.Tk()

app = GridApp(root)
root.mainloop()