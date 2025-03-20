import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Função para autenticar o usuário
def autenticar_usuario(username, password):
    conn = sqlite3.connect('database/sistema.db')
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM usuarios WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return user[0]  # Retorna o papel do usuário (admin ou recepcionista)
    return None

# Função para abrir a janela de login
def abrir_tela_login(callback_sucesso):
    def realizar_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        role = autenticar_usuario(username, password)
        if role:
            login_window.destroy()  # Fecha a janela de login
            callback_sucesso(role)  # Chama o callback com o papel do usuário
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    # Janela de login
    login_window = tk.Tk()
    login_window.title("Login - Sistema APAE")
    login_window.geometry("400x300")
    login_window.configure(bg="#2b2b2b")

    # Layout
    tk.Label(login_window, text="Login", font=("Arial", 20), bg="#2b2b2b", fg="white").pack(pady=20)
    tk.Label(login_window, text="Usuário:", bg="#2b2b2b", fg="white").pack(anchor="w", padx=50, pady=5)
    username_entry = ttk.Entry(login_window, width=30)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Senha:", bg="#2b2b2b", fg="white").pack(anchor="w", padx=50, pady=5)
    password_entry = ttk.Entry(login_window, show="*", width=30)
    password_entry.pack(pady=5)

    tk.Button(login_window, text="Entrar", command=realizar_login, bg="blue", fg="white", width=15).pack(pady=20)

    login_window.mainloop()

# Função para criar novos usuários (apenas para administradores)
def cadastrar_usuario(username, password, role):
    if not username or not password or not role:
        raise ValueError("Todos os campos devem ser preenchidos.")

    conn = sqlite3.connect('database/sistema.db')
    cursor = conn.cursor()

    # Verifica se o usuário já existe
    cursor.execute("SELECT * FROM usuarios WHERE username=?", (username,))
    if cursor.fetchone():
        conn.close()
        raise ValueError("Usuário já existe.")

    # Insere o novo usuário
    cursor.execute("INSERT INTO usuarios (username, password, role) VALUES (?, ?, ?)", (username, password, role))
    conn.commit()
    conn.close()

# Função para alterar senha de um usuário
def alterar_senha(username, nova_senha):
    if not username or not nova_senha:
        raise ValueError("Usuário e nova senha são obrigatórios.")

    conn = sqlite3.connect('database/sistema.db')
    cursor = conn.cursor()

    # Verifica se o usuário existe
    cursor.execute("SELECT * FROM usuarios WHERE username=?", (username,))
    if not cursor.fetchone():
        conn.close()
        raise ValueError("Usuário não encontrado.")

    # Atualiza a senha
    cursor.execute("UPDATE usuarios SET password=? WHERE username=?", (nova_senha, username))
    conn.commit()
    conn.close()

# Função para deletar um usuário (apenas para administradores)
def excluir_usuario(username):
    if not username:
        raise ValueError("Usuário é obrigatório.")

    conn = sqlite3.connect('database/sistema.db')
    cursor = conn.cursor()

    # Verifica se o usuário existe
    cursor.execute("SELECT * FROM usuarios WHERE username=?", (username,))
    if not cursor.fetchone():
        conn.close()
        raise ValueError("Usuário não encontrado.")

    # Deleta o usuário
    cursor.execute("DELETE FROM usuarios WHERE username=?", (username,))
    conn.commit()
    conn.close()
