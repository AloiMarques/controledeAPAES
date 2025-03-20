import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Função para inicializar o banco de dados de lembretes
def inicializar_tabela_lembretes():
    conn = sqlite3.connect('database/sistema.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lembretes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            descricao TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Função para exibir lembretes na data atual
def verificar_lembretes_hoje():
    conn = sqlite3.connect('database/sistema.db')
    cursor = conn.cursor()
    hoje = datetime.now().strftime("%d/%m/%Y")
    cursor.execute("SELECT descricao FROM lembretes WHERE data = ?", (hoje,))
    lembretes_hoje = cursor.fetchall()
    conn.close()

    if lembretes_hoje:
        mensagem = "\n".join([lembrete[0] for lembrete in lembretes_hoje])
        messagebox.showinfo("Lembretes de Hoje", f"Lembretes para hoje:\n\n{mensagem}")

# Função para abrir o módulo de lembretes
def abrir_lembretes():
    lembretes_window = tk.Tk()
    lembretes_window.title("Gerenciamento de Lembretes - Sistema APAE")
    lembretes_window.geometry("700x500")
    lembretes_window.configure(bg="#2b2b2b")

    # Função para listar lembretes
    def listar_lembretes():
        for widget in lembretes_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect('database/sistema.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, data, descricao FROM lembretes ORDER BY data")
        lembretes = cursor.fetchall()
        conn.close()

        if lembretes:
            for lembrete in lembretes:
                tk.Label(
                    lembretes_frame,
                    text=f"ID: {lembrete[0]} | Data: {lembrete[1]} | Descrição: {lembrete[2]}",
                    bg="#2b2b2b",
                    fg="white"
                ).pack(anchor="w", pady=2)
        else:
            tk.Label(
                lembretes_frame,
                text="Nenhum lembrete cadastrado.",
                bg="#2b2b2b",
                fg="white"
            ).pack(anchor="w", pady=2)

    # Função para cadastrar um lembrete
    def cadastrar_lembrete():
        data = data_entry.get().strip()
        descricao = descricao_entry.get().strip()

        if not data or not descricao:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        try:
            datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro", "A data deve estar no formato DD/MM/AAAA.")
            return

        conn = sqlite3.connect('database/sistema.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO lembretes (data, descricao) VALUES (?, ?)", (data, descricao))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Lembrete cadastrado com sucesso!")
        data_entry.delete(0, tk.END)
        descricao_entry.delete(0, tk.END)
        listar_lembretes()

    # Função para excluir um lembrete
    def excluir_lembrete():
        lembrete_id = id_entry.get().strip()

        if not lembrete_id:
            messagebox.showerror("Erro", "Por favor, informe o ID do lembrete para exclusão.")
            return

        conn = sqlite3.connect('database/sistema.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM lembretes WHERE id = ?", (lembrete_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Lembrete excluído com sucesso!")
        id_entry.delete(0, tk.END)
        listar_lembretes()

    # Layout da janela
    tk.Label(
        lembretes_window,
        text="Gerenciamento de Lembretes",
        font=("Arial", 16),
        bg="#2b2b2b",
        fg="blue"
    ).pack(pady=10)

    # Formulário de lembretes
    form_frame = tk.Frame(lembretes_window, bg="#2b2b2b")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="ID (para excluir):", bg="#2b2b2b", fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    id_entry = ttk.Entry(form_frame, width=30)
    id_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Data (DD/MM/AAAA):", bg="#2b2b2b", fg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    data_entry = ttk.Entry(form_frame, width=30)
    data_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Descrição:", bg="#2b2b2b", fg="white").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    descricao_entry = ttk.Entry(form_frame, width=30)
    descricao_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Button(form_frame, text="Cadastrar", command=cadastrar_lembrete, bg="blue", fg="white", width=15).grid(row=3, column=0, pady=10)
    tk.Button(form_frame, text="Excluir", command=excluir_lembrete, bg="blue", fg="white", width=15).grid(row=3, column=1, pady=10)

    # Listagem de lembretes
    lembretes_frame = tk.Frame(lembretes_window, bg="#2b2b2b")
    lembretes_frame.pack(pady=10, fill="both", expand=True)
    listar_lembretes()

    lembretes_window.mainloop()

# Inicializar a tabela de lembretes (chamar no início do sistema)
inicializar_tabela_lembretes()
