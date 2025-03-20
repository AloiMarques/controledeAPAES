import sqlite3
import customtkinter as ctk
from tkinter import messagebox

# Configuração do tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Função para abrir a janela de gerenciamento de especialistas
def abrir_especialistas():
    especialistas_window = ctk.CTk()
    especialistas_window.title("Gerenciamento de Especialistas - Sistema APAE")
    especialistas_window.geometry("1000x700")
    especialistas_window.configure(fg_color="#002060")  # Azul escuro da APAE

    # Função para listar os especialistas
    def listar_especialistas():
        for widget in especialistas_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect('database/sistema.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nome, especialidade, dias_semana, horarios
            FROM especialistas
            ORDER BY id
        """)
        especialistas = cursor.fetchall()
        conn.close()

        if especialistas:
            for especialista in especialistas:
                ctk.CTkLabel(
                    especialistas_frame,
                    text=f"ID: {especialista[0]} | Nome: {especialista[1]} | Especialidade: {especialista[2]} "
                         f"| Dias: {especialista[3]} | Horários: {especialista[4]}",
                    font=("Arial", 12),
                    text_color="white"
                ).pack(anchor="w", pady=5)
        else:
            ctk.CTkLabel(
                especialistas_frame,
                text="Nenhum especialista cadastrado.",
                font=("Arial", 12),
                text_color="white"
            ).pack(anchor="w", pady=5)

    # Função para cadastrar especialista
    def cadastrar_especialista():
        nome = nome_entry.get()
        especialidade = especialidade_entry.get()
        dias_semana = ", ".join([dia for dia, var in dias_checkboxes.items() if var.get()])
        entrada = entrada_entry.get()
        saida = saida_entry.get()

        if not nome or not especialidade or not dias_semana or not entrada or not saida:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        horarios = f"{entrada} - {saida}"

        conn = sqlite3.connect('database/sistema.db')
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM especialistas")
        last_id = cursor.fetchone()[0]
        novo_id = (last_id + 1) if last_id else 1

        cursor.execute("""
            INSERT INTO especialistas (id, nome, especialidade, dias_semana, horarios)
            VALUES (?, ?, ?, ?, ?)
        """, (novo_id, nome, especialidade, dias_semana, horarios))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Especialista cadastrado com sucesso!")
        nome_entry.delete(0, ctk.END)
        especialidade_entry.delete(0, ctk.END)
        entrada_entry.delete(0, ctk.END)
        saida_entry.delete(0, ctk.END)
        for checkbox in dias_checkboxes.values():
            checkbox.set(False)
        listar_especialistas()

    # Função para excluir especialista
    def excluir_especialista():
        id_especialista = id_entry.get()

        if not id_especialista:
            messagebox.showerror("Erro", "Informe o ID do especialista para excluir.")
            return

        conn = sqlite3.connect('database/sistema.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM especialistas WHERE id = ?", (id_especialista,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Especialista excluído com sucesso!")
        listar_especialistas()

    # Layout da janela
    ctk.CTkLabel(
        especialistas_window,
        text="Gerenciamento de Especialistas",
        font=("Arial", 20, "bold"),
        text_color="white"
    ).pack(pady=20)

    # Formulário de cadastro
    form_frame = ctk.CTkFrame(especialistas_window, fg_color="#1a1a1a", corner_radius=10)
    form_frame.pack(pady=20, padx=20, fill="x")

    ctk.CTkLabel(form_frame, text="Nome:", font=("Arial", 14), text_color="white").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    nome_entry = ctk.CTkEntry(form_frame, width=300)
    nome_entry.grid(row=0, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Especialidade:", font=("Arial", 14), text_color="white").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    especialidade_entry = ctk.CTkEntry(form_frame, width=300)
    especialidade_entry.grid(row=1, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Dias da Semana:", font=("Arial", 14), text_color="white").grid(row=2, column=0, padx=10, pady=10, sticky="ne")
    dias_frame = ctk.CTkFrame(form_frame, fg_color="#1a1a1a")
    dias_frame.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    dias_checkboxes = {
        "Segunda-feira": ctk.StringVar(),
        "Terça-feira": ctk.StringVar(),
        "Quarta-feira": ctk.StringVar(),
        "Quinta-feira": ctk.StringVar(),
        "Sexta-feira": ctk.StringVar()
    }
    for dia, var in dias_checkboxes.items():
        ctk.CTkCheckBox(dias_frame, text=dia, variable=var, text_color="white").pack(anchor="w")

    ctk.CTkLabel(form_frame, text="Horário de Entrada:", font=("Arial", 14), text_color="white").grid(row=3, column=0, padx=10, pady=10, sticky="e")
    entrada_entry = ctk.CTkEntry(form_frame, width=300)
    entrada_entry.grid(row=3, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Horário de Saída:", font=("Arial", 14), text_color="white").grid(row=4, column=0, padx=10, pady=10, sticky="e")
    saida_entry = ctk.CTkEntry(form_frame, width=300)
    saida_entry.grid(row=4, column=1, padx=10, pady=10)

    ctk.CTkButton(
        form_frame,
        text="Cadastrar Especialista",
        command=cadastrar_especialista,
        fg_color="#0056b3",
        text_color="white"
    ).grid(row=5, column=1, pady=20)

    # Exclusão de especialista
    exclusao_frame = ctk.CTkFrame(especialistas_window, fg_color="#1a1a1a", corner_radius=10)
    exclusao_frame.pack(pady=20, padx=20, fill="x")

    ctk.CTkLabel(exclusao_frame, text="ID do Especialista:", font=("Arial", 14), text_color="white").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    id_entry = ctk.CTkEntry(exclusao_frame, width=300)
    id_entry.grid(row=0, column=1, padx=10, pady=10)

    ctk.CTkButton(
        exclusao_frame,
        text="Excluir Especialista",
        command=excluir_especialista,
        fg_color="#b30000",
        text_color="white"
    ).grid(row=0, column=2, padx=10, pady=10)

    # Listagem de especialistas
    especialistas_frame = ctk.CTkFrame(especialistas_window, fg_color="#1a1a1a", corner_radius=10)
    especialistas_frame.pack(pady=20, padx=20, fill="both", expand=True)
    listar_especialistas()

    especialistas_window.mainloop()
