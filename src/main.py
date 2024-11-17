import watson
import sherlock


def main():
    '''
    watson.open_window abre uma aba para receber input dos usuários, recebendo duas funções para
    cifrar (sherlock.code) e descifrar (sherlock.decode) valores.
    '''
    watson.open_window(sherlock.code, sherlock.decode, sherlock.break_code)

if __name__ == '__main__':
    #main()
        # Exemplo de uso
    cypher_text = "IDCEMJVIXZ"
    partial_decoded_text = "AMOD"
    decoded_message = sherlock.break_code(cypher_text, partial_decoded_text)
    print("Mensagem Decodificada:")
    print(decoded_message)

