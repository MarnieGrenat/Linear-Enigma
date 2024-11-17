import numpy as np

def decypher(texto_cifrado, texto_claro_parcial):
    n = len(texto_claro_parcial)
    if n % 2 != 0:
        raise ValueError("Sherlock.Decypher : O texto claro parcial deve ter um número par de caracteres.")

    matriz_claro = []
    matriz_cifrado = []

    for i in range(0, n, 2):
        par_claro = [transforma_letra_em_numero(c) for c in texto_claro_parcial[i:i+2]]
        par_cifrado = [transforma_letra_em_numero(c) for c in texto_cifrado[i:i+2]]
        matriz_claro.append(par_claro)
        matriz_cifrado.append(par_cifrado)

    matriz_claro = np.array(matriz_claro)
    matriz_cifrado = np.array(matriz_cifrado)

    print(f'Sherlock.Decypher : Matriz MSG={matriz_claro} : Matriz Cifrada={matriz_cifrado}')

    matriz_chave = encontrar_transposta_decodificadora(matriz_cifrado, matriz_claro)

    print(f'Sherlock.Decypher : Matriz Chave={matriz_chave}')

    texto_decifrado = ""
    for i in range(0, len(texto_cifrado), 2):
        par_cifrado = [transforma_letra_em_numero(c) for c in texto_cifrado[i:i+2]]
        par_decifrado = np.dot(matriz_chave, par_cifrado) % 26
        texto_decifrado += ''.join(transforma_numero_em_letra(num) for num in par_decifrado)

    return texto_decifrado

def encontrar_transposta_decodificadora(matriz_cifrada, matriz_clara):
    """
    Transforma a matriz cifrada na identidade e aplica as mesmas operações
    na matriz clara, resultando na transposta da matriz decodificadora.
    """
    mod = 26
    n = matriz_cifrada.shape[0]

    # Garante que são inteiros
    matriz_esquerda = matriz_cifrada.astype(int).copy()
    matriz_direita = matriz_clara.astype(int).copy()

    for i in range(n):
        # Inverso modular do elemento diagonal
        elem_diagonal = int(matriz_esquerda[i, i])
        if elem_diagonal == 0:
            raise ValueError("Elemento diagonal zero encontrado, não é possível calcular o inverso modular.")
        inverso_modular = pow(elem_diagonal, -1, mod)

        # Escala linha
        matriz_esquerda[i] = (matriz_esquerda[i] * inverso_modular) % mod
        matriz_direita[i] = (matriz_direita[i] * inverso_modular) % mod

        # Executa Gauss Jordan na coluna
        for j in range(n):
            if i != j:
                fator = matriz_esquerda[j, i]
                matriz_esquerda[j] = (matriz_esquerda[j] - fator * matriz_esquerda[i]) % mod
                matriz_direita[j] = (matriz_direita[j] - fator * matriz_direita[i]) % mod

    return matriz_direita.T

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

def decode(cypher : str, m : list, is_inverse : bool) -> str :
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

# Suporta apenas matrizes 2x2
def inverter(matriz):
    inversa = {
        1: 1, 3: 9, 5: 21, 7: 15, 9: 3, 11: 19, 15: 7,
        17: 23, 19: 11, 21: 5, 23: 17, 25: 25
    }
    try:
        # Determinante como inteiro
        det_A = int(round(np.linalg.det(matriz)))
        det_mod_26 = det_A % 26

        if det_mod_26 == 0 or det_mod_26 not in inversa:
            raise ValueError(f"Sherlock.Inverter : Determinante ({det_A}) não possui inverso modular no módulo 26.")

        # Cálculo da adjunta
        adj_A = np.array([[matriz[1, 1], -matriz[0, 1]],
                          [-matriz[1, 0], matriz[0, 0]]]) % 26

        # Inversa modular do determinante
        det_inv = inversa[det_mod_26]
        inv_A = (det_inv * adj_A) % 26
        return inv_A

    except np.linalg.LinAlgError:
        raise ValueError("Sherlock.Inverter : Erro ao calcular a matriz inversa.")

def transforma_letra_em_numero(letra : str) -> int:
    modulo26 = 'zabcdefghijklmnopqrstuvwxy'
    return modulo26.find(letra.lower())

def transforma_numero_em_letra(numero : int) -> str:
    modulo26 = 'zabcdefghijklmnopqrstuvwxy'
    return modulo26[int(numero) % 26]