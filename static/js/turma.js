// MODAL CADASTRO
const modalCadastro = document.getElementById("modalCadastro");
const openBtn = document.getElementById("openModalBtn");
const closeBtn = document.getElementById("closeModalBtn");
if (openBtn) {
    openBtn.onclick = () => modalCadastro.style.display = "block";
}
if (closeBtn) {
    closeBtn.onclick = () => modalCadastro.style.display = "none";
}

window.onclick = (event) => {
    if (event.target == modalCadastro) modalCadastro.style.display = "none";
};

// MODAL EDIÇÃO
const modalEdicao = document.getElementById("modalEdicao");
const closeEditBtn = document.getElementById("closeEditBtn");
const formEdicao = document.getElementById("formEdicao");

function abrirModalEdicao(turma) {
    document.getElementById("editTurma").value = turma;
    formEdicao.action = "/editarTurma/" + turma;
    modalEdicao.style.display = "block";
}

closeEditBtn.onclick = () => modalEdicao.style.display = "none";

// MODAL CONFIRMAÇÃO
const modalConfirmacao = document.getElementById("modalConfirmacao");
const textoConfirmacao = document.getElementById("textoConfirmacao");
const btnCancelar = document.getElementById("btnCancelar");
const btnConfirmar = document.getElementById("btnConfirmar");

function confirmarDelecao(turma) {
    textoConfirmacao.textContent = `Deseja realmente deletar a turma ${turma}?`;
    btnConfirmar.href = "/deletarTurma/" + turma;
    modalConfirmacao.style.display = "block";
}

btnCancelar.onclick = () => modalConfirmacao.style.display = "none";

// MODAL ALUNOS
const modalAlunos = document.getElementById("modalAlunos");
const closeAlunos = document.getElementById("closeAlunos");
const listaAlunos = document.getElementById("listaAlunos");

closeAlunos.onclick = () => modalAlunos.style.display = "none";

function abrirModalAlunos(turma) {
    fetch(`/alunosPorTurma/${turma}`)
        .then(response => response.json())
        .then(data => {
            listaAlunos.innerHTML = '';
            if (data.alunos.length === 0) {
                listaAlunos.innerHTML = '<li>Nenhum aluno cadastrado nesta turma.</li>';
            } else {
                data.alunos.forEach(aluno => {
                    const li = document.createElement('li');
                    li.textContent =
                     `${aluno.nome}`;
                    listaAlunos.appendChild(li);
                });
            }
            document.getElementById('tituloModal').innerText = turma
            modalAlunos.style.display = "block";
        });
}

// FECHAR MODAIS AO CLICAR FORA
window.onclick = (event) => {
    if (event.target == modalCadastro) modalCadastro.style.display = "none";
    if (event.target == modalEdicao) modalEdicao.style.display = "none";
    if (event.target == modalConfirmacao) modalConfirmacao.style.display = "none";
    if (event.target == modalAlunos) modalAlunos.style.display = "none";
};