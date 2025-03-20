import sqlite3
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta

# Configuração do tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Função para abrir a janela de agendamentos
def abrir_agendamentos():
    agendamentos_window = ctk.CTk()
    agendamentos_window.title("Gerenciamento de Agendamentos - Sistema APAE")
    agendamentos_window.geometry("1000x700")
    agendamentos_window.configure(fg_color="#002060")  # Azul escuro da APAE

    # Função para listar os agendamentos
    def listar_agendamentos():
        for widget in agendamentos_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect('database/sistema.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id, p.nome, e.nome, a.data, a.hora, a.status
            FROM agendamentos a
            JOIN pacientes p ON a.paciente_id = p.id
            JOIN especialistas e ON a.especialista_id = e.id
            ORDER BY a.data, a.hora
        """)
        agendamentos = cursor.fetchall()
        conn.close()

        if agendamentos:
            for agendamento in agendamentos:
                ctk.CTkLabel(
                    agendamentos_frame,
                    text=f"ID: {agendamento[0]} | Paciente: {agendamento[1]} | Especialista: {agendamento[2]} "
                         f"| Data: {agendamento[3]} | Hora: {agendamento[4]} | Status: {agendamento[5]}",
                    font=("Arial", 12),
                    text_color="white"
                ).pack(anchor="w", pady=5)
        else:
            ctk.CTkLabel(
                agendamentos_frame,
                text="Nenhum agendamento encontrado.",
                font=("Arial", 12),
                text_color="white"
            ).pack(anchor="w", pady=5)

    # Função para verificar conflitos de horário
    def verificar_conflitos(data, hora, especialista_id):
        conn = sqlite3.connect('database/sistema.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM agendamentos
            WHERE data = ? AND hora = ? AND especialista_id = ?
        """, (data, hora, especialista_id))
        conflito = cursor.fetchone()[0] > 0
        conn.close()
        return conflito

    # Função para verificar o limite de especialistas para um paciente
    def verificar_limite_especialistas(paciente_id):
        conn = sqlite3.connect('database/sistema.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(DISTINCT especialista_id)
            FROM agendamentos
            WHERE paciente_id = ?
        """, (paciente_id,))
        especialista_count = cursor.fetchone()[0]
        conn.close()
        return especialista_count >= 2

    # Função para preencher horários disponíveis
    def preencher_horarios(event=None):
        especialista_id = especialista_combobox.get().split(" - ")[0]
        dia_semana = dia_combobox.get()

        if not especialista_id or not dia_semana:
            return

        conn = sqlite3.connect('database/sistema.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT horarios
            FROM especialistas
            WHERE id = ?
        """, (especialista_id,))
        horarios = cursor.fetchone()
        conn.close()

        if horarios:
            entrada, saida = horarios[0].split(" - ")
            horarios_disponiveis = []
            atual = datetime.strptime(entrada, "%H:%M")
            final = datetime.strptime(saida, "%H:%M")

            while atual < final:
                horario = atual.strftime("%H:%M")
                data = dia_para_data(dia_semana)
                if not verificar_conflitos(data, horario, especialista_id):
                    horarios_disponiveis.append(horario)
                atual += timedelta(minutes=30)

            hora_combobox.configure(values=horarios_disponiveis)
            hora_combobox.set("")

    # Converter dia da semana para a próxima data correspondente
    def dia_para_data(dia_semana):
        dias_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"]
        hoje = datetime.now()
        dia_index = dias_semana.index(dia_semana)
        delta_dias = (dia_index - hoje.weekday() + 7) % 7
        proxima_data = hoje + timedelta(days=delta_dias)
        return proxima_data.strftime("%d/%m/%Y")

    # Função para cadastrar um agendamento
    def cadastrar_agendamento():
        paciente_id = paciente_combobox.get().split(" - ")[0]
        especialista_id = especialista_combobox.get().split(" - ")[0]
        dia_semana = dia_combobox.get()
        hora = hora_combobox.get()
        frequencia = frequencia_combobox.get()

        if not paciente_id or not especialista_id or not dia_semana or not hora or not frequencia:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        if verificar_limite_especialistas(paciente_id):
            messagebox.showerror("Erro", "O paciente já atingiu o limite de 2 especialistas.")
            return

        data = dia_para_data(dia_semana)

        if verificar_conflitos(data, hora, especialista_id):
            messagebox.showerror("Erro", "Já existe um agendamento para esse horário.")
            return

        conn = sqlite3.connect('database/sistema.db')
        cursor = conn.cursor()

        # Adicionar agendamentos de acordo com a frequência
        delta = 7 if frequencia == "Semanal" else 14
        data_atual = datetime.strptime(data, "%d/%m/%Y")
        for _ in range(10):  # Limitar a 10 semanas
            cursor.execute("""
                INSERT INTO agendamentos (paciente_id, especialista_id, data, hora, status, justificativa)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (paciente_id, especialista_id, data_atual.strftime("%d/%m/%Y"), hora, "Pendente", ""))
            data_atual += timedelta(days=delta)

        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Agendamento cadastrado com sucesso!")
        listar_agendamentos()

    # Layout da janela
    ctk.CTkLabel(
        agendamentos_window,
        text="Gerenciamento de Agendamentos",
        font=("Arial", 20, "bold"),
        text_color="white"
    ).pack(pady=20)

    # Formulário de agendamento
    form_frame = ctk.CTkFrame(agendamentos_window, fg_color="#1a1a1a", corner_radius=10)
    form_frame.pack(pady=20, padx=20, fill="x")

    ctk.CTkLabel(form_frame, text="Paciente:", font=("Arial", 14), text_color="white").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    paciente_combobox = ctk.CTkComboBox(form_frame, width=300)
    paciente_combobox.grid(row=0, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Especialista:", font=("Arial", 14), text_color="white").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    especialista_combobox = ctk.CTkComboBox(form_frame, width=300, command=preencher_horarios)
    especialista_combobox.grid(row=1, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Dia da Semana:", font=("Arial", 14), text_color="white").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    dia_combobox = ctk.CTkComboBox(form_frame, values=["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"], width=300, command=preencher_horarios)
    dia_combobox.grid(row=2, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Hora:", font=("Arial", 14), text_color="white").grid(row=3, column=0, padx=10, pady=10, sticky="e")
    hora_combobox = ctk.CTkComboBox(form_frame, width=300)
    hora_combobox.grid(row=3, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Frequência:", font=("Arial", 14), text_color="white").grid(row=4, column=0, padx=10, pady=10, sticky="e")
    frequencia_combobox = ctk.CTkComboBox(form_frame, values=["Semanal", "Quinzenal"], width=300)
    frequencia_combobox.grid(row=4, column=1, padx=10, pady=10)

    ctk.CTkButton(
        form_frame,
        text="Cadastrar Agendamento",
        command=cadastrar_agendamento,
        fg_color="#0056b3",
        text_color="white"
    ).grid(row=5, column=1, pady=20)

    # Listagem de agendamentos
    agendamentos_frame = ctk.CTkFrame(agendamentos_window, fg_color="#1a1a1a", corner_radius=10)
    agendamentos_frame.pack(pady=20, padx=20, fill="both", expand=True)

    listar_agendamentos()

    # Preenchendo os comboboxes de pacientes e especialistas
    conn = sqlite3.connect('database/sistema.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM pacientes")
    pacientes = cursor.fetchall()
    paciente_combobox.configure(values=[f"{p[0]} - {p[1]}" for p in pacientes])

    cursor.execute("SELECT id, nome FROM especialistas")
    especialistas = cursor.fetchall()
    especialista_combobox.configure(values=[f"{e[0]} - {e[1]}" for e in especialistas])

    conn.close()

    agendamentos_window.mainloop()
