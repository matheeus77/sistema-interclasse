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

function abrirModalEdicao(id, esporte, turma, descricao, nomeEquipe) {
    document.getElementById("editId").value = id;
    document.getElementById("editEsporte").value = esporte;
    document.getElementById("editTurma").value = turma;
    document.getElementById("editDescricao").value = descricao;
    document.getElementById("editNomeEquipe").value = nomeEquipe || "";

    formEdicao.action = "/editarEquipe/" + id;

    carregarAlunosEdicao(turma, id);
    modalEdicao.style.display = "block";
}
closeEditBtn.onclick = () => modalEdicao.style.display = "none";

// MODAL CONFIRMAÇÃO
const modalConfirmacao = document.getElementById("modalConfirmacao");
const textoConfirmacao = document.getElementById("textoConfirmacao");
const btnCancelar = document.getElementById("btnCancelar");
const btnConfirmar = document.getElementById("btnConfirmar");

function confirmarDelecao(id, equipe) {
    textoConfirmacao.textContent = `Deseja realmente deletar a equipe ${equipe}?`;
    btnConfirmar.href = "/deletarEquipe/" + id;
    modalConfirmacao.style.display = "block";
}
btnCancelar.onclick = () => modalConfirmacao.style.display = "none";

// FILTRO DE BUSCA
const searchInput = document.getElementById('searchInput');
searchInput.addEventListener('keyup', function () {
    const filter = this.value.toLowerCase();
    const rows = document.querySelectorAll('.styled-table tbody tr');

    rows.forEach(row => {
        const esporte = row.cells[0].textContent.toLowerCase();
        const turma = row.cells[1].textContent.toLowerCase();
        const descricao = row.cells[2].textContent.toLowerCase();
        row.style.display = (esporte.includes(filter) || turma.includes(filter) || descricao.includes(filter)) ? '' : 'none';
    });
});

let limiteJogadores = null;

// Setar limite de jogadores ao selecionar esporte
function setLimiteJogadores(select) {
    const option = select.options[select.selectedIndex];
    limiteJogadores = parseInt(option.getAttribute("data-limite"));
}

// Bloquear seleção acima do limite
function aplicarLimite(containerId) {
    const container = document.getElementById(containerId);
    if (!container || !limiteJogadores) return;

    const checkboxes = container.querySelectorAll("input[type='checkbox']");
    checkboxes.forEach(cb => {
        cb.addEventListener("change", () => {
            const selecionados = container.querySelectorAll("input[type='checkbox']:checked").length;
            if (selecionados > limiteJogadores) {
                cb.checked = false;
                alert(`O limite para este esporte é de ${limiteJogadores} jogadores.`);
            }
        });
    });
}

// ----- carregar alunos no cadastro -----
function carregarAlunosTurma() {
    const turma = document.getElementById("turma").value;
    const classificacao = document.getElementById("descricao").value;

    if (!turma || !classificacao) {
        document.getElementById("alunosTurmaContainer").innerHTML =
            "<p>Selecione uma turma e classificação para listar os alunos.</p>";
        return;
    }

    fetch(`/alunosPorTurma/${encodeURIComponent(turma)}/${encodeURIComponent(classificacao)}`)
        .then(response => response.json())
        .then(data => {
            let html = '';
            if (data.alunos.length === 0) {
                html = "<p>Nenhum aluno cadastrado nesta turma com essa classificação.</p>";
            } else {
                data.alunos.forEach(aluno => {
                    html += `
                        <div>
                            <input type="checkbox" name="alunos" value="${aluno.matricula}">
                            ${aluno.nome}
                        </div>`;
                });
            }
            document.getElementById("alunosTurmaContainer").innerHTML = html;
            aplicarLimite("alunosTurmaContainer");
        })
        .catch(error => console.error("Erro ao carregar alunos:", error));
}
document.getElementById("turma").addEventListener("change", carregarAlunosTurma);
document.getElementById("descricao").addEventListener("change", carregarAlunosTurma);

// ----- carregar alunos no modal edição -----
function carregarAlunosEdicao(turma, idEquipe) {
    if (!turma) {
        document.getElementById("editAlunosTurmaContainer").innerHTML = "<p>Selecione uma turma.</p>";
        return;
    }
    fetch(`/alunosPorTurma/${encodeURIComponent(turma)}`)
        .then(res => res.json())
        .then(data => {
            fetch(`/jogadoresPorEquipe/${idEquipe}`)
                .then(res => res.json())
                .then(equipeData => {
                    let jogadoresEquipe = equipeData.jogadores.map(j => j.matricula);
                    let html = '';
                    data.alunos.forEach(aluno => {
                        const checked = jogadoresEquipe.includes(aluno.matricula) ? 'checked' : '';
                        html += `
                            <div>
                                <input type="checkbox" name="alunos" value="${aluno.matricula}" ${checked}>
                                ${aluno.nome}
                            </div>`;
                    });
                    document.getElementById("editAlunosTurmaContainer").innerHTML = html;
                    aplicarLimite("editAlunosTurmaContainer");
                });
        });
}

// ----- jogadores modal -----
const modalJogadores = document.getElementById("modalJogadores");
const closeJogadores = document.getElementById("closeJogadores");
const listaJogadores = document.getElementById("listaJogadores");
const tituloEquipe = document.getElementById("tituloEquipe");
let subTituloEquipe = document.getElementById("subTituloEquipe");

// Fechar modal ao clicar no "x"
closeJogadores.onclick = () => modalJogadores.style.display = "none";

// Fechar modal ao clicar fora
window.addEventListener('click', (event) => {
    if (event.target == modalJogadores) {
        modalJogadores.style.display = "none";
    }
});

function abrirModalJogadores(idEquipe, esporte, grupo, nomeEquipe) {
    fetch(`/jogadoresPorEquipe/${idEquipe}`)
        .then(response => response.json())
        .then(data => {
            listaJogadores.innerHTML = '';
            if (data.jogadores.length === 0) {
                listaJogadores.innerHTML = '<li>Nenhum jogador nesta equipe.</li>';
            } else {
                data.jogadores.forEach(jogador => {
                    const li = document.createElement('li');
                    li.textContent = `${jogador.nome}`;
                    listaJogadores.appendChild(li);
                });
            }
            tituloEquipe.innerText = `${esporte} - ${grupo}`;
            if(subTituloEquipe) subTituloEquipe.innerText = nomeEquipe ? nomeEquipe : '';
            modalJogadores.style.display = "block";
        });
}
