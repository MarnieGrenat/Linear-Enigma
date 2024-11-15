from tkinter import *
from tkinter import ttk
from tkinter import messagebox


def open_window(code, decode):
    root = Tk()
    root.title("Linear Enigma")

    # Estilização
    root.maxsize(width=400, height=300)
    root.minsize(width=400, height=300)
    root.iconbitmap(r"src\assets\icon.ico")
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

    # Função para gerenciar os campos de entrada
    def toggle_inputs(*args):
        if cipher_var.get():
            message_entry.config(state="disabled")
        else:
            message_entry.config(state="normal")

        if message_var.get():
            cipher_entry.config(state="disabled")
        else:
            cipher_entry.config(state="normal")

    # Variáveis de controle para monitorar entradas
    cipher_var = StringVar()
    message_var = StringVar()
    matrix_var = StringVar()
    is_inverse = BooleanVar(value=False)
    cipher_var.trace_add("write", toggle_inputs)
    message_var.trace_add("write", toggle_inputs)

    # Label e Entry para Cipher
    ttk.Label(frm, text="Cifra:", style="TLabel").grid(column=0, row=0, sticky="e", pady=10)
    cipher_entry = ttk.Entry(frm, width=30, textvariable=cipher_var, style="TEntry")
    cipher_entry.grid(column=1, row=0, pady=10, padx=10)

    # Label e Entry para Message
    ttk.Label(frm, text="Mensagem:", style="TLabel").grid(column=0, row=1, sticky="e", pady=10)
    message_entry = ttk.Entry(frm, width=30, textvariable=message_var, style="TEntry")
    message_entry.grid(column=1, row=1, pady=10, padx=10)

    # Label e Entry para Matrix
    ttk.Label(frm, text="Matriz:", style="TLabel").grid(column=0, row=2, sticky="e", pady=10)
    matrix_entry = ttk.Entry(frm, width=30, textvariable=matrix_var, style="TEntry")
    matrix_entry.grid(column=1, row=2, pady=10, padx=10)

    # Checkbox para verificar inversibilidade
    verify_checkbox = ttk.Checkbutton(frm, text="Inversa", onvalue=1, offvalue=0, variable=is_inverse, style="TCheckbutton")
    verify_checkbox.grid(column=0, row=3, columnspan=1, pady=10)

    # Botão para executar a função
    execute_button = ttk.Button(frm, text="Desvendar o Enigma", command=lambda: execute_operation(message_var.get(), cipher_var.get(), matrix_entry.get(), is_inverse.get(), code, decode), style="TButton")
    execute_button.grid(column=0, row=4, columnspan=2, pady=20)

    # Botão de Help
    help_button = ttk.Button(frm, text="Ajuda", command=show_help, style="TButton")
    help_button.grid(column=0, row=5, columnspan=2, pady=10)

    for child in frm.winfo_children():
        child.grid_configure(padx=10, pady=5)

    root.mainloop()


def execute_operation(msg, cipher, matrix, inverse, code, decode):
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
    help_message = (
        "Bem-vindo ao Linear Enigma!\n\n"
        "Como usar o programa:\n"
        "- Preencha **apenas um dos campos**: Cipher ou Message.\n"
        "- No campo Matrix, insira uma matriz no formato: 1,2;3,4\n"
        "  Isso representa a matriz:\n"
        "  [[1, 2],\n"
        "   [3, 4]]\n"
        "- Clique no botão Execute Cipher para codificar ou decodificar a mensagem.\n\n"
        "Dicas:\n"
        "- Se preencher Cipher, a mensagem será decodificada.\n"
        "- Se preencher Message, ela será codificada usando a matriz informada.\n"
        "- Certifique-se de preencher a matriz antes de executar qualquer operação.\n"
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