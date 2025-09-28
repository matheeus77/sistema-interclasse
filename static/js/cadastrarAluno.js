// MODAL CADASTRO
const modalCadastro = document.getElementById("modalCadastro");
const openBtn = document.getElementById("openModalBtn");
const closeBtn = document.getElementById("closeModalBtn");

openBtn.onclick = () => modalCadastro.style.display = "block";
closeBtn.onclick = () => modalCadastro.style.display = "none";
window.onclick = (event) => {
    if (event.target == modalCadastro) modalCadastro.style.display = "none";
};

// MODAL EDIÇÃO
const modalEdicao = document.getElementById("modalEdicao");
const closeEditBtn = document.getElementById("closeEditBtn");
const formEdicao = document.getElementById("formEdicao");

function abrirModalEdicao(matricula, nome, turma, genero) {
    document.getElementById("editMatricula").value = matricula;
    document.getElementById("editNome").value = nome;
    document.getElementById("editGenero").value = genero;

    // Seleciona a turma correta
    const selectTurma = document.getElementById("editTurma");
    for (let i = 0; i < selectTurma.options.length; i++) {
        if (selectTurma.options[i].value === turma) {
            selectTurma.selectedIndex = i;
            break;
        }
    }

    formEdicao.action = "/editarAluno/" + matricula;
    modalEdicao.style.display = "block";
}

closeEditBtn.onclick = () => modalEdicao.style.display = "none";

// Fechar modal clicando fora
window.onclick = (event) => {
    if (event.target == modalEdicao) modalEdicao.style.display = "none";
};


// MODAL CONFIRMAÇÃO
const modalConfirmacao = document.getElementById("modalConfirmacao");
const textoConfirmacao = document.getElementById("textoConfirmacao");
const btnCancelar = document.getElementById("btnCancelar");
const btnConfirmar = document.getElementById("btnConfirmar");

function confirmarDelecao(matricula, nome) {
    textoConfirmacao.textContent = `Deseja realmente deletar ${nome}?`;
    btnConfirmar.href = "/deletarAluno/" + matricula;
    modalConfirmacao.style.display = "block";
}

btnCancelar.onclick = () => modalConfirmacao.style.display = "none";
window.onclick = (event) => {
    if (event.target == modalConfirmacao) modalConfirmacao.style.display = "none";
    if (event.target == modalEdicao) modalEdicao.style.display = "none";
};

// FILTRO DE BUSCA
const searchInput = document.getElementById('searchInput');
searchInput.addEventListener('keyup', function () {
    const filter = this.value.toLowerCase();
    const rows = document.querySelectorAll('.styled-table tbody tr');

    rows.forEach(row => {
        const nome = row.cells[1].textContent.toLowerCase();
        const matricula = row.cells[0].textContent.toLowerCase();

        row.style.display = (nome.includes(filter) || matricula.includes(filter)) ? '' : 'none';
    });
});