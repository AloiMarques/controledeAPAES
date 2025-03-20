import os
import shutil
from datetime import datetime
import sqlite3

# Caminho do banco de dados e da pasta de backups
DB_PATH = "database/sistema.db"
BACKUP_DIR = "database/backups"

# Função para criar um backup
def criar_backup():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    timestamp = datetime.now().strftime("%d%m%Y%H%M")
    backup_path = os.path.join(BACKUP_DIR, f"backup_{timestamp}.db")

    if os.path.exists(DB_PATH):
        shutil.copy(DB_PATH, backup_path)
        print(f"Backup criado: {backup_path}")

        # Limita o número de backups a 3 por dia
        limpar_backups_antigos()
    else:
        print("Banco de dados não encontrado. Nenhum backup foi criado.")

# Função para limpar backups antigos (limita a 3 por dia)
def limpar_backups_antigos():
    backups = [f for f in os.listdir(BACKUP_DIR) if f.startswith(f"backup_{datetime.now().strftime('%d%m%Y')}")]
    if len(backups) > 3:
        backups.sort(key=lambda x: os.path.getctime(os.path.join(BACKUP_DIR, x)))
        for backup in backups[:-3]:
            os.remove(os.path.join(BACKUP_DIR, backup))
            print(f"Backup antigo removido: {backup}")

# Função para listar todos os backups disponíveis
def listar_backups():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    backups = [f for f in os.listdir(BACKUP_DIR) if f.endswith(".db")]
    backups.sort(key=lambda x: os.path.getctime(os.path.join(BACKUP_DIR, x)))
    return backups

# Função para restaurar um backup
def restaurar_backup(backup_file):
    backup_path = os.path.join(BACKUP_DIR, backup_file)

    if not os.path.exists(backup_path):
        raise FileNotFoundError(f"O arquivo de backup {backup_file} não foi encontrado.")

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    shutil.copy(backup_path, DB_PATH)
    print(f"Backup restaurado: {backup_file}")

# Interface gráfica para gerenciar backups
def abrir_gerenciador_backups():
    import tkinter as tk
    from tkinter import ttk, messagebox

    def realizar_backup():
        criar_backup()
        atualizar_lista_backups()

    def realizar_restauracao():
        selected_backup = backup_combobox.get()
        if not selected_backup:
            messagebox.showerror("Erro", "Por favor, selecione um backup para restaurar.")
            return

        try:
            restaurar_backup(selected_backup)
            messagebox.showinfo("Sucesso", f"Backup {selected_backup} restaurado com sucesso!")
        except FileNotFoundError as e:
            messagebox.showerror("Erro", str(e))

    def atualizar_lista_backups():
        backups = listar_backups()
        backup_combobox["values"] = backups
        if backups:
            backup_combobox.set(backups[-1])  # Seleciona o backup mais recente

    # Janela do gerenciador de backups
    backup_window = tk.Tk()
    backup_window.title("Gerenciador de Backups - Sistema APAE")
    backup_window.geometry("400x300")
    backup_window.configure(bg="#2b2b2b")

    # Layout
    tk.Label(
        backup_window, text="Gerenciador de Backups", font=("Arial", 16), bg="#2b2b2b", fg="blue"
    ).pack(pady=10)

    tk.Button(
        backup_window, text="Criar Backup", command=realizar_backup, bg="blue", fg="white", width=20
    ).pack(pady=10)

    tk.Label(backup_window, text="Restaurar Backup:", bg="#2b2b2b", fg="white").pack(anchor="w", padx=20, pady=5)
    backup_combobox = ttk.Combobox(backup_window, width=30)
    backup_combobox.pack(pady=5)

    tk.Button(
        backup_window, text="Restaurar Backup", command=realizar_restauracao, bg="blue", fg="white", width=20
    ).pack(pady=10)

    atualizar_lista_backups()
    backup_window.mainloop()
