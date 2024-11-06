
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

print("\nLeitura dos Processos\n")

processos = readfile()
for processo, dados in processos.items():
    print(f"Processo: {processo}, Tempo Chegada: {dados[0]}, Tempo Total: {dados[1]}, I/O Interrupts: {list(dados[2])}")

tempo_espera = {processo: 0 for processo in processos.keys()}




def FilaProcessos(Fila, tempo_atual, processos):
    Fila_aux = Fila[:]
    for processo, dados in processos.items():
        if tempo_atual == dados[0] and processo not in Fila_aux:
            #ADICIONAR NOVOS PROCESSOS
            print("#[evento] CHEGADA:", processo)
            saida.write(f"#[evento] CHEGADA: {processo}\n\n")
            Fila_aux.append(processo)
    
    #MOSTRAR FILA ATUAL
    print("Fila:", Fila_aux)
    saida.write(f"Fila: {Fila_aux}\n\n")

    return Fila_aux


def Fila_handler(Fila, processo_atual):
    #FAZER A FILA GIRAR
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

    #Percorrer toda o dicionario da fila de processos
    for processo, dados in processos.items():
        if processo_atual == processo:
            #Pegar o processo atual: referente ao dicionario
            if dados[1] == 0:
                #1) PROCESSO ACABOU MUDAR PARA O PROXIMO
                print("#[evento] ENCERRANDO ", processo_atual)
                saida.write(f"#[evento] ENCERRANDO {processo_atual}\n\n")
                io_atual.pop(processo_atual, None) #CONTROLADOR DA FILA DE IO
                processo_atual = None
                Fila_aux = Fila_handler(Fila_aux, processo_atual)
                processo_atual = Fila_aux[0] if Fila_aux else None
                tempo_quantum = quantum
    
                if processo_atual:

                    # IMPLICAÇÃO E SE 2 PROCESSOS SEGUIDOS SAIREM DA CPU ?
                    if processos[processo_atual][1] == 0 :
                        return CPU(Fila_aux, processos, io_atual, quantum, tempo_quantum)


        
                    print("CPU:", processo_atual, "(", processos[processo_atual][1], ")")
                    saida.write(f"CPU: {processo_atual} ({processos[processo_atual][1]})\n\n")
                    #ADICIONAR NO ARQUIVO
                    gantt_chart.append(processo_atual)
                    #IMPLICAÇAO 2 processos podem acabar ao mesmo tempo

                    
                    processos[processo_atual][1] -= 1
                return Fila_aux, processo_atual, io_atual, tempo_quantum

            print("CPU:", processo_atual, "(", dados[1], ")")
            saida.write(f"CPU: {processo_atual} ({dados[1]})\n\n")
            #ADICIONAR NO ARQUIVO
            gantt_chart.append(processo_atual)
            dados[1] -= 1

    return Fila_aux, processo_atual, io_atual , tempo_quantum



saida = open("saida.txt", "w")

def roudrobin(quantum):
    tempo_atual = 0
    tempo_quantum = quantum
    Fila = []
    processo_atual = ""
    preemp = False
    count = 0
    io_atual = {processo: 0 for processo in processos.keys()}
    control = None
    print()
    print("*********************************")
    #ADICIONAR NO ARQUIVO
    saida.write("*********************************\n")
    print("*****ESCALONADOR ROUND ROBIN*****")
    saida.write("*****ESCALONADOR ROUND ROBIN*****\n")
    #ADICIONAR NO ARQUIVO
    

    # Não houve uma tratativa para inicio em dummy
    # O código não supor dummy

    while True:

        print(f"********** TEMPO {tempo_atual} **************")
        saida.write(f"********** TEMPO {tempo_atual} **************\n")
        Fila = FilaProcessos(Fila, tempo_atual, processos)

        # Verifica a preempção do quantum
        if tempo_quantum == 0:
            print("#[evento] PREEMÇÃO QUANTUM")
            saida.write("#[evento] PREEMÇÃO QUANTUM\n")
            #ADICIONAR NO ARQUIVO
            Fila = Fila_handler(Fila, processo_atual)
            tempo_quantum = quantum  # Reset do quantum após preempção
            preemp = True
        #PROCESSO PODE OCORRER IO OU QUANTUM NUNCA OS 2 SIMULTANEAMENTE

        if preemp != True:
            # Verificação de evento de I/O
            for processo, dados in processos.items():
                
                if processo_atual == processo:  
                    if dados[2]:  # Verifica se há interrupções de I/O
                        primeiro_elemento = dados[2][0]
                        if  io_atual[processo_atual] == primeiro_elemento and  io_atual[processo_atual] != 0:
                            print("#[evento] IO")
                            saida.write("#[evento] IO\n\n")
                            #ADICIONAR NO ARQUIVO
                            dados[2].pop(0)  # Remove o evento de I/O
                            tempo_quantum = quantum  # Reset do quantum após I/O
                            Fila = Fila_handler(Fila, processo_atual)

        # Atualiza o processo atual na CPU
        Fila, processo_atual, io_atual, tempo_quantum = CPU(Fila, processos, io_atual, quantum,tempo_quantum)
        print("Fila (Professor):", Fila[1:])
        saida.write(f"Fila (Professor): {Fila[1:]}\n")

        #ADICIONAR NO ARQUIVO

        for processo in Fila[1:]:
            if processo in tempo_espera:
                tempo_espera[processo] += 1



        tempo_quantum -= 1
        tempo_atual += 1
        count+=1
        preemp = False
        if processo_atual:
            io_atual[processo_atual] += 1


        if not io_atual:
            break
        if count >40:
            print("Parada forçada!")
            break


roudrobin(4)    


print("-----------------------------------")
saida.write("-----------------------------------\n")
print("------- Encerrando simulacao ------\n")
saida.write("------- Encerrando simulacao ------")
print("-----------------------------------")
saida.write("-----------------------------------\n")


print("\nTempo de espera:\n")

print(tempo_espera)

print("Soma:", sum(tempo_espera.values()))

print("Media:", sum(tempo_espera.values()) / len(tempo_espera) if tempo_espera else 0)



saida.close()
#SALVAR /FECHARO ARQUIVO 

#EXTRA 

#Fazer uma apresentação de resultados de forma gráfica (pode ser no terminal) e em tempo
#real enquanto o algoritmo é executado. Sugestão: coloque um atraso (1 seg.) entre cada
#tempo. Não basta gerar uma imagem final da execução. Tem que ser gerado em tempo real,
#ou seja, enquanto executa vai mostrando o gráfico de gantt sendo feito.


import time

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


print("\nFinalizado!\n")


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
