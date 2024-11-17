import numpy as np

import numpy as np
import math

def break_code(cypher: str, partial_decoded: str) -> str:
    """
    Decodifica uma mensagem cifrada pela cifra de Hill usando uma parte da mensagem já decodificada.
    """

    # Converte as mensagens em vetores numéricos
    cypher_numbers = [transforma_letra_em_numero(c) for c in cypher]
    decoded_numbers = [transforma_letra_em_numero(c) for c in partial_decoded]

    # Construir matriz ampliada (2x2 para pares)
    matriz_cypher = np.array(cypher_numbers[:4]).reshape(2, 2)
    matriz_decoded = np.array(decoded_numbers[:4]).reshape(2, 2)

    # Determinar a matriz de decodificação
    matriz_cypher_inv = inverter_modular(matriz_cypher)
    matriz_decodificadora = np.dot(matriz_decoded, matriz_cypher_inv) % 26

    # Aplicar a matriz de decodificação à cifra completa
    decoded_message = ""
    for i in range(0, len(cypher_numbers), 2):
        bloco = np.array(cypher_numbers[i:i+2])
        decoded_bloco = np.dot(matriz_decodificadora, bloco) % 26
        decoded_message += "".join(transforma_numero_em_letra(n) for n in decoded_bloco)

    return decoded_message

def code(message : str, m : list, is_inverse : bool) -> str :
    # Preparação
    print(f"Sherlock.Code : Mensagem Recebida={message} : Tamanho : {len(message)} : Matriz_Inversa={is_inverse}")
    matriz_cifra = np.array(m)
    mensagem_cifrada = ''

    if is_inverse:
        matriz_cifra = inverter(matriz_cifra)

    # Operações
    lista_de_vetores = transforma_texto_em_lista_de_vetores(message, matriz_cifra.shape[1])

    for vetor in lista_de_vetores:
        # Multiplica cada vetor pela matriz\ de cifra
        vetor_cifra = np.dot(matriz_cifra, vetor)
        #
        for elemento in vetor_cifra:
            mensagem_cifrada += transforma_numero_em_letra(elemento)

    return mensagem_cifrada.upper()

def decode (cypher : str, m : list, is_inverse : bool) -> str :
    # Preparação
    print(f"Sherlock.Decode : Mensagem Cifrada Recebida={cypher} : Tamanho : {len(cypher)} : Matriz_Inversa={is_inverse}")
    matriz_cifra = np.array(m)

    mensagem_descifrada = ''

    if not is_inverse:
        matriz_cifra = inverter(matriz_cifra)

    # Operações
    lista_de_vetores = transforma_texto_em_lista_de_vetores(cypher, matriz_cifra.shape[1])

    for vetor in lista_de_vetores:
        # Multiplica cada vetor pela matriz\ de cifra
        vetor_cifra = np.dot(matriz_cifra, vetor)
        #
        for elemento in vetor_cifra:
            mensagem_descifrada += transforma_numero_em_letra(elemento)

    return mensagem_descifrada.upper()

def transforma_texto_em_lista_de_vetores(texto : str, tam_vetor : int) -> list:
    indice = 0
    lista_de_vetores = []

    while indice < len(texto):
        vetor = []

        # Constrói um vetor com mesmo número de elementos que a linha da cifra contém
        for _ in range(tam_vetor):
            if indice < len(texto):
                char = transforma_letra_em_numero(texto[indice])

                #ignora caracteres não mapeados em 'modulo26', como espaços e caracteres especiais
                while char == -1:
                    indice += 1
                    char = transforma_letra_em_numero(texto[indice])
                vetor.append(char)
                indice += 1
            else:
                # Preenche mais um com valor repetido
                vetor.append(vetor[-1])
        vetor = np.array(vetor)
        lista_de_vetores.append(vetor)
    return lista_de_vetores

def transforma_letra_em_numero(letra : str) -> int:
    modulo26 = 'zabcdefghijklmnopqrstuvwxy'
    return modulo26.find(letra.lower())

def transforma_numero_em_letra(numero : int) -> str:
    modulo26 = 'zabcdefghijklmnopqrstuvwxy'
    return modulo26[int(numero) % 26]

# Suporta apenas matrizes 2x2
def inverter(matriz):
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
    try:
        # Determinante como inteiro
        det_A = int(round(np.linalg.det(matriz)))

        if det_A == 0:
            print(f"Sherlock.Inverter : A matriz não tem inversa (determinante é zero) : Matriz={matriz}")
            return matriz

        # Verificar se o determinante tem inversa modular
        det_mod_26 = det_A % 26
        if det_mod_26 not in inversa:
            print(f"Sherlock.Inverter : Determinante não possui inversa modular : Determinante={det_A}")
            return matriz

        # Cálculo da adjunta
        adj_A = np.array([[matriz[1, 1], -matriz[0, 1]],
                          [-matriz[1, 0], matriz[0, 0]]])

        # Inversa modular do determinante
        det_inv = inversa[det_mod_26]

        # Multiplicação pelo inverso modular
        inv_A = (det_inv * adj_A) % 26

        print(f"Sherlock.Inverter : matriz inversa com sucesso : Matriz_Inversa={inv_A}")
        return inv_A

    except np.linalg.LinAlgError:
        print("A matriz não tem inversa (determinante é zero).")
    return matriz

def inverter_modular(matriz, mod=26):
    # Determinante
    det = int(round(np.linalg.det(matriz)))
    det_mod = det % mod

    # Verificar se o determinante é invertível no módulo
    if math.gcd(det_mod, mod) != 1:
        raise ValueError(f"Determinante ({det_mod}) não possui inverso modular no módulo {mod}.")

    # Inverso modular do determinante
    det_inv = pow(det_mod, -1, mod)

    # Cálculo da adjunta da matriz
    adj = np.array([[matriz[1, 1], -matriz[0, 1]],
                    [-matriz[1, 0], matriz[0, 0]]]) % mod

    # Inversa modular
    inv = (det_inv * adj) % mod
    return inv