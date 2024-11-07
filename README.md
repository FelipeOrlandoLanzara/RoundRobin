# Trabalho de Sistemas Operacionais

### Round Robin


###  - Instruções de como rodar:

1) O Código em si possui dependencia para as bibliotecas **time** (nativa, não requer instalação) e **matplotlib**.

Para instalar matplotlib ultilizar


```bash
pip install matplotlib
```

2) Após instalar as dependencias é necessário criar um arquivo chamado **entrada.txt** no mesmo local onde está o código gerado, contendo as entradas ultilizadas no Round Robin.

**Nota:** Inserir as informações em cada linha no formato, o - representara um espaço NOME_PROCESSO-TEMPO_CHEGADA-TEMPO_TOTAL-I/Os.

```python
#Exemplo de como será lido a entrada baseado no exemplo dado
# ENTRADA:
# NOME(PROCESSO) | TEMPO(CHEGADA)   | TEMPO TOTAL    | I/O 
# ---------------|------------------|----------------|----------------------
# P1             | 9                | 10             | 2, 4, 6, 8
# ---------------|------------------|----------------|----------------------
# P2             | 10               | 4              | 5
# ---------------|------------------|----------------|----------------------
# P3             | 5                | 0              | 2
#----------------|------------------|----------------|----------------------
# P4             | 7                | 1              | 3, 6
#----------------|------------------|----------------|----------------------
# P5             | 2                | 17             |
```


3) Após a criação do arquivo entrada.txt e preenchimento do mesmo basta rodar o código chamado **Final.py**


4) O código será rodado e no terminal aparecerá uma simulação em tempo real e depois um gráfico no matplotlib em outra aba mostrando o diagrama de Gantt





### Requisitos a serem cumpridos:

1) O escalonador deve contemplar o funcionamento usual do algoritmo e também deve possuir
a funcionalidade de haver operação de I/O que cada processo possa solicitar.  Quando o processo necessitar uma operação de I/O deve ser retirado de execução na CPU

2) O escalonador deve considerar o quantum de tempo que um processo pode utilizar a CPU

3) Todo processo que for retirado da CPU pelo escalonador, seja porque o quantum expirou
ou por necessidade de uma operação de I/O, deve ser colocado no final da Fila de Pronto

4) Caso ocorra de um novo processo chegar no mesmo instante em que um processo que
estava em execução foi retirado da CPU para a fila de espera, o novo processo terá prioridade em
relação ao processo em execução para ir para a fila de espera

5) O simulador deve ter como entrada as informações de cada processo como PID, tempo de
chegada, duração, e caso tenha operação de I/O, deve mostrar quando elas devem ser executadas
(em relação ao seu tempo de execução). O tempo do quantum também deve ser descrito no início
da simulação.

6)  Após a leitura de dados, o simulador deve apresentar em um arquivo separado o resultado de
execução dos processos em forma de um diagrama de Gantt, calculando o tempo de espera de
cada processo e o tempo de espera médio.


7) A saída de dados deve ser realizada imprimindo o resultado em um arquivo de saída (saida.txt).

8) Adicional escolhido: Fazer uma apresentação de resultados de forma gráfica (pode ser no terminal) e em tempo real enquanto o algoritmo é executado.

###
