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
                    processos[processo_atual][1] -= 1
                return Fila_aux, processo_atual, io_atual, tempo_quantum

            print("CPU:", processo_atual, "(", dados[1], ")")
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
                    #dados[2][1:] = [io - 1 for io in dados[2][1:]]

                    print("Contador (IO):",  io_atual[processo_atual])
                    print("Primeiro elemento:", primeiro_elemento)
                    #dados[2][0]-=1
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
        #incrementar 1 em cada contador de IO
        if processo_atual:
            io_atual[processo_atual] += 1

# Executa o round-robin

roudrobin(4)

