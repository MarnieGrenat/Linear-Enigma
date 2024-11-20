from tkinter import *
from tkinter import ttk
from tkinter import messagebox


def open_window(code, decode, break_code):
    root = Tk()
    root.title("Linear Enigma")

    # Estilização
    root.maxsize(width=380, height=380)
    root.minsize(width=380, height=380)
    root.iconbitmap(r"assets\icon.ico")
    root.configure(bg="#1E1E2E")
    style = ttk.Style(root)
    style.configure("TFrame", background="#1E1E2E")
    style.configure("TLabel", font=("Helvetica", 12), background="#1E1E2E", foreground="#FFFFFF")
    style.configure("TButton", font=("Helvetica", 10, "bold"), padding=10, background="#A020F0", foreground="#000000")
    style.configure("TCheckbutton", font=("Helvetica", 10), background="#1E1E2E", foreground="#FFFFFF")
    style.configure("TEntry", padding=5, relief="flat", fieldbackground="#333344", foreground="#000000")

    # Frame central
    frm = ttk.Frame(root, padding="20 15 20 15", style="TFrame")
    frm.grid(sticky="nsew")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Variáveis de controle para monitorar entradas
    cipher_var = StringVar()
    message_var = StringVar()
    matrix_var = StringVar()
    is_inverse = BooleanVar(value=False)

    # Cipher
    ttk.Label(frm, text="Cifra:", style="TLabel").grid(column=0, row=0, sticky="e", pady=10)
    cipher_entry = ttk.Entry(frm, width=30, textvariable=cipher_var, style="TEntry")
    cipher_entry.grid(column=1, row=0, pady=10, padx=10)

    # Message
    ttk.Label(frm, text="Mensagem:", style="TLabel").grid(column=0, row=1, sticky="e", pady=10)
    message_entry = ttk.Entry(frm, width=30, textvariable=message_var, style="TEntry")
    message_entry.grid(column=1, row=1, pady=10, padx=10)

    # Matrix
    ttk.Label(frm, text="Matriz:", style="TLabel").grid(column=0, row=2, sticky="e", pady=10)
    matrix_entry = ttk.Entry(frm, width=30, textvariable=matrix_var, style="TEntry")
    matrix_entry.grid(column=1, row=2, pady=10, padx=10)

    # Inversivel
    verify_checkbox = ttk.Checkbutton(frm, text="Inversa", onvalue=1, offvalue=0, variable=is_inverse, style="TCheckbutton")
    verify_checkbox.grid(column=0, row=3, columnspan=1, pady=10)

    # Execute
    execute_button = ttk.Button(frm, text="Desvendar o Enigma", command=lambda: execute_operation(message_var.get(), cipher_var.get(), matrix_entry.get(), is_inverse.get(), code, decode), style="TButton")
    execute_button.grid(column=0, row=4, columnspan=2, pady=20)

    # Help
    help_button = ttk.Button(frm, text="Quebrar o Enigma", command=lambda: execute_break(message_var.get(), cipher_var.get(), break_code), style="TButton")
    help_button.grid(column=0, row=5, columnspan=2, pady=10)

    # Help
    help_button = ttk.Button(frm, text="Ajuda", command=show_help, style="TButton")
    help_button.grid(column=0, row=6, columnspan=2, pady=10)

    for child in frm.winfo_children():
        child.grid_configure(padx=10, pady=5)

    root.mainloop()

def execute_break(msg, cipher, break_code):
    """
    Executa a função de quebra da cifra de Hill.
    """
    try:
        if not msg or not cipher:
            raise ValueError("Preencha ambos os campos: Mensagem e Cifra.")

        # Chamar a função break_code com os parâmetros fornecidos
        msg_result = break_code(cipher, msg)  # Note que msg é o partial_decoded

        # Exibir o resultado
        messagebox.showinfo("Resultado", f"Cifra quebrada com sucesso!\nMensagem: {msg_result}")
    except Exception as e:
        messagebox.showerror("Erro!", f"Erro ao executar a operação:\n{e}")

