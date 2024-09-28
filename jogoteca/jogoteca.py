from flask import Flask, render_template, request, redirect, session, flash, url_for
class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console
        
jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('Pac-Man', 'Ação', 'Atari')
jogo3 = Jogo('Donkey Kong', 'Ação', 'Nintendo')
lista_de_jogos: list = [jogo1, jogo2, jogo3]

# Inicializador aplicação Flask
app = Flask(__name__)
app.secret_key = 'qualquer_chave' # para usar a sessão

# Define as rotas da aplicação.
@app.route('/')
def index():
    return render_template('lista.html', titulo = 'Jogos', jogos = lista_de_jogos)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session ou session['usuario_logado'] == None:
        #return redirect('/login?proxima=novo') #query string ?proxima=<pagina>
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo= 'Novo Jogo')

@app.route('/criar', methods=['POST', ])
def criar():
    
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista_de_jogos.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if 'senha' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario']
        flash(session['usuario_logado'] + 'logado com sucesso.')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)
    else:
        flash('Usuário não logado, digite suas credenciais')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso.')
    return redirect(url_for('index'))

app.run(debug=True)
#Caso se queira usara a porta 8080 para a aplicação ou permitir acessos internos
# trecho da app
# app.run(host='0.0.0.0', port=8080)
