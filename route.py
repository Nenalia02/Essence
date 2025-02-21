from app.controllers.application import Application
from bottle import Bottle, run, request, static_file, redirect, template, response
from gevent import monkey
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.websocket import WebSocketError

monkey.patch_all()

connections = set()  # Lista de conexões WebSocket ativas

# Inicializa a aplicação
app = Bottle(template_lookup=['./app/views/html'])
ctl = Application()

#-----------------------------------------------------------------------------#
# WebSocket para notificações em tempo real

@app.route('/ws')
def websocket():
    """Gerencia conexões WebSocket para notificações"""
    ws = request.environ.get('wsgi.websocket')
    if not ws:
        return "WebSocket não suportado", 400
    
    connections.add(ws)
    try:
        while True:
            message = ws.receive()
            if message is None:
                break  # Conexão fechada
            
            # Envia a mensagem para todos os usuários conectados
            for conn in connections:
                conn.send(message)
    except WebSocketError:
        pass
    finally:
        connections.remove(ws)

#-----------------------------------------------------------------------------#
# Rotas para arquivos estáticos

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    """Rota para servir arquivos estáticos como CSS, imagens e JS"""
    return static_file(filepath, root='./app/static')

#-----------------------------------------------------------------------------#
# Rotas de exibição de páginas (GET)

@app.route('/helper')
def helper():
    """Rota para exibir a página de ajuda"""
    return ctl.render('helper')

@app.route('/pagina')
@app.route('/pagina/<parameter>', method='GET')
def action_pagina(parameter=None):
    """Rota para exibir a página principal ou do usuário"""
    return ctl.render('pagina', parameter) if parameter else ctl.render('pagina')

@app.route('/portal', method='GET')
def login():
    """Rota para exibir o portal (login)"""
    return ctl.render_portal()

@app.route('/register', method='GET')
def show_register():
    """Rota para exibir a página de cadastro"""
    return ctl.render('register')

#-----------------------------------------------------------------------------#
# Rotas para processar ações (POST)

@app.route('/portal', method='POST')
def action_portal():
    """Processa o login do usuário"""
    username = request.forms.get('username')
    password = request.forms.get('password')
    
    session_id, username = ctl.authenticate_user(username, password)
    
    if session_id:
        response.set_cookie('session_id', session_id, httponly=True, secure=True, max_age=3600)
        redirect(f'/pagina/{username}')  # Agora redireciona corretamente para a página do usuário!
    else:
        return template('app/views/html/portal', error="Usuário ou senha incorretos!")  # Retorna erro


@app.route('/logout', method='POST')
def logout():
    """Processa o logout do usuário"""
    ctl.logout_user()
    response.delete_cookie('session_id')
    return redirect('/pagina')

@app.route('/register', method='POST')
def process_register():
    """Processa o cadastro do usuário"""
    username = request.forms.get('username')
    password = request.forms.get('password')

    if ctl.register_user(username, password):
        return redirect('/portal')  # Após cadastro, redireciona para o login
    else:
        return template('app/views/html/register', error="Esse usuário já existe, tente outro!")  

#-----------------------------------------------------------------------------#
# Inicializa o servidor
if __name__ == '__main__':
    try:
        print("Server running on http://0.0.0.0:8080")
        server = WSGIServer(("0.0.0.0", 8080), app, handler_class=WebSocketHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("Servidor interrompido. Fechando...")
