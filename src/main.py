import watson
import sherlock


def main():
    '''
    watson.open_window abre uma aba para receber input dos usuários, recebendo duas funções para
    cifrar (sherlock.code) e descifrar (sherlock.decode) valores.
    '''
    watson.open_window(sherlock.code, sherlock.decode, sherlock.decypher)

if __name__ == '__main__':
    main()