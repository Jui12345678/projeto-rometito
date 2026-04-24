from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'segredo'

usuarios = []
tarefas = []


@app.route('/')
def index():
    return redirect('/login')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        usuarios.append({'nome': nome, 'senha': senha})

        return redirect('/login')

    return render_template('cadastro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        for u in usuarios:
            if u['nome'] == nome and u['senha'] == senha:
                session['user'] = nome
                return redirect('/home')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/home')
def home():
    status = request.args.get('status')

    if status:
        filtradas = [t for t in tarefas if t['status'] == status]
    else:
        filtradas = tarefas

    return render_template('home.html', tarefas=filtradas)


@app.route('/criar', methods=['POST'])
def criar():
    titulo = request.form['titulo']

    tarefas.append({
        'id': len(tarefas),
        'titulo': titulo,
        'status': 'pendente'
    })

    return redirect('/home')


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    tarefa = tarefas[id]

    if request.method == 'POST':
        tarefa['titulo'] = request.form['titulo']
        tarefa['status'] = request.form['status']
        return redirect('/home')

    return render_template('editar.html', tarefa=tarefa, id=id)


@app.route('/deletar/<int:id>')
def deletar(id):
    tarefas.pop(id)
    return redirect('/home')


if __name__ == '__main__':
    app.run(debug=True)
