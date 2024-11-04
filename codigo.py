
import time

#Adicional
gantt_chart = []

def readfile():
    processosLeitura = {}

    with open("entrada.txt", "r") as arquivo:
        linhas = arquivo.readlines()
        for idx, linha in enumerate(linhas, start=1):
            linha = linha.strip()
            partes = [parte.strip() for parte in linha.split(" ")]

            if len(partes) >= 3:
                nome_processo = partes[0]
                tempo_chegada = int(partes[1])
                tempo_total = int(partes[2])
                fila = []

                if len(partes) == 4 and partes[3]:
                    numeros = partes[3].split(",")
                    for numero in numeros:
                        fila.append(int(numero))
                else:
                    fila.append(0)

                if len(partes) > 4:
                    print("Arquivo Invalido, Colocar dados de forma correta")
                    print("Console error: [ Line", idx, "] Value out of bounds:", " ".join(partes[4:]))
                    exit()
                processosLeitura[nome_processo] = [tempo_chegada, tempo_total, fila]

    return dict(sorted(processosLeitura.items(), key=lambda item: item[1][0]))


processos = readfile()
for processo, dados in processos.items():
    print(f"Processo: {processo}, Tempo Chegada: {dados[0]}, Tempo Total: {dados[1]}, I/O Interrupts: {list(dados[2])}")


def FilaProcessos(Fila, tempo_atual, processos):
    Fila_aux = Fila[:]
    for processo, dados in processos.items():
        if tempo_atual == dados[0] and processo not in Fila_aux:
            Fila_aux.append(processo)
    
    print("Fila:", Fila_aux)
    return Fila_aux


def Fila_handler(Fila, processo_atual):

    Fila_aux = Fila[:]
    if processo_atual:
        Fila_aux.append(processo_atual)
    Fila_aux.pop(0)
    return Fila_aux


def CPU(Fila, processos, io_atual,quantum,tempo_quantum):
    if not Fila:
        print("A fila está vazia. Nenhum processo para executar.")
        return Fila, None, io_atual

    Fila_aux = Fila[:]
    processo_atual = Fila_aux[0]

    for processo, dados in processos.items():
        if processo_atual == processo:
            if dados[1] == 0:
                print("#[evento] ENCERRANDO ", processo_atual)
                io_atual.pop(processo_atual, None) # caso a chave não exista não faz nada (2o argumento)
                processo_atual = None
                Fila_aux = Fila_handler(Fila_aux, processo_atual)
                processo_atual = Fila_aux[0] if Fila_aux else None
                tempo_quantum = quantum
                if processo_atual:
                    print("#[evento] CHEGADA:", processo_atual, "(", processos[processo_atual][1], ")")
                    print("Fila ATUAL =", Fila_aux)
                    print("CPU:", processo_atual, "(", processos[processo_atual][1], ")")
                    gantt_chart.append(processo_atual)
                    processos[processo_atual][1] -= 1
                return Fila_aux, processo_atual, io_atual, tempo_quantum

            print("CPU:", processo_atual, "(", dados[1], ")")
            gantt_chart.append(processo_atual)
            dados[1] -= 1

    return Fila_aux, processo_atual, io_atual , tempo_quantum


def roudrobin(quantum):
    tempo_atual = 0
    tempo_quantum = quantum
    Fila = []
    processo_atual = ""
    
    io_atual = {processo: 0 for processo in processos.keys()}
    print("dicionario de IO:", io_atual)
    print("***********************************")
    print("***** ESCALONADOR ROUND ROBIN *****")
    # Lista para armazenar os tempos de execução para o gráfico de Gantt
    

#ADICIONAL VERIFICAR SE O PROCESSO VAI ENTRAR NA FILA ANTES DO SEU RESPECTIVO TEMPO NO QUAL O PROCESSO ENTRA OCORRER


