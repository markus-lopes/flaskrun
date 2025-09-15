from flask import Flask, render_template, request, redirect, url_for
from models import db, Tarefa

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        descricao = request.form.get('descricao')
        if descricao:
            nova = Tarefa(descricao=descricao)
            db.session.add(nova)
            db.session.commit()
        return redirect(url_for('index'))
    tarefas = Tarefa.query.all()
    return render_template('index.html',tarefas=tarefas)

@app.route('/delete/<int:id>')
def delete(id):
    tarefa = Tarefa.query.get_or_404(id)
    db.session.delete(tarefa)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>',methods=['GET', 'POST'])
def edit(id):
    tarefa = Tarefa.query.get_or_404(id)
    if request.method=='POST':
        tarefa.descricao=request.form.get('descricao')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html',tarefa=tarefa)

