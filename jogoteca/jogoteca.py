from flask import Flask, render_template, request, redirect, session, flash, url_for
#from flask_wtf.csrf import CSRFProtect

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console
        
jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('Pac-Man', 'Ação', 'Atari')
jogo3 = Jogo('Donkey Kong', 'Ação', 'Nintendo')
lista_de_jogos: list = [jogo1, jogo2, jogo3]
class Usuario:
    def __init__(self, nome, apelido, senha):
        self.nome = nome
        self.apelido = apelido
        self.senha = senha
        
usuario = Usuario('Julio', 'Jc', 'qwert')
usuario2 = Usuario('Jimmy', 'Jm', '4321')
usuario3 = Usuario('Maria', 'Ma', '7890')
        
usuarios = { 
            usuario.apelido : usuario,
            usuario2.apelido : usuario2,
            usuario3.apelido : usuario3
            }        
 
# Inicializador aplicação Flask
app = Flask(__name__)
app.secret_key = 'qualquer_chave' # para usar a sessão
#  Proteção contra ataques CSRF


# Define as rotas da aplicação.
@app.route('/')
def index():
    return render_template('lista.html', titulo = 'Jogos', jogos = lista_de_jogos)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        #return redirect('/login?proxima=novo') #query string ?proxima=<pagina>
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo= 'Novo Jogo')

@app.route('/criar', methods=['POST', ])
def criar():
    # Obter os dados do formulário
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    
    # Verificar se os campos estão preenchidos
    if nome and categoria and console:
        jogo = Jogo(nome, categoria, console)
        lista_de_jogos.append(jogo)
        return redirect(url_for('index'))
    else:
        # Mostrar mensagem de erro se os campos não estão preenchidos
        flash('Erro ao criar jogo. Por favor, preencha todos os campos.')
        return redirect(url_for('novo'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    # Verificar se o usuario existe
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        # Verificar se a senha está correta
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.apelido
            flash(usuario.apelido + 'logado com sucesso.')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
   
    else:
        # Mostrar mensagem de erro se o usuário não existe ou senha está incorreta
        flash('Usuário não logado, digite suas credenciais')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    # Verificar se o usuário está logado
    if 'usuario_logado' in session:
        session['usuario_logado'] = None
        flash('Logout efetuado com sucesso.')
    else:
        # Mostrar mensagem de erro se o usuário não está logado
        flash('Você não está logado.')
        return redirect(url_for('index'))

app.run(debug=True)
#Caso se queira usara a porta 8080 para a aplicação ou permitir acessos internos
# trecho da app
# app.run(host='0.0.0.0', port=8080)
