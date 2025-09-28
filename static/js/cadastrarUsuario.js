// MODAL CADASTRO
const modalCadastro = document.getElementById("modalCadastro");
const openBtn = document.getElementById("openModalBtn");
const closeBtn = document.getElementById("closeModalBtn");

openBtn.onclick = () => modalCadastro.style.display = "block";
closeBtn.onclick = () => modalCadastro.style.display = "none";

// MODAL EDIÇÃO
const modalEdicao = document.getElementById("modalEdicao");
const closeEditBtn = document.getElementById("closeEditBtn");
const formEdicao = document.getElementById("formEdicao");

// CAMPOS DE TURMA (cadastro)
const nivelSelect = document.getElementById("nivel");
const turmaGroup = document.getElementById("turmaCadastro");

// CAMPOS DE TURMA (edicao)
const editNivelSelect = document.getElementById("editNivel");
const editTurmaGroup = document.getElementById("turmaEdicao");

function abrirModalEdicao(usuario, nivel, turma = "") {
    document.getElementById("editUsuario").value = usuario;
    document.getElementById("editNivel").value = nivel;

    // definir a action do form de edição (usar o usuário antigo como chave)
    formEdicao.action = "/editarUsuario/" + usuario;

    // mostrar/ocultar e setar turma
    if (nivel === "AlunoMonitor") {
        editTurmaGroup.style.display = "block";
        const sel = document.getElementById("edit_fk_nome_turma");
        if (sel) sel.value = turma || "";
    } else {
        editTurmaGroup.style.display = "none";
    }

    modalEdicao.style.display = "block";
}

closeEditBtn.onclick = () => modalEdicao.style.display = "none";

// MODAL CONFIRMAÇÃO
const modalConfirmacao = document.getElementById("modalConfirmacao");
const textoConfirmacao = document.getElementById("textoConfirmacao");
const btnCancelar = document.getElementById("btnCancelar");
const btnConfirmar = document.getElementById("btnConfirmar");

function confirmarDelecao(usuario) {
    textoConfirmacao.textContent = `Deseja realmente deletar o usuário ${usuario}?`;
    btnConfirmar.href = "/deletarUsuario/" + usuario;
    modalConfirmacao.style.display = "block";
}

btnCancelar.onclick = () => modalConfirmacao.style.display = "none";

// MODAL ERRO
const modalErro = document.getElementById("modalErro");
const textoErro = document.getElementById("textoErro");
const btnFecharErro = document.getElementById("btnFecharErro");

btnFecharErro.onclick = () => modalErro.style.display = "none";

// Validação no cadastro (cliente)
const formCadastro = document.querySelector("#formCadastro");
formCadastro.addEventListener("submit", function (event) {
    const nivel = document.getElementById("nivel").value;
    const turma = document.getElementById("fk_nome_turma") ? document.getElementById("fk_nome_turma").value : "";

    if (nivel === "AlunoMonitor" && (!turma || turma.trim() === "")) {
        event.preventDefault();
        textoErro.textContent = "Erro: Aluno Monitor precisa estar vinculado a uma turma.";
        modalErro.style.display = "block";
    }
});

// Validação na edição (cliente)
formEdicao.addEventListener("submit", function (event) {
    const nivel = document.getElementById("editNivel").value;
    const turmaEl = document.getElementById("edit_fk_nome_turma");
    const turma = turmaEl ? turmaEl.value : "";

    if (nivel === "AlunoMonitor" && (!turma || turma.trim() === "")) {
        event.preventDefault();
        textoErro.textContent = "Erro: Aluno Monitor precisa estar vinculado a uma turma.";
        modalErro.style.display = "block";
    }
});

// FECHAR MODAIS AO CLICAR FORA
window.onclick = (event) => {
    if (event.target == modalCadastro) modalCadastro.style.display = "none";
    if (event.target == modalEdicao) modalEdicao.style.display = "none";
    if (event.target == modalConfirmacao) modalConfirmacao.style.display = "none";
    if (event.target == modalErro) modalErro.style.display = "none";
};

// Mostrar ou esconder turma quando mudar o nível
function toggleTurmaSelect(tipo) {
    if (tipo === "cadastro") {
        const nivel = document.getElementById("nivel").value;
        document.getElementById("turmaCadastro").style.display = nivel === "AlunoMonitor" ? "block" : "none";
    } else if (tipo === "edicao") {
        const nivel = document.getElementById("editNivel").value;
        document.getElementById("turmaEdicao").style.display = nivel === "AlunoMonitor" ? "block" : "none";
    }
}

// FILTRO DE BUSCA
const searchInput = document.getElementById('searchInput');
searchInput.addEventListener('keyup', function () {
    const filter = this.value.toLowerCase();
    const rows = document.querySelectorAll('.styled-table tbody tr');

    rows.forEach(row => {
        const usuario = row.cells[0].textContent.toLowerCase();
        const nivel = row.cells[1].textContent.toLowerCase();
        row.style.display = (usuario.includes(filter) || nivel.includes(filter)) ? '' : 'none';
    });
});