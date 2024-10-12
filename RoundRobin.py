class Processo:
    def __init__(self, nome, chegada, surto, io, tempo, estado): # cria a classe de processos
        self.nome = nome
        self.chegada = chegada
        self.surto = surto
        self.io = io
        self.tempo = tempo
        self.estado = estado
        
    def __repr__(self): # serve para poder printar 'processos' sem ser a representacao padrao
        return f'Processo(nome={self.nome}, chegada={self.chegada}, surto={self.surto}, io={self.io}, tempo={self.tempo})\n'
        
# 1- nome processo
# 2- instante de chegada
# 3- duração processo
# 4- I/O caso haja

# criacao de variaveis padroes
total_surto = 0
qtde_processos = 0
tempo_atual = 0 # em qual tempo está
matriz = [] # contem a entrada
processos = [] # tem todos os objetos de processos
fila = [] # processos que estao na fila

# leitura do arquivo
with open('entrada.txt', 'r') as file:
    linhas = file.readlines()
    for linha in linhas:
        linha = linha.strip().split()
        qtde_processos += 1 # saber a quantidade de processos
        total_surto += int(linha[2]) # saber o total de surto
        matriz.append(linha) # jogar em uma variavel para poder analisar melhor
        
# criacao das instanciais dos objetos        
for conteudo in matriz:
    processo = Processo(conteudo[0], conteudo[1], conteudo[2], conteudo[3], 0, False)
    processos.append(processo)
        
# criar o print inicial
def print_inicial():
    saida = "*" * 35 + '\n' + "*" * 5 + " ESCALONADOR ROUND ROBIN " + "*" * 5 + "\n" + "-" * 35 + "\n" + "-" * 7 + " INICIANDO SIMULACAO " + "-" * 7 + "\n" + "-" * 35
    print(saida)

def print_tempo(tempo):
    saida = "*" * 12 + " TEMPO " + str(tempo) + " " + "*" * 12
    print(saida)

print_inicial()
print_tempo(1)

for p in processos:
    pass
        
        
        
        
        
#print(total_surto)
#print(qtde_processos)
#print(processos)
#print(matriz)
print(processos)
