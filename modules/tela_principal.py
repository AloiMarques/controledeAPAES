import sqlite3  # Importação necessária
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from pacientes import abrir_pacientes
from especialistas import abrir_especialistas
from agendamentos import abrir_agendamentos
from lembretes import abrir_lembretes, verificar_lembretes_hoje
from administracao import abrir_administracao
from backup import abrir_gerenciador_backups

# Função para abrir a tela principal
def abrir_tela_principal(role):
    main_window = tk.Tk()
    main_window.title("Sistema APAE - Tela Principal")
    main_window.geometry("900x600")
    main_window.configure(bg="#2b2b2b")

    # Função para exibir a agenda do dia
    def exibir_agenda():
        for widget in agenda_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect('database/sistema.db')
        cursor = conn.cursor()
        hoje = datetime.now().strftime("%d/%m/%Y")
        cursor.execute("""
            SELECT a.id, p.nome, e.nome, a.hora, a.status
            FROM agendamentos a
            JOIN pacientes p ON a.paciente_id = p.id
            JOIN especialistas e ON a.especialista_id = e.id
            WHERE a.data = ?
        """, (hoje,))
        agendamentos = cursor.fetchall()
        conn.close()

        if agendamentos:
            tk.Label(agenda_frame, text="Agenda do Dia:", font=("Arial", 14), bg="#2b2b2b", fg="white").pack(anchor="w", pady=5)
            for agendamento in agendamentos:
                tk.Label(
                    agenda_frame,
                    text=f"Paciente: {agendamento[1]} | Especialista: {agendamento[2]} | Hora: {agendamento[3]} | Status: {agendamento[4]}",
                    bg="#2b2b2b",
                    fg="white"
                ).pack(anchor="w", pady=2)
        else:
            tk.Label(agenda_frame, text="Nenhum agendamento para hoje.", bg="#2b2b2b", fg="white").pack(anchor="w", pady=5)

    # Layout da tela principal
    tk.Label(
        main_window,
        text="Sistema APAE",
        font=("Arial", 24),
        bg="#2b2b2b",
        fg="blue"
    ).pack(pady=10)

    # Botões para acessar funcionalidades
    btn_frame = tk.Frame(main_window, bg="#2b2b2b")
    btn_frame.pack(pady=20)

    tk.Button(
        btn_frame,
        text="Gerenciar Pacientes",
        command=abrir_pacientes,
        bg="blue",
        fg="white",
        width=20
    ).grid(row=0, column=0, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="Gerenciar Especialistas",
        command=abrir_especialistas,
        bg="blue",
        fg="white",
        width=20
    ).grid(row=0, column=1, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="Agendamentos",
        command=abrir_agendamentos,
        bg="blue",
        fg="white",
        width=20
    ).grid(row=0, column=2, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="Gerenciar Lembretes",
        command=abrir_lembretes,
        bg="blue",
        fg="white",
        width=20
    ).grid(row=1, column=0, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="Gerenciar Backups",
        command=abrir_gerenciador_backups,
        bg="blue",
        fg="white",
        width=20
    ).grid(row=1, column=1, padx=10, pady=10)

    if role == "admin":
        tk.Button(
            btn_frame,
            text="Administração",
            command=abrir_administracao,
            bg="blue",
            fg="white",
            width=20
        ).grid(row=1, column=2, padx=10, pady=10)

    # Frame da agenda do dia
    agenda_frame = tk.Frame(main_window, bg="#2b2b2b")
    agenda_frame.pack(pady=20, fill="both", expand=True)

    exibir_agenda()

    # Verificar lembretes ao abrir a tela principal
    verificar_lembretes_hoje()

    main_window.mainloop()