def execute_operation(msg, cipher, matrix, inverse, code, decode):
    if not matrix:
        messagebox.showerror(title='Erro!', message='É necessário uma matriz para encriptar e descriptar.\nPreencha a matriz.')

    if msg and cipher:
        messagebox.showerror(title='Erro!', message='Preencha apenas um dos campos.')
    elif msg:
        cipher_result = code(msg, parse_matrix(matrix), inverse)
        messagebox.showinfo("Resultado", f"Mensagem codificada com sucesso!\nCifra: {cipher_result}")
    elif cipher:
        msg_result = decode(cipher, parse_matrix(matrix), inverse)
        messagebox.showinfo("Resultado", f"Cifra decodificada com sucesso!\nMensagem: {msg_result}")
    else:
        messagebox.showerror(title='Erro!', message='Preencha pelo menos um dos campos.')


def show_help():
    """
    Exibe as instruções de uso do programa.
    """
    help_message = ("""
Bem-vindo ao Linear Enigma!

Esta ferramenta permite codificar, decodificar e quebrar mensagens utilizando a Cifra de Hill. Siga as instruções abaixo para utilizar corretamente o programa:

Como usar:

1. Preencher os campos necessários:
   - Cifra: Insira o texto cifrado que deseja decodificar.
   - Mensagem: Insira o texto parcial decifrado (no caso de quebra de cifra) ou o texto original que deseja codificar.
   - Matriz: Insira a matriz de codificação/decodificação no formato: 1,2;3,4.
     Exemplo: 9,4;3,5 representa:
       [[9, 4],
        [3, 5]]

2. Escolher a operação:
   - Codificar Mensagem:
     - Preencha o campo "Mensagem" e o campo "Matriz".
     - Deixe o campo "Cifra" vazio.
     - Clique em "Desvendar o Enigma".
   - Decodificar Cifra:
     - Preencha o campo "Cifra" e o campo "Matriz".
     - Deixe o campo "Mensagem" vazio.
     - Clique em "Desvendar o Enigma".
   - Quebrar a Cifra:
     - Preencha ambos os campos "Mensagem" (com uma parte do texto decifrado) e "Cifra" (texto cifrado completo).
     - Deixe o campo "Matriz" vazio.
     - Clique em "Quebrar o Enigma".

3. Opção de Matriz Inversa:
   - Marque a opção Inversa caso precise trabalhar com a matriz inversa para codificação ou decodificação.

Dicas:

- Certifique-se de inserir a matriz corretamente no formato especificado (1,2;3,4).
- Preencha apenas os campos necessários para a operação escolhida.
"""
    )
    messagebox.showinfo("Ajuda", help_message)


def parse_matrix(matrix_str):
    """
    Converte uma string de matriz no formato "1,2;3,4" para uma lista de listas [[1, 2], [3, 4]].

    Parâmetros:
        matrix_str (str): String representando a matriz no formato "1,2;3,4".

    Retorna:
        list: Matriz como lista de listas.

    Exceções:
        ValueError: Se o formato for inválido ou se os elementos não puderem ser convertidos para números inteiros.
    """
    try:
        # Divide a string em linhas com base no separador `;`
        rows = matrix_str.strip().split(";")

        # Para cada linha, separa os elementos por `,` e converte para inteiros
        matrix = [list(map(int, row.split(","))) for row in rows]

        # Verifica se todas as linhas têm o mesmo número de colunas
        num_cols = len(matrix[0])
        if not all(len(row) == num_cols for row in matrix):
            raise ValueError("Watson.parse_matrix : Todas as linhas da matriz devem ter o mesmo número de colunas.")

        return matrix
    except Exception as e:
        raise ValueError(f"Watson.parse_matrix : Erro ao interpretar a matriz: {e}")