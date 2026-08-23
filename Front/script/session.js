const TEMPO_INATIVIDADE = 20 * 60 * 1000; // 20 minutos
const AVISO_EXPIRACAO = 1 * 60 * 1000; // 5 minutos


let timeoutLogout;
let timeoutAviso;
function fecharModal() {
    const modal = document.getElementById("modal-sessao");

    if (modal) {
        modal.style.display = "none";
    }
}
function logout() {
    sessionStorage.removeItem("token");
    window.location.href = "login.html";
}
function mostrarAviso() {
    const modal = document.getElementById("modal-sessao");

    if (modal) {
        modal.style.display = "flex";
    }
}
function reiniciarTemporizadores() {

    clearTimeout(timeoutAviso);
    clearTimeout(timeoutLogout);

    fecharModal();

    timeoutAviso = setTimeout(
        mostrarAviso,
        TEMPO_INATIVIDADE - AVISO_EXPIRACAO
    );

    timeoutLogout = setTimeout(
        logout,
        TEMPO_INATIVIDADE
    );
}
[
    "click",
    "mousemove",
    "keydown",
    "scroll",
    "touchstart"
].forEach(evento =>
    document.addEventListener(evento, reiniciarTemporizadores)
);
reiniciarTemporizadores();
document
    .getElementById("continuar-sessao")
    ?.addEventListener("click", reiniciarTemporizadores);