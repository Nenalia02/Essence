import sqlite3

class DataRecord:
    def __init__(self):
        """Inicializa o banco de dados"""
        self.conn = sqlite3.connect('database.db')
        self.create_tables()

    def create_tables(self):
        """Cria a tabela de usuários se não existir"""
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)

    def add_user(self, username, password):
        """Adiciona um novo usuário ao banco de dados"""
        try:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
            )
            return True  
        except sqlite3.IntegrityError:
            return False  

    def get_user(self, username):
        """Busca um usuário pelo nome e retorna um dicionário"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user:
            return {'id': user[0], 'username': user[1], 'password': user[2]}
    
        return None
