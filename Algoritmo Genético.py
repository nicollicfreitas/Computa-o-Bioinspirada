import random
import time

start_time = time.time()

n_cromossomos = 80
peso_maximo = 75
n_geracoes = 10
pesos_valores = [[2,4],[30,10],[20,31],[18,20],[8,300],[2,30],[12,23],[6,570],[25,27],[3,6]]
n_itens = len(pesos_valores)
taxa_mutacao = 0.1

# Listas para armazenar informações sobre as gerações e os melhores valores 
geracoes = []
melhores_valores = []

def fitness(cromossomo):
    peso_total, valor_total = 0,0
    for indice, _ in enumerate(cromossomo):
        peso_total += (cromossomo[indice] * pesos_valores[indice][0])
        valor_total += (cromossomo[indice] * pesos_valores[indice][1])

        if peso_total > peso_maximo:
            return 0
    return valor_total

def calcula_probabilidades(populacao):
    v_fitness = [fitness(cromossomo) for cromossomo in populacao]
    soma_total_fit = sum(v_fitness)
    probabilidades = [v_fit / soma_total_fit for v_fit in v_fitness]

    return probabilidades

#faz o sorteios dos cromossomos pais, através do método da roleta
def sorteio(populacao, probabilidades):
    total_prob = sum(probabilidades) 
    #junta a lista probabilidade com a lista populacao
    prob_cromossomos = list(zip(probabilidades, populacao))
    #caso só tenha sobrado invididuos com probabilidade igual 0, será sorteado sem considerar a probabilidade
    if(total_prob == 0):
        cromossomo = random.choice(prob_cromossomos)
    #função random.choices realiza o sorteio baseado nas probabilidades
    else:
        cromossomo = random.choices(prob_cromossomos, weights=[w/total_prob for w in probabilidades], k=1)[0]

    return cromossomo

#cria a população, com valores 0 ou 1
populacao = [[random.choice([0, 1]) for _ in range(n_itens)] for _ in range(n_cromossomos)]

#realiza a seleção, o crossover e a mutação 
for geracao in range(n_geracoes):
    ponto_corte = 0
    nova_populacao = []

    #Geração de novos indivíduos via seleção por roleta
    roleta = list(populacao)
    probabilidades = calcula_probabilidades(populacao)   

    for _ in range(1, n_cromossomos, 2):
        #seleção dos individuos pais, com base nos valores fitness (quanto maior o valor, maior a probabilidade)
        pai = sorteio(roleta, probabilidades)
        roleta.remove(pai[1])
        probabilidades.remove(pai[0])
        mae = sorteio(roleta, probabilidades)
        roleta.remove(mae[1])
        probabilidades.remove(mae[0])

        #recombinação em 1 ponto
        ponto_corte = random.randint(1, n_itens - 1)
        filho = pai[1][:ponto_corte] + mae[1][ponto_corte:]
        
        for i in range(len(filho)):
            if random.random() < taxa_mutacao:
                filho[i] = 1 - filho[i]

        nova_populacao.append(filho) #para geração dos graficos
        populacao.append(filho)

    #para geração dos gráficos
    geracoes.append(geracao)
    melhores_valores.append(fitness(max(nova_populacao, key=lambda cromossomo: fitness(cromossomo)))) #melhor valor de cada geração

    v_fitness = [fitness(cromossomo) for cromossomo in populacao]
    populacao.sort(key=lambda cromossomo: fitness(cromossomo), reverse=True) #ordena a população de forma descrecente, ou seja, os mais aptos ficarão nas primeiras posições
    populacao = populacao[:n_cromossomos] #seleciona os N_cromossomos da lista ordenada

melhor_individuo = max(populacao, key=lambda cromossomo: fitness(cromossomo))
melhor_valor = fitness(melhor_individuo)
print(melhor_individuo, "= ",melhor_valor)

execution_time = time.time() - start_time
print(f"Execution time: {execution_time} seconds")

# Gráfico de Evolução dos Valores
plt.figure()
plt.plot(geracoes, melhores_valores, marker='o')
plt.xlabel('Geração')
plt.ylabel('Melhor Valor')
plt.title('Evolução dos Valores')
plt.grid(True)
plt.show()

import matplotlib.pyplot as plt

# Calcula a taxa de convergência
taxa_convergencia = []
for geracao in range(1, len(melhores_valores)):
    if melhores_valores[geracao] == melhores_valores[geracao - 1]:
        taxa_convergencia.append(1)
    else:
        taxa_convergencia.append(0)

# Plot da taxa de convergência
plt.plot(range(1, len(melhores_valores)), taxa_convergencia, marker='o')
plt.xlabel('Geração')
plt.ylabel('Taxa de Convergência')
plt.title('Taxa de Convergência do Algoritmo Genético')
plt.grid(True)
plt.show()
