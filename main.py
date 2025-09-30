from flask import Flask, render_template, redirect, request, session, jsonify, flash, url_for
from functools import wraps
from model import *

def verificaSessao(f):
    @wraps(f)
    def verificando(*args, **kwargs):
        if 'nome' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return verificando

app = Flask(__name__)
app.secret_key = '29bfd352-ed9e-4818-b05b-498b8f77e4e3'

@app.route("/")
def home():

    return render_template("home.html")


## ---------------LOGIN---------------- ##



## ----------------LISTAGENS----------------- ##

@app.route("/turma")
def turma():
    turmas = buscarTurmas()
    print(turmas[0]['pk_nome_turma'])
    return render_template("turma.html", turmas=turmas)

@app.route("/alunosPorTurma/<turma>")
def alunosPorTurma(turma):
    alunos = buscarAlunosPorTurma(turma)
      # função do model que retorna lista de alunos da turma
    return jsonify({"alunos": [{"matricula": a[0], "nome": a[1]} for a in alunos]})

if __name__ == "__main__":
    app.run(debug=True)


## ----------------CADASTRAR ALUNOS---------------##

@app.route("/cadastrarAluno", methods=["GET"])
def paginacadastrarAluno():
    alunos = buscarAlunos()
    turmas = buscarTurmas()
    print(turmas[0]['pk_nome_turma'])
    return render_template("cadastrarAluno.html", alunos=alunos, turmas = turmas)

@app.route("/cadastrarAluno", methods=["POST"])
def rotaCadastrarAluno():
    nome = request.form.get("nome")
    matricula = request.form.get("matricula")
    turma = request.form.get("turma")
    genero = request.form.get("genero")

    cadastrarAluno(matricula, nome, turma, genero)
    alunos = buscarAlunos()
    return render_template("cadastrarAluno.html", alunos=alunos)

@app.route("/editarAluno/<matricula>", methods=["POST"])
def rotaEditarAluno(matricula):
    nome = request.form.get("nome")
    turma = request.form.get("turma")
    genero = request.form.get("genero")

    editarAluno(matricula, nome, turma, genero)
    alunos = buscarAlunos()
    return render_template("cadastrarAluno.html", alunos=alunos)

@app.route("/deletarAluno/<matricula>")
def rotaDeletarAluno(matricula):
    deletarAluno(matricula)
    alunos = buscarAlunos()
    return render_template("cadastrarAluno.html", alunos=alunos)


## ------------------CADASTRAR TURMAS-------------------- ##

# Cadastrar
@app.route("/cadastrarTurma", methods=["POST"])
def rotaCadastrarTurma():
    pk_nome_turma = request.form.get("pk_nome_turma")
    cadastrarTurma(pk_nome_turma)
    turmas = buscarTurmas()
    return render_template("turma.html", turmas=turmas)

# Editar
@app.route("/editarTurma/<string:turma>", methods=["POST"])
def rotaEditarTurma(turma):
    novo_nome = request.form.get("pk_nome_turma")
    editarTurma(turma, novo_nome)
    turmas = buscarTurmas()
    return render_template("turma.html", turmas=turmas)

# Deletar
@app.route("/deletarTurma/<string:turma>")
def rotaDeletarTurma(turma):
    deletarTurma(turma)
    turmas = buscarTurmas()
    return render_template("turma.html", turmas=turmas)


## ---------------------CADASTRAR EQUIPE---------------------- ##

@app.route("/cadastrarEquipe", methods=["GET"])
def paginaCadastrarEquipe():
    equipes = buscarEquipes()
    esportes = buscarEsportes()
    turmas = buscarTurmas()
    classificacoes = buscarClassificacoes()
    return render_template("cadastrarEquipe.html",
                           equipes=equipes,
                           esportes=esportes,
                           turmas=turmas,
                           classificacoes=classificacoes)

@app.route("/cadastrarEquipe", methods=["POST"])
def rotaCadastrarEquipe():
    esporte = request.form.get("esporte")
    turma = request.form.get("turma")
    descricao = request.form.get("descricao")
    alunos = request.form.getlist("alunos")

    cadastrarEquipe(esporte, turma, descricao, alunos)

    return redirect("/cadastrarEquipe")