#INICIALIZAR A FILA DE PROCESSOS PELA PRIMEIRA VEZ
    for processo, dados in processos.items():
        if tempo_atual == dados[0] and processo not in Fila:
            Fila.append(processo)


    while not Fila:
        print(f"********** TEMPO {tempo_atual} **************")  
        tempo_atual+=1
        print("AQUARDANDO PROCESSOS NA FILA")
        Fila = FilaProcessos(Fila, tempo_atual, processos)
        if Fila:
            print("Iniciando....")


    while io_atual:

        print(f"********** TEMPO {tempo_atual} **************")

        Fila = FilaProcessos(Fila, tempo_atual, processos)

        # Verifica a preempção do quantum
        if tempo_quantum == 0:
            print("#[evento] PREEMÇÃO QUANTUM")
            Fila = Fila_handler(Fila, processo_atual)
            tempo_quantum = quantum  # Reset do quantum após preempção

        # Verificação de evento de I/O
        for processo, dados in processos.items():
            
            if processo_atual == processo:  
                if dados[2]:  # Verifica se há interrupções de I/O
                    primeiro_elemento = dados[2][0]
                    print("Contador (IO):",  io_atual[processo_atual])
                    print("Primeiro elemento:", primeiro_elemento)
                    if  io_atual[processo_atual] == primeiro_elemento and  io_atual[processo_atual] != 0:
                        print("#[evento] IO")
                        dados[2].pop(0)  # Remove o evento de I/O
                        tempo_quantum = quantum  # Reset do quantum após I/O
                        Fila = Fila_handler(Fila, processo_atual)

        # Atualiza o processo atual na CPU
        Fila, processo_atual, io_atual, tempo_quantum = CPU(Fila, processos, io_atual, quantum,tempo_quantum)
        print("Fila (Professor):", Fila[1:])
        tempo_quantum -= 1
        tempo_atual += 1
        #Incrementar 1 em cada contador de IO
        if processo_atual:
            io_atual[processo_atual] += 1

# Executa o round-robin


print("-----------------------------------")
print("------- Encerrando simulacao ------")
print("-----------------------------------")


roudrobin(4)

#EXTRA 

#Fazer uma apresentação de resultados de forma gráfica (pode ser no terminal) e em tempo
#real enquanto o algoritmo é executado. Sugestão: coloque um atraso (1 seg.) entre cada
#tempo. Não basta gerar uma imagem final da execução. Tem que ser gerado em tempo real,
#ou seja, enquanto executa vai mostrando o gráfico de gantt sendo feito.


#DEBUG PURPOSE PRINT
# print("\nGráfico de Gantt:")
# print(" | ".join(gantt_chart))
# print("-----------------------------------")



gantt_chart_dict = {}


processos = sorted(set(gantt_chart))  # Mantém a ordem dos processos única e ordenada
gantt_chart_dict = {processo: [] for processo in processos}

# Define o comprimento do gráfico de Gantt
gantt_length = len(gantt_chart)

# Preenche o gráfico de Gantt coluna por coluna, simulando tempo real
for i in range(gantt_length):
    print("\nGráfico de Gantt:")

    # Atualiza cada processo no instante de tempo i
    print("Tempo :",i)
    for processo in processos:
        # Se o processo atual corresponde ao instante de tempo, marca com "x", caso contrário, "-"
        if gantt_chart[i] == processo:
            gantt_chart_dict[processo].append("x")
        else:
            gantt_chart_dict[processo].append("-")

        # Imprime a linha atualizada para o processo

        print(f"{processo}: {''.join(gantt_chart_dict[processo])}")

    # Delay de 1 segundo entre cada coluna para simulação de tempo real
    time.sleep(1)


print("Finalizado!")


##CALCULAR TEMPO DE ESPERA E TEMPO DE ESPERA MEDIO 


##CRIAR GRÁFICO SEPARADO


import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

processos = sorted(set(gantt_chart))  # Processos únicos
cores = {processo: plt.cm.tab20(i / len(processos)) for i, processo in enumerate(processos)}

# Configura o gráfico
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_title("Diagrama de Gantt dos Processos")
ax.set_xlabel("Tempo")
ax.set_ylabel("Processos")

# Mapeia os processos para linhas no gráfico
y_pos = {processo: i for i, processo in enumerate(processos)}

# Adiciona os blocos de tempo para cada processo no gráfico de Gantt
for time, processo in enumerate(gantt_chart):
    ax.broken_barh([(time, 1)], (y_pos[processo] - 0.4, 0.8), facecolors=cores[processo])

# Adiciona as labels e personaliza o gráfico
ax.set_yticks([y_pos[processo] for processo in processos])
ax.set_yticklabels(processos)
ax.set_xticks(range(0, len(gantt_chart) + 1, 1))
ax.grid(True, axis='x', linestyle='--', alpha=0.7)

# Adiciona legenda
handles = [mpatches.Patch(color=cores[proc], label=proc) for proc in processos]
ax.legend(handles=handles, title="Processos")

plt.show()



