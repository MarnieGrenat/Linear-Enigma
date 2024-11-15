import numpy as np

modulo26 = 'zabcdefghijklmnopqrstuvwxy'

inversa = {
    1 : 1,
    3 : 9,
    5 : 21,
    7 : 15,
    9 : 3,
    11 : 19,
    15 : 7,
    17 : 23,
    19 : 11,
    21 : 5,
    23 : 17,
    25 : 25
}

def code(message : str, m : list, is_inverse : bool) -> str :
    indice = 0
    matriz_cifra = np.array(m)

    # Número de colunas da matriz de cifra
    num_colunas = matriz_cifra.shape[1]
    mensagem_cifrada = ''

    print(f"Sherlock.Code : Mensagem Recebida={message} : Tamanho : {len(message)} : Matriz_Inversa={is_inverse}")
    if is_inverse:
        matriz_cifra = inverter(matriz_cifra)

    while indice < len(message):
        vetor = []

        # Constrói um vetor com mesmo número de elementos que a linha da cifra contém
        for _ in range(num_colunas):
            if indice < len(message):
                char = modulo26.find(message.lower()[indice])

                #ignora caracteres não mapeados em 'modulo26', como espaços e caracteres especiais
                while char == -1:
                    indice += 1
                    char = modulo26.find(message.lower()[indice])
                vetor.append(char)
                indice += 1
            else:
                # Preenche mais um com valor repetido
                vetor.append(vetor[-1])
        vetor = np.array(vetor)

        print(vetor)

        # Multiplica o vetor pela matriz de cifra
        vetor_cifra = np.dot(matriz_cifra, vetor)

        for elemento in vetor_cifra:
            mensagem_cifrada += modulo26[int(elemento) % 26]

    return mensagem_cifrada.upper()

def decode (cypher : str, m : list, is_inverse : bool) -> str :
    modulo26 = 'zabcdefghijklmnopqrstuvwxy'

    return ''


def inverter(matriz):
    # TODO
    return matriz
    # matriz_inversa = np.linalg.det()
    # nova_matriz = [[]]
    # for i in range(len(matriz)):
    #     for j in range(len(matriz[0])):
    #         nova_matriz[i, j] = inversa[matriz[i, j]]
    # return nova_matriz