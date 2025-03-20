import sqlite3
import os
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from modules.pacientes import abrir_pacientes
from modules.especialistas import abrir_especialistas
from modules.agendamentos import abrir_agendamentos
from modules.administracao import abrir_administracao
from modules.lembretes import abrir_lembretes

# Configurações do tema
ctk.set_appearance_mode("dark")  # Tema escuro
ctk.set_default_color_theme("blue")  # Botões azuis

# Cores personalizadas (inspiradas na APAE)
COR_PRINCIPAL = "#002060"  # Azul escuro
COR_SECUNDARIA = "#ffffff"  # Branco
COR_DESTAQUE = "#0056b3"  # Azul intermediário

# Função para inicializar o banco de dados
def inicializar_banco():
    if not os.path.exists('database'):
        os.makedirs('database')

    db_path = 'database/sistema.db'
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Criação das tabelas
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL,
                            password TEXT NOT NULL,
                            role TEXT NOT NULL)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS pacientes (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            idade INTEGER,
                            endereco TEXT,
                            contato TEXT,
                            diagnostico TEXT,
                            observacoes TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS especialistas (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            especialidade TEXT,
                            horarios TEXT,
                            dias_semana TEXT,
                            contato TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS agendamentos (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            paciente_id INTEGER,
                            especialista_id INTEGER,
                            data TEXT,
                            hora TEXT,
                            status TEXT,
                            justificativa TEXT,
                            FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
                            FOREIGN KEY (especialista_id) REFERENCES especialistas (id))''')

        cursor.execute('''INSERT INTO usuarios (username, password, role)
                           VALUES ('admin', '1234', 'admin')''')

        conn.commit()
        conn.close()

# Função para confirmar presença ou justificar ausência
def confirmar_presenca(agendamento_id, status, justificativa=""):
    conn = sqlite3.connect('database/sistema.db')
    cursor = conn.cursor()
    if status == "Faltou" and not justificativa:
        messagebox.showerror("Erro", "Justificativa é obrigatória para ausência.")
        return
    cursor.execute("""
        UPDATE agendamentos
        SET status = ?, justificativa = ?
        WHERE id = ?
    """, (status, justificativa, agendamento_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Status do agendamento atualizado com sucesso.")
    listar_agenda_do_dia()

# Função para listar a agenda do dia
def listar_agenda_do_dia():
    for widget in agenda_frame.winfo_children():
        widget.destroy()

    hoje = datetime.now().strftime("%d/%m/%Y")
    conn = sqlite3.connect('database/sistema.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.id, p.nome, e.nome, a.hora, a.status
        FROM agendamentos a
        JOIN pacientes p ON a.paciente_id = p.id
        JOIN especialistas e ON a.especialista_id = e.id
        WHERE a.data = ?
        ORDER BY a.hora
    """, (hoje,))
    agendamentos = cursor.fetchall()
    conn.close()

    if agendamentos:
        for agendamento in agendamentos:
            agendamento_frame = ctk.CTkFrame(agenda_frame, fg_color="#333333", corner_radius=10)
            agendamento_frame.pack(pady=10, padx=20, fill="x")

            ctk.CTkLabel(
                agendamento_frame,
                text=f"Paciente: {agendamento[1]} | Especialista: {agendamento[2]} | Hora: {agendamento[3]} | Status: {agendamento[4]}",
                font=("Arial", 14),
                text_color=COR_SECUNDARIA
            ).pack(pady=5, padx=5)

            # Combobox para selecionar status
            status_combobox = ctk.CTkComboBox(
                agendamento_frame,
                values=["Compareceu", "Faltou"],
                width=200
            )
            status_combobox.pack(side="left", padx=5)

            # Campo para justificativa
            justificativa_entry = ctk.CTkEntry(
                agendamento_frame,
                placeholder_text="Justificativa (se necessário)",
                width=300
            )
            justificativa_entry.pack(side="left", padx=5)

            # Botão para salvar status
            ctk.CTkButton(
                agendamento_frame,
                text="Salvar",
                fg_color=COR_DESTAQUE,
                text_color=COR_SECUNDARIA,
                hover_color="#0078d7",
                command=lambda ag_id=agendamento[0], status=status_combobox, justificativa=justificativa_entry:
                confirmar_presenca(ag_id, status.get(), justificativa.get())
            ).pack(side="left", padx=5)
    else:
        ctk.CTkLabel(
            agenda_frame,
            text="Nenhum agendamento para hoje.",
            font=("Arial", 16),
            text_color=COR_SECUNDARIA
        ).pack(pady=20)

# Função de login
def login():
    username = username_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect('database/sistema.db')
    cursor = conn.cursor()

    cursor.execute("SELECT role FROM usuarios WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    if user:
        role = user[0]
        login_window.destroy()
        abrir_tela_principal(role)
    else:
        messagebox.showerror("Erro de Login", "Usuário ou senha inválidos.")
    conn.close()

# Tela principal do sistema
def abrir_tela_principal(role):
    main_window = ctk.CTk()
    main_window.title("Sistema APAE - Tela Principal")
    main_window.geometry("1200x700")
    main_window.configure(fg_color=COR_PRINCIPAL)

    # Cabeçalho
    header = ctk.CTkFrame(main_window, fg_color=COR_PRINCIPAL)
    header.pack(side="top", fill="x")

    ctk.CTkLabel(
        header,
        text="Sistema APAE",
        font=("Arial", 28, "bold"),
        text_color=COR_SECUNDARIA
    ).pack(pady=10)

    # Menu lateral
    sidebar = ctk.CTkFrame(main_window, width=250, fg_color="#1a1a1a")
    sidebar.pack(side="left", fill="y")

    ctk.CTkButton(
        sidebar,
        text="Gerenciar Pacientes",
        command=abrir_pacientes,
        fg_color=COR_DESTAQUE,
        text_color=COR_SECUNDARIA,
        hover_color="#0078d7",
        font=("Arial", 14)
    ).pack(pady=10, padx=20, fill="x")

    ctk.CTkButton(
        sidebar,
        text="Gerenciar Especialistas",
        command=abrir_especialistas,
        fg_color=COR_DESTAQUE,
        text_color=COR_SECUNDARIA,
        hover_color="#0078d7",
        font=("Arial", 14)
    ).pack(pady=10, padx=20, fill="x")

    ctk.CTkButton(
        sidebar,
        text="Agendamentos",
        command=abrir_agendamentos,
        fg_color=COR_DESTAQUE,
        text_color=COR_SECUNDARIA,
        hover_color="#0078d7",
        font=("Arial", 14)
    ).pack(pady=10, padx=20, fill="x")

    ctk.CTkButton(
        sidebar,
        text="Gerenciar Lembretes",
        command=abrir_lembretes,
        fg_color=COR_DESTAQUE,
        text_color=COR_SECUNDARIA,
        hover_color="#0078d7",
        font=("Arial", 14)
    ).pack(pady=10, padx=20, fill="x")

    if role == "admin":
        ctk.CTkButton(
            sidebar,
            text="Administração",
            command=abrir_administracao,
            fg_color=COR_DESTAQUE,
            text_color=COR_SECUNDARIA,
            hover_color="#0078d7",
            font=("Arial", 14)
        ).pack(pady=10, padx=20, fill="x")

    # Área principal (agenda do dia)
    global agenda_frame
    main_content = ctk.CTkFrame(main_window, fg_color="#262626")
    main_content.pack(side="right", expand=True, fill="both", padx=10, pady=10)

    ctk.CTkLabel(
        main_content,
        text="Agenda do Dia",
        font=("Arial", 20, "bold"),
        text_color=COR_SECUNDARIA
    ).pack(pady=20)

    agenda_frame = ctk.CTkFrame(main_content, fg_color="#1a1a1a", corner_radius=10)
    agenda_frame.pack(expand=True, fill="both", padx=10, pady=10)

    listar_agenda_do_dia()

    main_window.mainloop()

# Tela de login
login_window = ctk.CTk()
login_window.title("Sistema APAE - Login")
login_window.geometry("500x400")
login_window.configure(fg_color=COR_PRINCIPAL)

# Título
ctk.CTkLabel(
    login_window,
    text="Login",
    font=("Arial", 24, "bold"),
    text_color=COR_SECUNDARIA
).pack(pady=30)

# Campo de usuário
username_entry = ctk.CTkEntry(
    login_window,
    placeholder_text="Usuário",
    font=("Arial", 14),
    width=300
)
username_entry.pack(pady=10)

# Campo de senha
password_entry = ctk.CTkEntry(
    login_window,
    placeholder_text="Senha",
    show="*",
    font=("Arial", 14),
    width=300
)
password_entry.pack(pady=10)

# Botão de login
ctk.CTkButton(
    login_window,
    text="Entrar",
    command=login,
    font=("Arial", 16, "bold"),
    fg_color=COR_DESTAQUE,
    text_color=COR_SECUNDARIA,
    hover_color="#0078d7",
    width=150
).pack(pady=30)

# Inicializar banco de dados
inicializar_banco()

login_window.mainloop()
