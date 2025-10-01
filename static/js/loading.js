// Mostra loading (pode ser chamado manualmente quando precisar)
function showLoading(message = "Carregando... Por favor, aguarde") {
  const loading = document.getElementById("loading");
  if (!loading) return;
  loading.style.display = "flex";
  const msg = loading.querySelector(".msg");
  if (msg) msg.textContent = message;
}

// Esconde loading
function hideLoading() {
  const loading = document.getElementById("loading");
  if (!loading) return;
  loading.style.display = "none";
}

// Ao carregar a página, remove o loading automaticamente
window.addEventListener("load", () => {
  hideLoading();
});
