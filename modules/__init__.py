# __init__.py

import os

# Definir o caminho para o banco de dados
DB_PATH = "database/sistema.db"
BACKUP_PATH = "database/backups"

# Verifica e cria pastas necessárias ao inicializar o módulo
if not os.path.exists("database"):
    os.makedirs("database")
if not os.path.exists(BACKUP_PATH):
    os.makedirs(BACKUP_PATH)

# Informações sobre o sistema
__version__ = "1.0.0"
__author__ = "Seu Nome"
__description__ = "Sistema de Gerenciamento para APAE"