@app.route("/editarEquipe/<int:pk_equipe>", methods=["POST"])
def rotaEditarEquipe(pk_equipe):
    esporte = request.form.get("esporte")
    turma = request.form.get("turma")
    descricao = request.form.get("descricao")
    alunos = request.form.getlist("alunos")

    editarEquipe(pk_equipe, esporte, turma, descricao, alunos)
    return redirect("/cadastrarEquipe")

#Deletar equipe
@app.route("/deletarEquipe/<int:pk_equipe>")
def rotaDeletarEquipe(pk_equipe):
    deletarEquipe(pk_equipe)
    return redirect("/cadastrarEquipe")

# Buscar alunos por turma (JSON)
@app.route("/alunosPorTurma/<nome_turma>")
def alunosPorTurmaEquipes(nome_turma):
    alunos = alunosPorTurmaListaEquipes(nome_turma)
    return jsonify({"alunos": alunos})

# Jogadores de uma equipe (JSON)
@app.route("/jogadoresPorEquipe/<int:id_equipe>")
def jogadoresPorEquipe(id_equipe):
    jogadores = buscarJogadoresPorEquipe(id_equipe)
    return jsonify({"jogadores": jogadores})


## -------------------CADASTRO DO USUARIO------------------ ##

# Página de cadastro
@app.route("/cadastrarUsuario", methods=["GET"])
def paginaCadastrarUsuario():
    usuarios = telaUsuarios()
    turmas = buscarTurmas()
    return render_template("cadastrarUsuario.html", usuarios=usuarios, turmas=turmas)

# Inserção no banco
@app.route("/cadastrarUsuario", methods=["POST"])
def rotaCadastrarUsuario():
    pk_usuario = request.form.get("pk_usuario")
    senha = request.form.get("senha")
    nivel = request.form.get("nivel")
    fk_nome_turma = request.form.get("fk_nome_turma") if nivel == "AlunoMonitor" else None

    #--Validação: aluno monitor precisa de turma
    if nivel == "AlunoMonitor" and (not fk_nome_turma or fk_nome_turma.strip() == ""):
        flash("Erro: Aluno Monitor precisa estar vinculado a uma turma.", "error")
        return redirect(url_for("paginaCadastrarUsuario"))

    cadastrarUsuario(pk_usuario, senha, nivel, fk_nome_turma)
    flash("Usuário cadastrado com sucesso!", "success")
    return redirect(url_for("paginaCadastrarUsuario"))

# Edição
@app.route("/editarUsuario/<pk_usuario>", methods=["POST"])
def rotaEditarUsuario(pk_usuario):
    novo_usuario = request.form.get("pk_usuario")
    senha = request.form.get("senha")  # opcional
    nivel = request.form.get("nivel")
    fk_nome_turma = request.form.get("fk_nome_turma") if nivel == "AlunoMonitor" else None

    #--Validação
    if nivel == "AlunoMonitor" and (not fk_nome_turma or fk_nome_turma.strip() == ""):
        flash("Erro: Aluno Monitor precisa estar vinculado a uma turma.", "error")
        return redirect(url_for("paginaCadastrarUsuario"))

    editarUsuario(pk_usuario, novo_usuario, senha, nivel, fk_nome_turma)
    flash("Usuário atualizado com sucesso!", "success")
    return redirect(url_for("paginaCadastrarUsuario"))

# Deleção
@app.route("/deletarUsuario/<pk_usuario>")
def rotaDeletarUsuario(pk_usuario):
    deletarUsuario(pk_usuario)
    usuarios = telaUsuarios()
    turmas = buscarTurmas()
    return render_template("cadastrarUsuario.html", usuarios=usuarios, turmas=turmas)


# ## ----------------CHAVEAMENTO------------------ ##

# @app.route("/chaveamento")
# def paginaChaveamento():
#     esportes = buscarEsportes()
#     return render_template("chaveamento.html", esportes=esportes)

# # Buscar equipes de um esporte
# @app.route("/equipesPorEsporte/<string:esporte>")
# def equipesPorEsporte(esporte):
#     equipes = buscarEquipesPorEsporte(esporte)  # você precisa implementar no model
#     return jsonify({"equipes": [
#         {"id": e[0], "nome": e[1], "turma": e[2], "descricao": e[3]} for e in equipes
#     ]})
