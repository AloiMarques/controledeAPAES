import tkinter as tk

# Configuração do tema padrão (dark mode)
def aplicar_tema(widget):
    widget.configure(bg="#2b2b2b", fg="white")
    if isinstance(widget, tk.Tk) or isinstance(widget, tk.Toplevel):
        widget.option_add("*Background", "#2b2b2b")
        widget.option_add("*Foreground", "white")
        widget.option_add("*Button.Background", "blue")
        widget.option_add("*Button.Foreground", "white")
        widget.option_add("*Entry.Background", "#404040")
        widget.option_add("*Entry.Foreground", "white")
        widget.option_add("*TCombobox*Listbox.Background", "#2b2b2b")
        widget.option_add("*TCombobox*Listbox.Foreground", "white")

# Função para aplicar o tema em widgets filhos
def aplicar_tema_em_todos(widget):
    aplicar_tema(widget)
    for child in widget.winfo_children():
        if isinstance(child, tk.Frame):
            aplicar_tema_em_todos(child)
        else:
            aplicar_tema(child)

# Função para configurar botões
def configurar_botoes(botao):
    botao.configure(bg="blue", fg="white", activebackground="#1E90FF", activeforeground="white")
