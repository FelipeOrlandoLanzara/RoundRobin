def readfile():
    processosLeitura = {}

# 1 ) Leitura de cada elemento do arquivo

    with open("entrada.txt", "r") as arquivo:
        linhas = arquivo.readlines()
        for idx, linha in enumerate(linhas, start=1):
            linha = linha.strip() #dividir linha por linha
           # Separar os dados por espaço e remover espaços em branco

           #list comprehension para pegar caracter por caracter
            partes = [parte.strip() for parte in linha.split(" ")]


# 2 ) Processo pode não apresentar IO
            if len(partes) >= 3:
                nome_processo = partes[0]
                tempo_chegada = int(partes[1])
                tempo_total = int(partes[2])
# 3) Quando processo possui IO verificar se há uma lista de interrupções de I/O
                fila = []
# 4) Verificar se tem tempo de chegada do IO

                if len(partes) == 4 and partes[3]:
                    numeros = partes[3].split(",")
                    for numero in numeros:
                        fila.append(int(numero))
                else:
                    fila.append(0)
# 5) Verificar se o arquivo foi escrito corretamente, caso contrario apontar o erro
                if len(partes) > 4:
                    print("Arquivo Invalido, Colocar dados de forma correta")
                    print("Console error: [ Line", idx,"] Value out of bounds:", " " .join(partes[4:]))
                    exit()
                # Armazenar os dados no dicionário
                processosLeitura[nome_processo] = [tempo_chegada, tempo_total, fila]

    # Retornar o dicionário ordenado pelo tempo de chegada
    return dict(sorted(processosLeitura.items(), key=lambda item: item[1][1]))


# Exemplo de uso
processos = readfile()
for processo, dados in processos.items():
    print(f"Processo: {processo}, Tempo Chegada: {dados[0]}, Tempo Total: {dados[1]}, I/O Interrupts: {list(dados[2])}")

print(processos)

# ENTRADA:
# NOME(PROCESSO) | TEMPO(CHEGADA)   | TEMPO(TOTAL)   | I/O INTERRUPÇÃO(CPU/PARCIAL) [FILA]
# ---------------|------------------|----------------|----------------------------------
# P1             | 9                | 10             | 2, 4, 6, 8
# ---------------|------------------|----------------|----------------------------------
# P2             | 10               | 4              | 5
# ---------------|------------------|----------------|----------------------------------
# P3             | 5                | 0              | 2
#----------------|------------------|----------------|----------------------------------
# P4             | 7                | 1              | 3, 6
#----------------|------------------|----------------|----------------------------------
# P5             | 2                | 17             |


def FilaProcessos(Fila,tempo_atual,processos):
    Fila_aux = Fila[:] #copia os elementos da fila

    if Fila_aux:
    #1) QUANDO NÂO HÀ NENHUM PROCESSO NA FILA
        for processo, dados in processos.items():
            # 1) Colocar na fila

            if(tempo_atual ==  dados[0]):   
                Fila_aux.append(processo)

            # 3) Atualizar Fila (processo em execução)
            
        print("Fila: " , Fila_aux)
        return Fila_aux
    else:
        #2) QUANDO HÀ PROCESSO NA FILA


        #2.1) Adicionar um novo processo
        for processo, dados in processos.items():
            # 1) Colocar na fila

            if(tempo_atual ==  dados[0]):   
                Fila_aux.append(processo)

                
        # 2.2) Tirar o processo da Fila
            if(dados[1] == 0):
                print("EVENTO TIRADO DA FILA ",processo)
                Fila_aux.pop(0)
            # 3) Atualizar Fila (processo em execução)
            

        print("Fila: " , Fila_aux)
        return Fila_aux



def Quantum(Fila, processos, processo_atual):
    Fila_aux = Fila[:]

    #Quando tiver quantum, trocar o processo na CPU e colocar no fim da fila de processos e colocar o 1o processo da fila de processo na cpu

    Fila_aux.append(processo_atual)
    Fila_aux.pop(0)
    return Fila_aux



# def verificar_IO(Fila, processos, processo_atual, contador):

#     return Fila_aux, contador, tempoquantum


def CPU (Fila,quantum,processos): #um novo processo entra na CPU

    if not Fila:  # Verifica se a fila está vazia
        print("A fila está vazia. Nenhum processo para executar.")


    Fila_aux = Fila[:] #copia os elementos da fila

    processo_atual = Fila_aux[0]

    for processo, dados in processos.items():
        if(processo_atual == processo):
            print("CPU:", processo_atual, "(", dados[1] ,")")
            dados[1]-=1
    
    return Fila_aux , processo_atual


def roudrobin(quantum):
    tempo_atual = 0
    tempo_quantum = quantum
    contador = 0
    Fila =[]
    processo_atual = ""
    print("***** COMEÇANDO O ROUND ROBIN *****")
    # Tempos
    #soma de todos
    final = False
    
    for i in range(12):
        print(f"************{tempo_atual}***************")
        if final: #acabou todos os processo da fila
            break
        #deve ser executado pelo menos 1 vez
        Fila = FilaProcessos(Fila,tempo_atual,processos)

        if(tempo_quantum == 0):
            print("Preempção do Qauntum")
            Fila = Quantum(Fila,processos,processo_atual)
            print("Fila após quantum:",i)
            print(Fila)
            contador = 0
            print("contador atualizado")
            tempo_quantum = quantum

        #VERIFICAR IO

        # Quando houver IO, troque o processo na CPU, coloque-o no final da fila e coloque o próximo processo na CPU
        for processo, dados in processos.items():
            if processo_atual == processo:
                # Verifica se a lista de IO não está vazia
                if dados[2]:  # Isso verifica se dados[2] tem elementos
                    primeiro_elemento = dados[2][0]  # Acessa o primeiro elemento
                    if contador == primeiro_elemento and contador != 0:
                        print("#EVENTO DE IO")
                        #print("FILA IO(ANTES)",dados[2])
                        dados[2].pop(0)  # Remove o primeiro elemento da fila de IO
                        #print("FILA IO(DEPOIS)",dados[2])
                        contador = 0
                        tempo_quantum = quantum
                        Fila = Quantum(Fila, processos, processo_atual)



        #END
        Fila, processo_atual = CPU(Fila,4,processos)
        

        #Mudar o processo
        contador += 1
        tempo_quantum -=1
        tempo_atual +=1

roudrobin(4)