import sqlite3
import customtkinter as ctk
from tkinter import messagebox

# Configuração do tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Função para abrir a janela de gerenciamento de pacientes
def abrir_pacientes():
    pacientes_window = ctk.CTk()
    pacientes_window.title("Gerenciamento de Pacientes - Sistema APAE")
    pacientes_window.geometry("1000x700")
    pacientes_window.configure(fg_color="#002060")  # Azul escuro da APAE

    # Função para listar pacientes
    def listar_pacientes():
        for widget in pacientes_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect('database/sistema.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nome, idade, endereco, contato, diagnostico, observacoes
            FROM pacientes
            ORDER BY id
        """)
        pacientes = cursor.fetchall()
        conn.close()

        if pacientes:
            for paciente in pacientes:
                ctk.CTkLabel(
                    pacientes_frame,
                    text=f"ID: {paciente[0]} | Nome: {paciente[1]} | Idade: {paciente[2]} | Endereço: {paciente[3]} "
                         f"| Contato: {paciente[4]} | Diagnóstico: {paciente[5]} | Observações: {paciente[6]}",
                    font=("Arial", 12),
                    text_color="white"
                ).pack(anchor="w", pady=5)
        else:
            ctk.CTkLabel(
                pacientes_frame,
                text="Nenhum paciente cadastrado.",
                font=("Arial", 12),
                text_color="white"
            ).pack(anchor="w", pady=5)

    # Função para cadastrar paciente
    def cadastrar_paciente():
        nome = nome_entry.get()
        idade = idade_entry.get()
        endereco = endereco_entry.get()
        contato = contato_entry.get()
        diagnostico = diagnostico_entry.get()
        observacoes = observacoes_entry.get()

        if not nome or not idade or not endereco or not contato or not diagnostico:
            messagebox.showerror("Erro", "Todos os campos obrigatórios devem ser preenchidos.")
            return

        conn = sqlite3.connect('database/sistema.db')
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM pacientes")
        last_id = cursor.fetchone()[0]
        novo_id = (last_id + 1) if last_id else 1

        cursor.execute("""
            INSERT INTO pacientes (id, nome, idade, endereco, contato, diagnostico, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (novo_id, nome, idade, endereco, contato, diagnostico, observacoes))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")
        nome_entry.delete(0, ctk.END)
        idade_entry.delete(0, ctk.END)
        endereco_entry.delete(0, ctk.END)
        contato_entry.delete(0, ctk.END)
        diagnostico_entry.delete(0, ctk.END)
        observacoes_entry.delete(0, ctk.END)
        listar_pacientes()

    # Função para excluir paciente
    def excluir_paciente():
        id_paciente = id_entry.get()

        if not id_paciente:
            messagebox.showerror("Erro", "Informe o ID do paciente para excluir.")
            return

        conn = sqlite3.connect('database/sistema.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pacientes WHERE id = ?", (id_paciente,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Paciente excluído com sucesso!")
        listar_pacientes()

    # Layout da janela
    ctk.CTkLabel(
        pacientes_window,
        text="Gerenciamento de Pacientes",
        font=("Arial", 20, "bold"),
        text_color="white"
    ).pack(pady=20)

    # Formulário de cadastro
    form_frame = ctk.CTkFrame(pacientes_window, fg_color="#1a1a1a", corner_radius=10)
    form_frame.pack(pady=20, padx=20, fill="x")

    ctk.CTkLabel(form_frame, text="Nome:", font=("Arial", 14), text_color="white").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    nome_entry = ctk.CTkEntry(form_frame, width=300)
    nome_entry.grid(row=0, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Idade:", font=("Arial", 14), text_color="white").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    idade_entry = ctk.CTkEntry(form_frame, width=300)
    idade_entry.grid(row=1, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Endereço:", font=("Arial", 14), text_color="white").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    endereco_entry = ctk.CTkEntry(form_frame, width=300)
    endereco_entry.grid(row=2, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Contato:", font=("Arial", 14), text_color="white").grid(row=3, column=0, padx=10, pady=10, sticky="e")
    contato_entry = ctk.CTkEntry(form_frame, width=300)
    contato_entry.grid(row=3, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Diagnóstico:", font=("Arial", 14), text_color="white").grid(row=4, column=0, padx=10, pady=10, sticky="e")
    diagnostico_entry = ctk.CTkEntry(form_frame, width=300)
    diagnostico_entry.grid(row=4, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Observações:", font=("Arial", 14), text_color="white").grid(row=5, column=0, padx=10, pady=10, sticky="e")
    observacoes_entry = ctk.CTkEntry(form_frame, width=300)
    observacoes_entry.grid(row=5, column=1, padx=10, pady=10)

    ctk.CTkButton(
        form_frame,
        text="Cadastrar Paciente",
        command=cadastrar_paciente,
        fg_color="#0056b3",
        text_color="white"
    ).grid(row=6, column=1, pady=20)

    # Exclusão de paciente
    exclusao_frame = ctk.CTkFrame(pacientes_window, fg_color="#1a1a1a", corner_radius=10)
    exclusao_frame.pack(pady=20, padx=20, fill="x")

    ctk.CTkLabel(exclusao_frame, text="ID do Paciente:", font=("Arial", 14), text_color="white").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    id_entry = ctk.CTkEntry(exclusao_frame, width=300)
    id_entry.grid(row=0, column=1, padx=10, pady=10)

    ctk.CTkButton(
        exclusao_frame,
        text="Excluir Paciente",
        command=excluir_paciente,
        fg_color="#b30000",
        text_color="white"
    ).grid(row=0, column=2, padx=10, pady=10)

    # Listagem de pacientes
    pacientes_frame = ctk.CTkFrame(pacientes_window, fg_color="#1a1a1a", corner_radius=10)
    pacientes_frame.pack(pady=20, padx=20, fill="both", expand=True)
    listar_pacientes()

    pacientes_window.mainloop()
