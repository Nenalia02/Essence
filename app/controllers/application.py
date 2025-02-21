from bottle import template, request, response, redirect
from app.models.DataRecord import DataRecord
import hashlib # Armazenamento de senhas de maneira segura

class Application():
    def __init__(self):
        # Dicionário de páginas
        self.pages = {
            'pagina': self.pagina,
            'portal': self.portal,
            'register': self.register
        }
        
        # Adaptador de banco de dados
        self.models = DataRecord()
    
    def render(self, page, parameter=None):
        """Renderiza a página solicitada."""
        content = self.pages.get(page, self.helper)
        if not parameter:
            return content()
        else:
            return content(parameter)
    
    def helper(self):
        """Renderiza a página de ajuda."""
        return template('app/views/html/helper')
    
    
    def pagina(self, parameter=None):
        """Renderiza a página principal ou a página personalizada do usuário."""
        if not parameter:
            return template('app/views/html/pagina', transferred=False)
    
        user = self.models.get_user(parameter)

        if not user:
            return redirect('/portal')  # Se usuário não existe, redireciona para login

        return template('app/views/html/user', username=user['username'])  # ✅ Exibe a página do usuário!

    
    def render_portal(self):
        """Renderiza a página do portal (login)."""
        return self.portal()  # Apenas chama a função portal diretamente
        
    def portal(self):
        """Renderiza a página do portal."""
        return template('app/views/html/portal')
    
    def authenticate_user(self, username, password):
        """Autentica o usuário verificando no banco de dados"""
        user = self.models.get_user(username)  # Recupera o usuário do banco

        if not user:
            return None, None  # Retorna dois valores para evitar erro
    
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
        if hashed_password != user['password']:  # Senha errada
            return None, None  

        session_id = hashlib.sha256(f"{username}{hashed_password}".encode()).hexdigest()
        
        return session_id, username  # Retorna corretamente os dois valores

    def logout_user(self):
        """Remove a sessão do usuário"""
        response.delete_cookie('session_id')

    def register(self):
        """Renderiza a página de cadastro"""
        return template('app/views/html/register')

    def register_user(self, username, password):
        """Registra um novo usuário no banco de dados"""
        if self.models.get_user(username):  # Verifica se já existe um usuário com esse nome
            return False  

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
        sucesso = self.models.add_user(username, hashed_password)
        return sucesso  
