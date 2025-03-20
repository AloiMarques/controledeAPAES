import sqlite3
import customtkinter as ctk
from tkinter import messagebox

# Configuração do tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Função para inicializar a janela de administração
def abrir_administracao():
    admin_window = ctk.CTk()
    admin_window.title("Administração - Sistema APAE")
    admin_window.geometry("1000x700")
    admin_window.configure(fg_color="#002060")  # Azul escuro da APAE

    # Função para listar usuários
    def listar_usuarios():
        for widget in usuarios_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect('database/sistema.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role FROM usuarios")
        usuarios = cursor.fetchall()
        conn.close()

        if usuarios:
            for usuario in usuarios:
                ctk.CTkLabel(
                    usuarios_frame,
                    text=f"ID: {usuario[0]} | Usuário: {usuario[1]} | Permissão: {usuario[2]}",
                    font=("Arial", 12),
                    text_color="white"
                ).pack(anchor="w", pady=5)
        else:
            ctk.CTkLabel(
                usuarios_frame,
                text="Nenhum usuário cadastrado.",
                font=("Arial", 12),
                text_color="white"
            ).pack(anchor="w", pady=5)

    # Função para cadastrar usuário
    def cadastrar_usuario():
        username = username_entry.get()
        password = password_entry.get()
        role = role_combobox.get()

        if not username or not password or not role:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        conn = sqlite3.connect('database/sistema.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        username_entry.delete(0, ctk.END)
        password_entry.delete(0, ctk.END)
        role_combobox.set("")
        listar_usuarios()

    # Função para editar usuário
    def editar_usuario():
        selected_id = usuario_id_entry.get()
        new_username = username_entry.get()
        new_password = password_entry.get()
        new_role = role_combobox.get()

        if not selected_id or not new_username or not new_password or not new_role:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        conn = sqlite3.connect('database/sistema.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET username=?, password=?, role=? WHERE id=?",
                       (new_username, new_password, new_role, selected_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
        listar_usuarios()

    # Função para excluir usuário
    def excluir_usuario():
        selected_id = usuario_id_entry.get()

        if not selected_id:
            messagebox.showerror("Erro", "Por favor, informe o ID do usuário para exclusão.")
            return

        conn = sqlite3.connect('database/sistema.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id=?", (selected_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
        listar_usuarios()

    # Função para visualizar escala de trabalho
    def visualizar_escala():
        for widget in escala_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect('database/sistema.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nome, dias_semana, horarios FROM especialistas")
        escala = cursor.fetchall()
        conn.close()

        if escala:
            for item in escala:
                ctk.CTkLabel(
                    escala_frame,
                    text=f"Nome: {item[0]} | Dias: {item[1]} | Horários: {item[2]}",
                    font=("Arial", 12),
                    text_color="white"
                ).pack(anchor="w", pady=5)
        else:
            ctk.CTkLabel(
                escala_frame,
                text="Nenhum funcionário cadastrado na escala.",
                font=("Arial", 12),
                text_color="white"
            ).pack(anchor="w", pady=5)

    # Layout da janela
    ctk.CTkLabel(
        admin_window,
        text="Administração de Usuários",
        font=("Arial", 20, "bold"),
        text_color="white"
    ).pack(pady=20)

    # Formulário de cadastro/edição
    form_frame = ctk.CTkFrame(admin_window, fg_color="#1a1a1a", corner_radius=10)
    form_frame.pack(pady=10, padx=20, fill="x")

    ctk.CTkLabel(form_frame, text="ID do Usuário (para editar/excluir):", font=("Arial", 14), text_color="white").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    usuario_id_entry = ctk.CTkEntry(form_frame, width=300)
    usuario_id_entry.grid(row=0, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Nome de Usuário:", font=("Arial", 14), text_color="white").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    username_entry = ctk.CTkEntry(form_frame, width=300)
    username_entry.grid(row=1, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Senha:", font=("Arial", 14), text_color="white").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    password_entry = ctk.CTkEntry(form_frame, width=300, show="*")
    password_entry.grid(row=2, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Permissão:", font=("Arial", 14), text_color="white").grid(row=3, column=0, padx=10, pady=10, sticky="e")
    role_combobox = ctk.CTkComboBox(form_frame, values=["admin", "recepcionista"])
    role_combobox.grid(row=3, column=1, padx=10, pady=10)

    ctk.CTkButton(form_frame, text="Cadastrar Usuário", command=cadastrar_usuario, fg_color="#0056b3").grid(row=4, column=0, pady=20, padx=10)
    ctk.CTkButton(form_frame, text="Editar Usuário", command=editar_usuario, fg_color="#0056b3").grid(row=4, column=1, pady=20, padx=10)
    ctk.CTkButton(form_frame, text="Excluir Usuário", command=excluir_usuario, fg_color="#0056b3").grid(row=4, column=2, pady=20, padx=10)

    # Listagem de usuários
    usuarios_frame = ctk.CTkFrame(admin_window, fg_color="#1a1a1a", corner_radius=10)
    usuarios_frame.pack(pady=20, padx=20, fill="x")
    listar_usuarios()

    # Visualizar escala de trabalho
    ctk.CTkLabel(
        admin_window,
        text="Escala de Trabalho dos Funcionários",
        font=("Arial", 20, "bold"),
        text_color="white"
    ).pack(pady=20)

    escala_frame = ctk.CTkFrame(admin_window, fg_color="#1a1a1a", corner_radius=10)
    escala_frame.pack(pady=10, padx=20, fill="x")
    visualizar_escala()

    admin_window.mainloop()
