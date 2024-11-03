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


def CPU(Fila, processos, contador,quantum,tempo_quantum):
    if not Fila:
        print("A fila está vazia. Nenhum processo para executar.")
        return Fila, None, contador

    Fila_aux = Fila[:]
    processo_atual = Fila_aux[0]

    for processo, dados in processos.items():
        if processo_atual == processo:
            if dados[1] == 0:
                print("#[evento] ENCERRANDO ", processo_atual)
                processo_atual = None
                Fila_aux = Fila_handler(Fila_aux, processo_atual)
                processo_atual = Fila_aux[0] if Fila_aux else None
                contador = 0
                tempo_quantum = quantum
                if processo_atual:
                    print("Novo processo na CPU:", processo_atual, "(", processos[processo_atual][1], ")")
                    print("Fila ATUAL =", Fila_aux)
                    print("CPU:", processo_atual, "(", processos[processo_atual][1], ")")
                    processos[processo_atual][1] -= 1
                return Fila_aux, processo_atual, contador, tempo_quantum

            print("CPU:", processo_atual, "(", dados[1], ")")
            dados[1] -= 1

    return Fila_aux, processo_atual, contador , tempo_quantum


def roudrobin(quantum):
    tempo_atual = 0
    tempo_quantum = quantum
    contador = 0
    Fila = []
    processo_atual = ""
    print("***********************************")
    print("***** ESCALONADOR ROUND ROBIN *****")

    for i in range(34):
        print(f"********** TEMPO {tempo_atual} **************")

        Fila = FilaProcessos(Fila, tempo_atual, processos)

        # Verifica a preempção do quantum
        if tempo_quantum == 0:
            print("Preempção do Quantum")
            Fila = Fila_handler(Fila, processo_atual)
            contador = 0
            tempo_quantum = quantum  # Reset do quantum após preempção

        # Verificação de evento de I/O
        for processo, dados in processos.items():
            if processo_atual == processo and dados[2]:  # Verifica se há interrupções de I/O
                primeiro_elemento = dados[2][0]
                if contador == primeiro_elemento and contador != 0:
                    print("#EVENTO DE IO")
                    dados[2].pop(0)  # Remove o evento de I/O
                    contador = 0
                    tempo_quantum = quantum  # Reset do quantum após I/O
                    Fila = Fila_handler(Fila, processo_atual)

        # Atualiza o processo atual na CPU
        Fila, processo_atual, contador, tempo_quantum = CPU(Fila, processos, contador, quantum,tempo_quantum)
        contador += 1
        tempo_quantum -= 1
        tempo_atual += 1


# Executa o round-robin
processos = readfile()
roudrobin(4)
