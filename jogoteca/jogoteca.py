from flask import Flask, render_template, request, redirect
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

# Define as rotas da aplicação.
@app.route('/')
def index():
    return render_template('lista.html', titulo = 'Jogos', jogos = lista_de_jogos)

@app.route('/novo')
def novo():    
    return render_template('novo.html', titulo= 'Novo Jogo')

@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista_de_jogos.append(jogo)
    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = request.form['usuario']
    senha = request.form['senha']
    if usuario == 'admin' and senha == '123':
        return redirect('/')
    else:
        return redirect('/login')
    

app.run(debug=True)
#Caso eu queira usara a porta 8080 para a aplicação ou permitir acessos internos
# trecho da app
# app.run(host='0.0.0.0', port=8080)
